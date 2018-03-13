from django.conf.urls import url
from blog import views

app_name = 'blog'
urlpatterns = [
    url(r'^post/(?P<post_id>\d+)$', views.show_post, name='show_post'),
    url(r'^add-post$', views.AddPostView.as_view(), name='add_post'),
    url(r'^tag/add/(?P<post_id>\d+)$', views.AddTagView.as_view(), name='add_tag'),
    url(r'^like/(?P<post_id>\d+)$', views.LikeView.as_view(), name='like'),
    url(r'^dislike/(?P<post_id>\d+)$', views.DislikeView.as_view(), name='dislike'),
    url(r'^delete/(?P<post_id>\d+)$', views.DeleteView.as_view(), name='delete'),
    url(r'^report/(?P<post_id>\d+)$', views.ReportView.as_view(), name='report'),
]
