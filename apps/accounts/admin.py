"""Registros de modelos no Django Admin do app accounts."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UsuarioAdmin(UserAdmin):
    """Cadastro de usuários no admin, incluindo o papel (role)."""

    fieldsets = UserAdmin.fieldsets + (("Papel", {"fields": ("role",)}),)
    add_fieldsets = UserAdmin.add_fieldsets + (("Papel", {"fields": ("role",)}),)
    list_display = ("username", "email", "role", "is_active", "is_staff")
    list_filter = UserAdmin.list_filter + ("role",)
