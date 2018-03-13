from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.


class StudentField(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


def handle_avatar_upload_path(instance, filename):
    return 'avatars/' + str(instance.id) + '.' + filename.split('.')[-1]


class UserProfile(models.Model):
    student_id = models.IntegerField()
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    field = models.ForeignKey(StudentField, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to=handle_avatar_upload_path, default='/avatars/default.jpg')

    def __str__(self):
        return 'پروفایل ' + str(self.user)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(verbose_name=_('Notifictation text'))
    seen = models.BooleanField(verbose_name=_('Seen'))
