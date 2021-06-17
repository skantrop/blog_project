from datetime import datetime
from django import forms
from django.http import request

from .models import Post, Comment


class CreatePostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(initial=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), required=False)

    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'video', 'category', 'tags']


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'video', 'category', 'tags']


class CommentForm(forms.ModelForm):
    pub_date = forms.DateTimeField(initial=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), required=False)

    class Meta:
        model = Comment
        fields = ['description']