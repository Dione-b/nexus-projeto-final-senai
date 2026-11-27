from django.db import models


class Retrieval(models.Model):
    """Registro de auditoria de um trecho recuperado para uma mensagem (RN09)."""

    message = models.ForeignKey(
        "conversations.Message",
        on_delete=models.CASCADE,
        related_name="retrievals",
        verbose_name="mensagem",
    )
    chunk = models.ForeignKey(
        "knowledge.Chunk",
        on_delete=models.CASCADE,
        related_name="retrievals",
        verbose_name="trecho",
    )
    similarity = models.FloatField("similaridade", default=0.0)
    created_at = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        verbose_name = "recuperação"
        verbose_name_plural = "recuperações"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Mensagem #{self.message_id} ← Chunk #{self.chunk_id} ({self.similarity:.3f})"
