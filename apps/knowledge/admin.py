"""Registros de modelos no Django Admin do app knowledge."""

from django.contrib import admin

from apps.accounts.admin_site import nexus_admin_site

from .models import Chunk, Document


class ChunkInline(admin.TabularInline):
    """Trechos do documento; o embedding vetorial fica oculto."""

    model = Chunk
    extra = 0
    exclude = ("embedding",)
    ordering = ("id",)


@admin.register(Document, site=nexus_admin_site)
class DocumentAdmin(admin.ModelAdmin):
    """Documentos da base de conhecimento (RN01 — só administradores)."""

    list_display = ("title", "status", "chunk_count", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("title",)
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    inlines = (ChunkInline,)

    @admin.display(description="chunks")
    def chunk_count(self, obj):
        return obj.chunks.count()


@admin.register(Chunk, site=nexus_admin_site)
class ChunkAdmin(admin.ModelAdmin):
    """Trechos indexados; o embedding cru nunca aparece na tela."""

    list_display = ("id", "document", "short_content")
    list_filter = ("document__status",)
    search_fields = ("content", "document__title")
    exclude = ("embedding",)

    @admin.display(description="conteúdo")
    def short_content(self, obj):
        return obj.content[:80]
