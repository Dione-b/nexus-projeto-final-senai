"""Configuração do app rag (pipeline RAG de recuperação e geração)."""

from django.apps import AppConfig


class RagConfig(AppConfig):
    """Configuração padrão do app de pipeline RAG de recuperação e geração."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.rag"
