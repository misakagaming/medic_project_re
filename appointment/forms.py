from django.contrib.auth.models import User
from history.models import IllnessType, Treatment, TYPE_CHOICES
from .models import TIME_CHOICES, Appointment
from django import forms


class AppointmentForm(forms.ModelForm):
    queryset = User.objects.filter(profile__user_type='b')
    doctor = forms.ModelChoiceField(queryset=queryset)
    time = forms.ChoiceField(choices=TIME_CHOICES)
    date = forms.DateField(input_formats=['%d/%m/%Y'], help_text='Format: DD/MM/YYYY')
    type = forms.ModelChoiceField(queryset=IllnessType.objects.all())

    class Meta:
        model = Appointment
        fields = ['doctor', 'type', 'date', 'time']


class TreatmentForm(forms.ModelForm):
    diagnosis = forms.CharField()
    type = forms.ChoiceField(choices=TYPE_CHOICES)
    dose = forms.IntegerField()
    duration = forms.IntegerField()

    class Meta:
        model = Treatment
        fields = ['diagnosis', 'name', 'type', 'dose', 'hospital_name', 'duration']
