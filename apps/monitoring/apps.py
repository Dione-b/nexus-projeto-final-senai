"""Configuração do app monitoring (logs, métricas e monitoramento)."""

from django.apps import AppConfig


class MonitoringConfig(AppConfig):
    """Configuração padrão do app de logs, métricas e monitoramento."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.monitoring"
