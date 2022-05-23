from django import forms
from .models import Author, Post


class PostForm(forms.ModelForm):
    """ Создание формы для создания поста """

    class Meta:

        model = Post
        fields = ['title', 'content', 'cat', 'tags']


class ForumUserForm(forms.ModelForm):

    class Meta:

        model = Author
        fields = ['fullname', 'bio', 'profile_pic']
        exclude = ['user']