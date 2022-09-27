from django.contrib.auth.models import User
from history.models import IllnessType
from users.models import Profile
from .models import TIME_CHOICES, Appointment
from django import forms


class AppointmentForm(forms.ModelForm):
    queryset = User.objects.filter(profile__user_type='b')
    doctor = forms.ModelChoiceField(queryset=queryset)
    time = forms.ChoiceField(choices=TIME_CHOICES)
    type = forms.ModelChoiceField(queryset=IllnessType.objects.all())

    class Meta:
        model = Appointment
        fields = ['doctor', 'type', 'time']
