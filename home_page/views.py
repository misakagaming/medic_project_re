from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import NewsForm
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.models import User


# Create your views here.


class HomeView(View):
    def get(self, request):
        news_list = News.objects.all().order_by('-date_posted')
        paginator = Paginator(news_list, 4)
        page_number = request.GET.get('page')
        news = paginator.get_page(page_number)
        context = {
            'news': news
        }
        return render(request, 'home_page/home.html', context)


class UserNewsView(View):
    def get(self, request, username):
        user = User.objects.filter(username=username).first()
        news_list = News.objects.filter(author=user).order_by('-date_posted')
        paginator = Paginator(news_list, 4)
        page_number = request.GET.get('page')
        news = paginator.get_page(page_number)
        context = {
            'news': news,
            'username': username
        }
        return render(request, 'home_page/user_news.html', context)


class NewsDetailsView(View):
    def get(self, request, pk):
        news = News.objects.filter(pk=pk)
        if news:
            news = news.first()
            comments = Comment.objects.filter(author=news.author)
            context = {
                'news': news,
                'comment': comments
            }
            return render(request, 'home_page/news_detail.html', context)
        raise Http404


class NewsCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = NewsForm()
        return render(request, 'home_page/news_form.html', {'form': form})

    def post(self, request):
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news_created = form.save(commit=False)
            news_created.author = request.user
            news_created.save()
            return redirect('news-detail', pk=news_created.id)
        else:
            return render(request, 'home_page/news_form.html', {'form': form})


class NewsUpdateView(LoginRequiredMixin, View):
    def get(self, request, pk):
        news = News.objects.filter(pk=pk)
        if news:
            news = news.first()
            if not news.author_id == request.user.id:
                messages.error(request, f'Current authorised user is not the original author')
                return redirect('hospital-home')
            form = NewsForm(instance=news)
            return render(request, 'home_page/news_form.html', {'form': form})
        raise Http404

    def post(self, request, pk):
        news = News.objects.filter(pk=pk)
        if news:
            news = news.first()
            form = NewsForm(request.POST, request.FILES, instance=news)
            if form.is_valid():
                news_updated = form.save(commit=False)
                news_updated.author = request.user
                news_updated.save()
                return redirect('news-detail', pk=news_updated.id)
            else:
                return render(request, 'home_page/news_form.html', {'form': form})
        raise Http404


class NewsDeleteView(LoginRequiredMixin, View):
    def get(self, request, pk):
        news = News.objects.filter(pk=pk)
        if news:
            news = news.first()
            if not news.author_id == request.user.id:
                messages.error(request, f'Current authorised user is not the original author')
                return redirect('hospital-home')
            return render(request, 'home_page/news_confirm_delete.html', {'news': news})
        raise Http404

    def post(self, request, pk):
        news = News.objects.filter(pk=pk)
        if news:
            news.delete()
            messages.success(request, f'Post deleted')
            return redirect('hospital-home')
        raise Http404


class AboutView(View):
    def get(self, request):
        return render(request, 'home_page/about.html')
