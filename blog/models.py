from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=70)
    slug = models.SlugField(max_length=70, primary_key=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(max_length=30, primary_key=True)

    def __str__(self):
        return self.title


class Post(models.Model):
    STATUS_CHOICES = (
        ('published', 'Опубликован'),
        ('draft', 'Черновик')
    )
    title = models.CharField(max_length=100)
    text = models.TextField()
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='posts')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')
    pub_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='posts', blank=True, null=True)
    video = models.FileField(upload_to='media', blank=True)
    category = models.ForeignKey(Category,
                                 on_delete=models.CASCADE,
                                 related_name='posts')
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})





