from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, CreateView
from django.views import View
import json
from django.views.generic.edit import FormView

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, authenticate, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin

from gallery.models import Photo, User, Comment, Like
from gallery.forms import AddPhotoForm, CommentForm, UserRegisterForm, UpdatePhotoForm


class AddPhoto(LoginRequiredMixin, View):
    def get(self, request):
        form = AddPhotoForm()
        return render(request, 'add_photo.html', {'form': form})

    def post(self, request):
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            photo = form.save(commit=False)
            photo.user = request.user
            photo.path = form.cleaned_data.get('path')
            photo.description = form.cleaned_data.get('description')
            photo.save()
            form.save_m2m()

            return redirect('/')


class Photos(View):
    def get(self, request):
        photos = Photo.objects.all().order_by('-creation_date')
        if request.user.is_authenticated:
            liked = Photo.objects.filter(like__like_user=request.user)
        else:
            liked = None

        return render(request, 'photos.html', {'photos': photos, 'liked': liked})


class PhotoDetails(LoginRequiredMixin, View):
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
    def post(self, request):
        id = request.POST.get('pk')
        photo = Photo.objects.get(pk=id)
        if not Like.objects.filter(like_user=request.user, like_photo=photo).exists():
            like = Like(like_user=request.user, like_photo=photo)
            like.save()
        like_count = photo.like_set.count()
        return HttpResponse(json.dumps({'like_count': like_count}), content_type='application/json')


class Unlike(View):
    def post(self, request):
        id = request.POST.get('pk')
        photo = Photo.objects.get(pk=id)
        like = Like.objects.get(like_user=request.user, like_photo=photo)
        like.delete()
        like_count = photo.like_set.count()
        return HttpResponse(json.dumps({'like_count': like_count}), content_type='application/json')


class RegisterView(View):
    def get(self, request):
        form = UserRegisterForm()
        return render(request, 'registration/register.html', {'form': form})

    def post(self, request):
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            return redirect('login')
        else:
            return render(request, 'registration/register.html', {'form': form})


class Profile(LoginRequiredMixin, View):
    def get(self, request, id):
        photos = Photo.objects.filter(user_id=id)
        photo_user = User.objects.get(id=id)
        return render(request, 'profile.html', {'photos': photos, 'photo_user': photo_user})


class SearchPhoto(LoginRequiredMixin, View):
    def post(self, request):
        tag = request.POST.get('tag')
        try:
            photos = Photo.objects.filter(tags__name=tag)
        except ValueError:
            photos = None
        return render(request, 'found.html', {'photos': photos})


class LikedPhotos(View):
    def get(self, request, id):
        photos = Photo.objects.filter(like__like_user_id=id)
        photo_user = User.objects.get(id=id)
        return render(request, 'liked.html', {'photos': photos, 'photo_user': photo_user})


class DeletePhoto(LoginRequiredMixin, View):
    def get(self, request, id):
        photo = Photo.objects.get(id=id)
        photo.delete()
        return redirect('/')


class UpdatePhoto(LoginRequiredMixin, View):
    def get(self, request, id):
        photo = Photo.objects.get(id=id)
        form = UpdatePhotoForm(instance=photo)
        return render(request, 'update_photo.html', {'form': form, 'photo': photo})

    def post(self, request, id):
        photo = Photo.objects.get(id=id)
        form = UpdatePhotoForm(request.POST, instance=photo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('photo', args=(photo.id,)))
