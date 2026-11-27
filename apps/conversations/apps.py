"""Configuração do app conversations (conversas e mensagens)."""

from django.apps import AppConfig


class ConversationsConfig(AppConfig):
    """Configuração padrão do app de conversas e mensagens."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.conversations"
