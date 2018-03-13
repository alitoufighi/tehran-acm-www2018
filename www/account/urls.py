from django.conf.urls import url

from account import views

app_name = 'account'
urlpatterns = [
    url(r'^register$', views.Register.as_view(), name='register'),
    url(r'^login$', views.Login.as_view(), name='login'),
    url(r'^reset$', views.PasswordReset.as_view(), name='reset'),
    url(r'^reset/done$', views.PasswordResetDone.as_view(),
        name='reset_done'),
    url(r'^profile/(?P<user_id>\d+)$', views.profile, name='profile'),
    url(r'^my_profile/$', views.my_profile, name='my_profile'),
    url(r'^notifications$', views.Notifications.as_view(), name='notifications'),
    url(r'^logout', views.my_logout, name='logout'),
    url(r'^notifications/seen/(?P<id>\d+)$', views.SeenNotification.as_view(), name='seen_notif'),
    url(r'^user/change_permission$', views.ChangePermissionList.as_view(), name='change_perm_list'),
    url(r'^user/activate/(?P<uidb64>[^/]+)/(?P<token>[^/]+)$', views.ActivateUser.as_view(), name='activate'),
    url(r'^user/change_permission/(?P<id>[^/]+)/(?P<action>[^/]+)$', views.ChangePermission.as_view(),
        name='change_perm')
]
