from django.contrib import admin

from .models import User


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'price', 'active', 'password', 'is_admin')


admin.site.register(User, CustomUserAdmin)


