from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from.forms import AppointmentForm
from .models import Appointment
from users.models import Profile
from django.contrib.auth.models import User
# Create your views here.


class MakeAppointmentView(View):
    def get(self, request):
        form = AppointmentForm()
        return render(request, 'create_appointment.html', {'form': form})

    def post(self, request):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            if not Appointment.objects.filter(time=form.cleaned_data.get('time'), patient=request.user):
                appointment = form.save(commit=False)
                appointment.patient = request.user
                appointment.save()
                messages.success(request, f'Appointment created!')
                return redirect('create-appointment')
            messages.error(request, f'An appointment for this time and user already exists!')
        return render(request, 'create_appointment.html', {'form': form})


class ListAppointmentsView(View):
    def get(self, request, username):
        profile = Profile.objects.get(user__username=username)
        if profile.user_type == 'a':
            queryset = Appointment.objects.filter(patient__username=username).order_by('time')
        else:
            queryset = Appointment.objects.filter(doctor__username=username).order_by('time')
        context = {
            'user': User.objects.get(username=username),
            'user_type': profile.user_type,
            'appointments': queryset
        }
        return render(request, 'user_appointments.html', context)
