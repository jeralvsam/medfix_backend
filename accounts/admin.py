from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("role",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Extra Info", {"fields": ("role",)}),
    )

    list_display = ("username", "email", "role", "is_staff", "is_active")

admin.site.register(User, CustomUserAdmin)