from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models import ForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='users', blank=True, default= 'profile_images/default.png')

    def __str__(self):
        return self.get_full_name()
