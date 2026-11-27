"""Configuração do app telegram (canal de atendimento via Telegram)."""

from django.apps import AppConfig


class TelegramConfig(AppConfig):
    """Configuração padrão do app de canal de atendimento via Telegram."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.telegram"
