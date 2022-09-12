from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class IllnessType(models.Model):
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.type


class Illness(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(IllnessType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Treatment(models.Model):
    name = models.CharField(max_length=100)
    is_prescription = models.BooleanField(default=False)
    is_hospital_stay = models.BooleanField(default=False)
    dose = models.FloatField(default=0)
    hospital_name = models.CharField(max_length=100)
    duration = models.IntegerField(default=0)

    def __str__(self):
        if self.is_prescription:
            return f'{self.name}, {self.dose} mg, {self.duration} week(s)'
        elif self.is_hospital_stay:
            return f'{self.name}, stayed at {self.hospital_name}, {self.duration} week(s)'
        else:
            return 'what'


class MedicalHistoryRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    illness = models.ForeignKey(Illness, on_delete=models.CASCADE)
    treatment = models.OneToOneField(Treatment, on_delete=models.CASCADE)
    date_recorded = models.DateTimeField(default=timezone.now)
