from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


TYPE_CHOICES = (('a', 'Prescription'),
           ('b', 'Hospital Stay'))


# Create your models here.
class IllnessType(models.Model):
    type = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Illness Type"
        verbose_name_plural = "Illness Types"

    def __str__(self):
        return self.type


class Illness(models.Model):
    name = models.CharField(max_length=100)
    type = models.ForeignKey(IllnessType, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Illnesses"

    def __str__(self):
        return self.name


class Treatment(models.Model):
    name = models.CharField(max_length=100)
    type = models.CharField(max_length=1, choices=TYPE_CHOICES, default='a')
    dose = models.FloatField(default=0)
    hospital_name = models.CharField(max_length=100)
    duration = models.IntegerField(default=0)

    def __str__(self):
        if self.type == 'a':
            return f'{self.name}, {self.dose} mg, {self.duration} week(s)'
        elif self.type == 'b':
            return f'{self.name}, stayed at {self.hospital_name}, {self.duration} week(s)'
        else:
            return 'what'


class MedicalHistoryRecord(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    illness = models.ForeignKey(Illness, on_delete=models.CASCADE)
    treatment = models.OneToOneField(Treatment, on_delete=models.CASCADE)
    date_recorded = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Medical History Record"
        verbose_name_plural = "Medical History Records"
