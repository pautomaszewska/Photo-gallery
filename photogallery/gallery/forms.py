from django import forms
from gallery.models import Photo, Comment

class AddPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['path', 'description', 'user']