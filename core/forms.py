from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    """ Создание формы для создания поста """

    class Meta:

        model = Post
        fields = ["title", "content", "cat", "tags"]