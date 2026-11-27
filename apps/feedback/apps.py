"""Configuração do app feedback (avaliações das respostas)."""

from django.apps import AppConfig


class FeedbackConfig(AppConfig):
    """Configuração padrão do app de avaliações das respostas."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.feedback"
