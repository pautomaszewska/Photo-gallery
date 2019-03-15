from django import forms
from gallery.models import Photo, Comment, Like


class AddPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ['path', 'description']
        widgets = {'user': forms.HiddenInput}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {'comment_user': forms.HiddenInput,
                   'photo': forms.HiddenInput}

# class LikeForm(forms.ModelForm):
#     class Meta:
#         model = Like
#         widgets = {'like_user': forms.HiddenInput,
#                    'like_photo': forms.HiddenInput}