"""Configuração do app accounts (usuários e permissões)."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configuração padrão do app de usuários e permissões."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
