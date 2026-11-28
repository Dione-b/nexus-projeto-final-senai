from django.conf import settings
from django.db import models


class Conversation(models.Model):
    """Conversa de um usuário em um canal (Web ou Telegram). RN05."""

    class Channel(models.TextChoices):
        WEB = "web", "Web"
        TELEGRAM = "telegram", "Telegram"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversations",
        verbose_name="usuário",
    )
    channel = models.CharField(
        max_length=20,
        choices=Channel.choices,
        default=Channel.WEB,
        verbose_name="canal",
    )
    created_at = models.DateTimeField("criada em", auto_now_add=True)

    class Meta:
        verbose_name = "conversa"
        verbose_name_plural = "conversas"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Conversa #{self.pk} ({self.get_channel_display()})"


class Message(models.Model):
    """Mensagem de uma conversa, com papel de quem fala."""

    class Role(models.TextChoices):
        USER = "user", "Usuário"
        ASSISTANT = "assistant", "Assistente"

    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
        verbose_name="conversa",
    )
    role = models.CharField(max_length=20, choices=Role.choices, verbose_name="papel")
    content = models.TextField("conteúdo")
    created_at = models.DateTimeField("criada em", auto_now_add=True)

    class Meta:
        verbose_name = "mensagem"
        verbose_name_plural = "mensagens"
        ordering = ["created_at"]

    def __str__(self):
        return f"Mensagem #{self.pk} ({self.get_role_display()})"
