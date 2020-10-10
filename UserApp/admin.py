from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


# Register your models here.
admin.site.register(User, UserAdmin)


class IMSUser(User):
    class Meta:
        proxy = True


admin.site.register(IMSUser)
