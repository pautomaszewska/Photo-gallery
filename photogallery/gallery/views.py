from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, CreateView
from django.views import View
from django.views.generic.edit import FormView

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, authenticate, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin

from gallery.models import Photo, User, Comment, Like
from gallery.forms import AddPhotoForm, CommentForm


class AddPhoto(View):

    def get(self, request):
        form = AddPhotoForm()
        like = Like.objects.get(like_photo__user=self.request.user)
        return render(request, 'add_photo.html', {'form': form, 'like': like})

    def post(self, request):
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = Photo(user=self.request.user,
                          path=form.cleaned_data.get('path'),
                          description=form.cleaned_data.get('description'))
            photo.save()

            return HttpResponseRedirect(reverse('main'))


class Photos(LoginRequiredMixin, View):

    def get(self, request):
        photos = Photo.objects.all().order_by('creation_date')
        return render(request, 'photos.html', {'photos': photos})


class PhotoDetails(View):

    def get(self, request, photo_id):
        form = CommentForm()
        photo = Photo.objects.get(pk=photo_id)
        comments = Comment.objects.filter(photo_id=photo_id)

        return render(request, 'photo.html', {'photo': photo, 'comments': comments, 'form': form})

    def post(self, request, photo_id):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(comment_user=self.request.user,
                              photo_id=photo_id,
                              content=form.cleaned_data.get('content'))
            comment.save()

            return HttpResponseRedirect(reverse('photo', args=[photo_id]))


class AddLike(View):

    def post(self, request, photo_id):
        photo = Photo.objects.get(pk=photo_id)
        like = Like(like_user=request.user,
                    like_photo=photo)
        like.save()

        return HttpResponseRedirect(reverse('main'))

