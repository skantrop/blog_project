from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from .forms import CreatePostForm, UpdatePostForm
from .models import Post


class IndexPageView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'blog/index.html', {'posts': posts})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


class PostCreateView(CreateView):
    queryset = Post.objects.all()
    template_name = 'blog/create_post_form.html'
    form_class = CreatePostForm


class EditPostView(UpdateView):
    queryset = Post.objects.all()
    template_name = 'blog/edit_post_form.html'
    form_class = UpdatePostForm


class DeletePostView(DeleteView):
    queryset = Post.objects.all()
    template_name = 'blog/delete_post.html'

    def get_success_url(self):
        return reverse('index-page')


