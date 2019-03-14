from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic.edit import FormView, CreateView
from django.views import View
from django.views.generic.edit import FormView

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, authenticate, PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin

from gallery.models import Photo, User
from gallery.forms import AddPhotoForm


class AddPhoto(View):

    def get(self, request):
        form = AddPhotoForm()
        return render(request, 'add_photo.html', {'form': form})

    def post(self, request):
        form = AddPhotoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect(reverse('main'))


class Photos(View):

    def get(self, request):
        photos = Photo.objects.all()
        return render(request, 'photos.html', {'photos': photos})


        



