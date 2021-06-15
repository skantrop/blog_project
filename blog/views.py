from django.shortcuts import render
from .models import Category , Post


# def index(request):
#     categories = Category.objects.all()
#     return render(request, 'blog/index.html', context={'categories': categories})

def index(request):
    posts = Post.objects.all()
    return render(request, 'blog/index.html', context={'posts': posts})
