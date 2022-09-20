from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import Http404
from .models import *
from django.contrib import messages

# Create your views here.


class UserMedicalHistoryView(LoginRequiredMixin, View):
    def get(self, request, username):
        patient = User.objects.get(username=username)
        records = MedicalHistoryRecord.objects.filter(patient=patient).order_by('-date_recorded')
        context = {
            'patient': patient,
            'records': records
        }
        if not patient.id == request.user.id:
            messages.error(request, f'Current authorised user is not the correct patient')
            return redirect('hospital-home')
        return render(request, 'history/user_records.html', context)

