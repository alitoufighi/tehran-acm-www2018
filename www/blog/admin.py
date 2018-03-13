from django.contrib import admin
from blog.models import *

admin.site.register([Post, Comment, UserLikesPost, UserDislikesPost, ReportPost, Tag])
