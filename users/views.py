from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import Profile
from django.contrib.auth.models import User
from home_page.models import News


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()
            user.profile.user_type = form.cleaned_data.get('user_type')
            Profile.objects.update_or_create(user=user)
            user.save()
            messages.success(request, f'Account created!')
            return redirect('login')
        return render(request, 'users/register.html', {'form': form})


class ProfileView(View):
    def get(self, request, username):
        user = User.objects.get(username=username)
        profile = Profile.objects.get(user=user)
        news = News.objects.filter(author=user)
        u_form = UserUpdateForm(instance=user)
        p_form = ProfileUpdateForm(instance=user)
        context = {
            'u_form': u_form,
            'p_form': p_form,
            'title': f'Profile of {user.username}',
            'profile_user': user,
            'news': news,
            'profile': profile
        }
        return render(request, 'users/profile.html', context)

    def post(self, request, username):
        user = User.objects.get(username=username)
        u_form = UserUpdateForm(request.POST, instance=user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Account updated.')
            return redirect('profile', username=user.username)
        context = {
            'u_form': u_form,
            'p_form': p_form
        }
        return render(request, 'users/profile.html', context)
