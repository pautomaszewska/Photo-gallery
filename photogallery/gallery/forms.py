from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from gallery.models import Photo, Comment, Like


def validate_email_unique(value):
    exists = User.objects.filter(email=value)
    if exists:
        raise ValidationError("Email address already exists")


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
    email = forms.EmailField(validators=[validate_email_unique])

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UpdatePhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['description', 'tags']
