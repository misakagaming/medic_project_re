from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from appointment.models import Appointment
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
        appointment = Appointment.objects.filter(patient=patient, doctor_id=request.user.id)
        if not patient.id == request.user.id and not appointment:
            messages.error(request, f'Current authorised user is not the correct patient or doctor!')
            return redirect('hospital-home')
        return render(request, 'history/user_records.html', context)
