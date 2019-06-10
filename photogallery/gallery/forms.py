from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from gallery.models import Photo, Comment, Like


class AddPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['path', 'description', 'tags']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {'content': forms.TextInput(attrs={'size': 55})}


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# class LikeForm(forms.ModelForm):
#     class Meta:
#         model = Like
#         widgets = {'like_user': forms.HiddenInput,
#                    'like_photo': forms.HiddenInput}