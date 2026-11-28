"""Registros de modelos no Django Admin do app knowledge."""

from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Gestão dos documentos da base de conhecimento no admin."""

    list_display = ("title", "status", "enviado_por", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title",)
    readonly_fields = ("created_at", "atualizado_em", "enviado_por")
