from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from django.http import Http404
from .models import *

# Create your views here.


class UserMedicalHistoryView(LoginRequiredMixin, View):
    def get(self, request, username):
        patient = User.objects.get(username=username)
        records = MedicalHistoryRecord.objects.filter(patient=patient).order_by('-date_recorded')
        context = {
            'patient': patient,
            'records': records
        }
        return render(request, 'history/user_records.html', context)

