from django.contrib.auth.models import User
from django.db import models

from website import jalali


class Post(models.Model):
    title = models.CharField(max_length=256, null=True, blank=True)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    tags = models.ManyToManyField(to='Tag', related_name='tagged_items', null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    anon = models.BooleanField(verbose_name='ناشناس', default=False)

    def get_likes_count(self):
        return UserLikesPost.objects.filter(post=self).count()

    def get_dislikes_count(self):
        return UserDislikesPost.objects.filter(post=self).count()

    def get_comments_count(self):
        return Comment.objects.filter(post=self).count()

    def get_time(self):
        return jalali.Gregorian(str(self.time).split(' ')[0]).persian_string()


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.CharField(max_length=1024)
    time = models.DateTimeField(auto_now_add=True)


class UserLikesPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class UserDislikesPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class ReportPost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)


class Tag(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

