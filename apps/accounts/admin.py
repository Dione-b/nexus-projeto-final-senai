"""Registros de modelos no Django Admin do app accounts."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from apps.accounts.admin_site import nexus_admin_site
from apps.accounts.models import User


@admin.register(User, site=nexus_admin_site)
class UserAdmin(DjangoUserAdmin):
    """Gestão de usuários com o papel de acesso (RN01).

    O hash da senha continua protegido pelo widget padrão do Django: ele
    é mascarado e tem uma tela própria de troca de senha, nunca aparecendo
    em claro. `last_login` e `date_joined` ficam somente leitura por serem
    campos de auditoria.
    """

    fieldsets = (
        (None, {"fields": ("username", "password")}),
        ("Dados pessoais", {"fields": ("name", "email")}),
        (
            "Permissões",
            {
                "fields": (
                    "role",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Datas importantes", {"fields": ("last_login", "date_joined")}),
    )
    # O papel também é informado na criação, senão todo usuário novo
    # nasceria como cliente sem chance de escolha.
    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        ("Papel", {"fields": ("role",)}),
    )
    list_display = ("username", "name", "email", "role", "is_staff", "is_active")
    list_filter = ("role", "is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username", "name", "email")
    ordering = ("username",)
    readonly_fields = ("last_login", "date_joined")
    filter_horizontal = ("groups", "user_permissions")
