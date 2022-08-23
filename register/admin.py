from django.contrib import admin
from .models import User , Group

class UserAdmin (admin.ModelAdmin):
    list_display = ("email", "username", "is_verified", "last_generated", "auth_provider")

admin.site.register(User, UserAdmin)
admin.site.register(Group)
