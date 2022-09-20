from django.db import models
from django import forms
from django.contrib.auth.models import User
from PIL import Image

# Create your models here.
CHOICES = (('a', 'Patient'),
           ('b', 'Doctor'))


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='blank-profile-picture.png', upload_to='profile_pics')
    user_type = models.CharField(max_length=1, choices=CHOICES, default='a')

    def __str__(self):
        return f'Profile of {self.user.username}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)
