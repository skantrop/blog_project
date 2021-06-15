from datetime import datetime

from django import forms

from blog.models import Post


class CreatePostForm(forms.ModelForm):
    pub_date = forms.DateTimeField(initial=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), required=False)

    class Meta:
        model = Post
        fields = '__all__'


class UpdatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'category', 'tags']


