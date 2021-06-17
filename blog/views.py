from urllib.request import Request

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from .forms import CreatePostForm, UpdatePostForm, CommentForm
from .models import Post, Comment


class IndexPageView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'blog/index.html', {'posts': posts})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    form = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['comments'] = Comment.objects.all()
        context['form'] = self.form
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.request = Request.objects.get(pk=self.object.pk)
        form.instance.created = timezone.now
        form.save()


class PostCreateView(LoginRequiredMixin, CreateView):
    queryset = Post.objects.all()
    template_name = 'blog/create_post_form.html'
    form_class = CreatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class EditPostView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    queryset = Post.objects.all()
    template_name = 'blog/edit_post_form.html'
    form_class = UpdatePostForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    queryset = Post.objects.all()
    template_name = 'blog/delete_post.html'

    def get_success_url(self):
        return reverse('index-page')

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class CommentView(DetailView):
    model = Comment
    template_name = 'blog/post_detail.html'
    form_class = CommentForm


class SearchResultsView(View):
    def get(self, request):
        q = request.GET.get('q', '')
        if q:
            posts = Post.objects.filter(Q(title__icontains=q)|
                                       Q(text__icontains=q))
        else:
            posts = Post.objects.none()
        return render(request, 'blog/index.html', {'posts': posts})


