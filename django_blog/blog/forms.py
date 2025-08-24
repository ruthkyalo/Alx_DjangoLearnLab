#user creation form
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post
from .models import Comment
from taggit.forms import TagWidget 

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# blog post form for CRUD
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']  # include tags field
        widgets = {
            'tags': TagWidget(),  # ensures proper tag input in form
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']        