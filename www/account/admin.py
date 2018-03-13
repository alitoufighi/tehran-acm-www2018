from django.contrib import admin

# Register your models here.
from account.models import StudentField, UserProfile, Notification

admin.site.register(StudentField)
admin.site.register(UserProfile)
admin.site.register(Notification)
