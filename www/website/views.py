from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

from blog.models import Post


def home(request):
    blog_posts = Post.objects.order_by('-time').all()
    return render(request, 'website/home.html', {
        'blog_posts': blog_posts
    })