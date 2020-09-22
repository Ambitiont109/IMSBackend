from django.contrib import admin
from .models import Child, SiblingGroup, Contact, AuthPerson
# Register your models here.
admin.site.register(Child)
admin.site.register(SiblingGroup)
admin.site.register(Contact)
admin.site.register(AuthPerson)

