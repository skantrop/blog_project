from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(upload_to='users', blank=True, default= 'profile_images/default.png')

    def __str__(self):
        return self.get_full_name()

    def get_image_url(self):
        if self.image:
            return self.image.url
        return ''