from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from .forms import AppointmentForm, TreatmentForm
from .models import Appointment
from users.models import Profile
from history.models import MedicalHistoryRecord, Illness
from django.contrib.auth.models import User
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class MakeAppointmentView(LoginRequiredMixin, View):
    def get(self, request):
        form = AppointmentForm()
        return render(request, 'create_appointment.html', {'form': form})

    def post(self, request):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            if not Appointment.objects.filter(time=form.cleaned_data.get('time'), date=form.cleaned_data.get('date'),
                                              patient=request.user):
                appointment = form.save(commit=False)
                appointment.patient = request.user
                appointment.save()
                messages.success(request, f'Appointment created!')
                return redirect('list-appointment', request.user.username, 'active')
            messages.error(request, f'An appointment for this time and user already exists!')
        return render(request, 'create_appointment.html', {'form': form})


class AppointmentDetailView(View):
    def get(self, request, username, pk):
        appointment = Appointment.objects.get(pk=pk)
        if not (request.user == appointment.patient or request.user == appointment.doctor):
            messages.error(request, f'Current user is not the correct user!')
            return redirect('hospital-home')
        type = Profile.objects.get(user__username=username).user_type
        if appointment:
            context = {
                'user': User.objects.get(username=username),
                'appointment': appointment,
                'type': type
            }
            return render(request, 'appointment_detail.html', context)
        else:
            raise Http404


class ListAppointmentsView(View):
    def get(self, request, username, select):
        user = User.objects.get(username=username)
        if not request.user == user:
            messages.error(request, f'Current user is not the correct user!')
            return redirect('hospital-home')
        profile = Profile.objects.get(user__username=username)
        if profile.user_type == 'a':
            queryset = Appointment.objects.filter(patient__username=username).order_by('date', 'time').filter(active=True)
            queryset2 = Appointment.objects.filter(patient__username=username).order_by('date', 'time')
        else:
            queryset = Appointment.objects.filter(doctor__username=username).order_by('date', 'time').filter(active=True)
            queryset2 = Appointment.objects.filter(doctor__username=username).order_by('date', 'time')
        context = {
            'user': User.objects.get(username=username),
            'user_type': profile.user_type,
            'appointments': queryset,
            'all': queryset2,
            'select': select
        }
        return render(request, 'user_appointments.html', context)


class PatientTreatmentView(View):
    def get(self, request, username, pk):
        appointment = Appointment.objects.get(pk=pk)
        if not request.user == appointment.doctor:
            messages.error(request, f'Current user is not the correct doctor!')
            return redirect('hospital-home')
        form = TreatmentForm()
        return render(request, 'treatment.html', {'form': form})

    def post(self, request, username, pk):
        form = TreatmentForm(request.POST)
        if form.is_valid():
            treatment = form.save()
            appointment = Appointment.objects.get(pk=pk)
            appointment.active = False
            appointment.save()
            illness = Illness(name=form.cleaned_data.get('diagnosis'), type=appointment.type)
            illness.save()
            record = MedicalHistoryRecord(treatment=treatment, patient= appointment.patient,
                                          illness=illness)
            record.save()
            form.save()
            messages.success(request, f'Treatment Applied!')
            return redirect('list-appointment', username, 'active')
        return render(request, 'treatment.html', {'form': form})
