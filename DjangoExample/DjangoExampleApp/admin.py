from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Role, Profile, News


admin.site.register(Role)
admin.site.register(Profile)
admin.site.register(News)

admin.site.unregister(Group)
