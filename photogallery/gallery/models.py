from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User


# Create your models here.

class Photo(models.Model):
    path = models.ImageField(upload_to='media/')
    creation_date = models.DateTimeField(default=now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=264)


class Comment(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(default=now())
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)

