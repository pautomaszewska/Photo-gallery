"""photogallery URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.conf.urls import url
from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from .settings import MEDIA_ROOT, MEDIA_URL

from gallery.views import AddPhoto, Photos, PhotoDetails, AddLike

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', Photos.as_view(), name='/'),
    url(r'^add-photo', AddPhoto.as_view(), name="add-photo"),
    url(r'^photo/(?P<photo_id>(\d)+)', PhotoDetails.as_view(), name="photo"),
    url(r'^like/(?P<photo_id>(\d)+)', AddLike.as_view(), name="like"),

    url(r'^login', auth_views.LoginView.as_view(), name="login"),
    url(r'^logout/', auth_views.LogoutView.as_view(), name="logout"),
    url(r'^password_reset/', auth_views.PasswordChangeView.as_view(), name='password_reset'),

] + static(MEDIA_URL, document_root=MEDIA_ROOT)