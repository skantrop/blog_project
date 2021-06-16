from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView

from .forms import CreatePostForm, UpdatePostForm, CommentForm
from .models import Post, Comment


class IndexPageView(View):
    def get(self, request):
        posts = Post.objects.all()
        return render(request, 'blog/index.html', {'posts': posts})


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'


def post_detail(request, id, slug):
    post = get_object_or_404(Post, id=id, slug=slug)
    comments = Comment.objects.filter(post=post).order('-id')
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        is_liked = True

    if request.method == 'POST':
        comment_form = CommentForm(request.POST or None)
        if comment_form.is_valid():
            comment_form.save()
        else:
            comment_form=CommentForm()

    context = {
        'post': post,
        'is_liked': is_liked,
        'total_likes': post.total_likes(),
        'comments': comments,
        'comment_form': comment_form,
     }
    return render(request, 'blog/post_detail.html', context)


def like_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    is_liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        is_liked = False
    else:
        post.likes.add(request.user)
        is_liked = True
    return HttpResponseRedirect(post.get_absolute_url())


class PostCreateView(LoginRequiredMixin, CreateView):
    queryset = Post.objects.all()
    template_name = 'blog/create_post_form.html'
    form_class = CreatePostForm


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


class DeletePostView(DeleteView):
    queryset = Post.objects.all()
    template_name = 'blog/delete_post.html'

    def get_success_url(self):
        return reverse('index-page')



