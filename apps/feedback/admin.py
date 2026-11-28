"""Registros de modelos no Django Admin do app feedback."""

from django.contrib import admin

from apps.accounts.admin_site import nexus_admin_site

from .models import Feedback


@admin.register(Feedback, site=nexus_admin_site)
class FeedbackAdmin(admin.ModelAdmin):
    """Avaliações recebidas nas respostas (US05, US23)."""

    list_display = ("id", "message", "rating", "short_comment")
    list_filter = ("rating",)
    search_fields = ("comment", "message__content")

    @admin.display(description="comentário")
    def short_comment(self, obj):
        return obj.comment[:80] or "—"
