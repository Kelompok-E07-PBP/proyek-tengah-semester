from django import forms
from forum.models import Post,Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['topic', 'description']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['description']