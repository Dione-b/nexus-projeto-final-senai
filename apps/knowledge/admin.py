"""Registros de modelos no Django Admin do app knowledge."""

from django.contrib import admin

from .models import Document


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    """Gestão dos documentos da base de conhecimento no admin."""

    list_display = ("titulo", "status", "enviado_por", "criado_em")
    list_filter = ("status", "criado_em")
    search_fields = ("titulo",)
    readonly_fields = ("criado_em", "atualizado_em", "enviado_por")
