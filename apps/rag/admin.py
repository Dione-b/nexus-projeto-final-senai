"""Registros de modelos no Django Admin do app rag."""

from django.contrib import admin

from apps.accounts.admin_site import nexus_admin_site

from .models import Retrieval


@admin.register(Retrieval, site=nexus_admin_site)
class RetrievalAdmin(admin.ModelAdmin):
    """Auditoria das respostas: quais chunks sustentaram cada mensagem (RN09)."""

    list_display = ("id", "message", "chunk", "similarity", "created_at")
    list_filter = ("created_at",)
    search_fields = ("message__content", "chunk__content", "chunk__document__title")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
