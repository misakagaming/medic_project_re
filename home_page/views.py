from django.shortcuts import render, redirect
from django.views import View
from django.db.models import *
from .forms import *
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from .models import News, Comment
from users.models import Profile
from history.models import MedicalHistoryRecord
from appointment.models import Appointment


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
        form = CommentForm()
        if news:
            news = news.first()
            comments = Comment.objects.filter(news=news).order_by('-date_posted')
            context = {
                'news': news,
                'comments': comments,
                'form': form
            }
            return render(request, 'home_page/news_detail.html', context)
        raise Http404

    def post(self, request, pk):
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment_created = form.save(commit=False)
            comment_created.author = request.user
            comment_created.news_id = pk
            comment_created.save()

        return redirect('news-detail', pk)


class AddCommentView(LoginRequiredMixin, View):
    def post(self, request, pk):
        form = CommentForm(request.POST, request.FILES)
        comments = Comment.objects.filter(news_id=pk).order_by('-date_posted')
        if form.is_valid():
            comment_created = form.save(commit=False)
            comment_created.author = request.user
            comment_created.news_id = pk
            comment_created.save()
            comments = Comment.objects.filter(news_id=pk).order_by('-date_posted')

        return render(request, 'home_page/comment_list.html', {'comments': comments})


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
        user_count = User.objects.count()
        news_count = News.objects.count()
        comment_count = Comment.objects.count()
        user_with_most_news = User.objects.get(pk=News.objects.values('author')
                                               .annotate(author_count=Count('author'))
                                               .order_by('-author_count').first()['author'])
        user_with_most_comments = User.objects.get(pk=Comment.objects.values('author')
                                                   .annotate(author_count=Count('author'))
                                                   .order_by('-author_count').first()['author'])

        patient_count = Profile.objects.filter(user_type='a').count()
        doctor_count = Profile.objects.filter(user_type='b').count()
        user_with_most_medical_records = User.objects.get(pk=MedicalHistoryRecord.objects.values('patient')
                                                          .annotate(patient_count=Count('patient'))
                                                          .order_by('-patient_count').first()['patient'])
        patient_with_most_appointments = User.objects.get(pk=Appointment.objects.values('patient')
                                                          .annotate(patient_count=Count('patient'))
                                                          .order_by('-patient_count').first()['patient'])
        doctor_with_most_appointments = User.objects.get(pk=Appointment.objects.values('doctor')
                                                          .annotate(doctor_count=Count('doctor'))
                                                          .order_by('-doctor_count').first()['doctor'])
        appointment_count = Appointment.objects.count()
        active_appointment_count = Appointment.objects.filter(active=True).count()

        context = {
            'user_count': user_count,
            'news_count': news_count,
            'comment_count': comment_count,
            'user_with_most_news': user_with_most_news,
            'user_with_most_comments': user_with_most_comments,
            'patient_count': patient_count,
            'doctor_count': doctor_count,
            'user_with_most_medical_records': user_with_most_medical_records,
            'patient_with_most_appointments': patient_with_most_appointments,
            'doctor_with_most_appointments': doctor_with_most_appointments,
            'appointment_count': appointment_count,
            'active_appointment_count': active_appointment_count
        }
        return render(request, 'home_page/about.html', context=context)
