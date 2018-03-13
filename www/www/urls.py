"""www URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import account
from account import urls as account_urls
from website import urls as website_urls
from blog import urls as blog_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^account/', include(account_urls)),
    url(r'^blog/', include(blog_urls)),
    url(r'^', include(website_urls)),
                  url(
        r'^account/reset/confirm/(?P<uidb64>[^/]+)/(?P<token>[^/]+)/$',
        account.views.PasswordResetConfirm.as_view(), name='password_reset_confirm'),
] +  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + \
  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
