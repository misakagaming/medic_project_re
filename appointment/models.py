from django.db import models
from history.models import IllnessType
from users.models import Profile
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
TIME_CHOICES = (('a', '9:00 - 9:20'),
                ('b', '9:30 - 9:50'),
                ('c', '10:00 - 10:20'),
                ('d', '10:30 - 10:50'),
                ('e', '11:00 - 11:20'),
                ('f', '11:30 - 11:50'),
                ('g', '12:00 - 12:20'),
                ('h', '13:00 - 13:20'),
                ('i', '13:30 - 13:50'),
                ('j', '14:00 - 14:20'),
                ('k', '14:30 - 14:50'),
                ('l', '15:00 - 15:20'),
                ('m', '15:30 - 15:50'),
                ('n', '16:00 - 16:20'),
                ('o', '16:30 - 16:50'),
                ('p', '17:00 - 17:20'))


class Appointment(models.Model):
    patient = models.ForeignKey(User, related_name="patient", on_delete=models.CASCADE)
    type = models.ForeignKey(IllnessType, null=True, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, null=True, related_name="doctor", on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    time = models.CharField(max_length=1, choices=TIME_CHOICES)
    active = models.BooleanField(default=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=['patient', 'time', 'date'], name='patient appointment time'),
                       models.UniqueConstraint(fields=['doctor', 'time', 'date'], name='doctor appointment time')]


