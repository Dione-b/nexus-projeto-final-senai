"""Registros de modelos no Django Admin do app conversations."""

from django.contrib import admin

from apps.accounts.admin_site import nexus_admin_site

from .models import Conversation, Message


@admin.register(Conversation, site=nexus_admin_site)
class ConversationAdmin(admin.ModelAdmin):
    """Conversas de todos os canais, com as mensagens em linha."""

    class MessageInline(admin.TabularInline):
        model = Message
        extra = 0
        fields = ("role", "content", "created_at")
        readonly_fields = ("created_at",)
        ordering = ("created_at",)

    list_display = ("id", "user", "channel", "message_count", "created_at")
    list_filter = ("channel", "created_at")
    search_fields = ("user__name", "user__username", "user__email")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"
    inlines = (MessageInline,)

    @admin.display(description="mensagens")
    def message_count(self, obj):
        return obj.messages.count()


@admin.register(Message, site=nexus_admin_site)
class MessageAdmin(admin.ModelAdmin):
    """Mensagens de todas as conversas (RN05 — isoladas por conversa)."""

    list_display = ("id", "conversation", "role", "short_content", "created_at")
    list_filter = ("role", "conversation__channel", "created_at")
    search_fields = ("content", "conversation__user__name", "conversation__user__username")
    readonly_fields = ("created_at",)
    date_hierarchy = "created_at"

    @admin.display(description="conteúdo")
    def short_content(self, obj):
        return obj.content[:80]
