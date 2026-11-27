"""Configuração do app knowledge (base de conhecimento)."""

from django.apps import AppConfig


class KnowledgeConfig(AppConfig):
    """Configuração padrão do app de base de conhecimento."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.knowledge"
