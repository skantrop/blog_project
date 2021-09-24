from datetime import timedelta
from urllib.request import Request

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import request
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView
from django.core.paginator import Paginator
from .forms import CreatePostForm, UpdatePostForm, CommentForm, UpdateCommentForm
from .models import Post, Comment, Category, Tag


class IndexPageView(View):
    context_object_name = 'posts'

    def get(self, request):
        posts = Post.objects.all()
        categories = Category.objects.all()
        return render(request, 'blog/index.html', {'posts': posts, 'categories': categories})

    def get_category(self, request, url):
        posts = Post.objects.all(category__url=url)
        categories = Category.objects.all()
        return render(request, 'blog/index.html', {'posts': posts, 'categories': categories})

    def det_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = self.request.GET.get('q')
        if filter:
            start_date = timezone.now() - timedelta(days=1)
            context['posts'] = Post.objects.filter(created__gte=start_date)
        return context


class PostDetailView(DetailView, LoginRequiredMixin):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    form = CommentForm
    pk_url_kwarg = "pk"

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['comments'] = Comment.objects.filter(post=kwargs.get("object"))
        context['form'] = self.form
        context['genres'] = Category.objects.all()
        context['tags'] = Tag.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST)
        if form.is_valid():
            description = form.cleaned_data['description']
            author = self.request.user
            post = self.get_object()
            form.save(description, author, post)
        else:
            form = CommentForm
        return redirect(self.request.get_full_path())


class UpdateCommentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    queryset = Comment.objects.all()
    template_name = 'blog/edit_comment.html'
    form_class = UpdateCommentForm

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def get_success_url(self):
        post = self.get_object()
        return reverse('post-detail', args=(self.object.post.id, ))


class DeleteCommentView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    queryset = Comment.objects.all()
    template_name = 'blog/delete_comment.html'

    def get_success_url(self):
        post = self.get_object()
        return reverse('post-detail', args=(self.object.post.id, ))

    def test_func(self):
        comment = self.get_object()
        if self.request.user == comment.author:
            return True
        return False


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


class SearchResultsView(View):
    def get(self, request):
        q = request.GET.get('q', '')
        if q:
            posts = Post.objects.filter(Q(title__icontains=q)|
                                       Q(text__icontains=q))
        else:
            posts = Post.objects.none()
        return render(request, 'blog/index.html', {'posts': posts})



