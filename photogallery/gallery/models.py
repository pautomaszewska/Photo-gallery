from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from PIL import Image


# Create your models here.

class Photo(models.Model):
    path = models.ImageField(upload_to='media/')
    creation_date = models.DateTimeField(default=now())
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(max_length=264)

    # def save(self):
    #     super().save()
    #
    #     img = Image.open(self.path.path)
    #     if img.height > 300 or img.width > 300:
    #         new_img = (300, 300)
    #         img.thumbnail(new_img)
    #         img.save(self.path.path)


class Comment(models.Model):
    comment_user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_date = models.DateTimeField(default=now())
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    content = models.CharField(max_length=4000, verbose_name='')


class Like(models.Model):
    like_user = models.ForeignKey(User, on_delete=models.CASCADE)
    like_photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
