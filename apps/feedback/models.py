from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Feedback(models.Model):
    """Avaliação do cliente sobre uma resposta do assistente (US05/US23)."""

    message = models.ForeignKey(
        "conversations.Message",
        on_delete=models.CASCADE,
        related_name="feedbacks",
        verbose_name="mensagem",
    )
    rating = models.PositiveSmallIntegerField(
        "nota",
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Nota de 1 a 5.",
    )
    comment = models.TextField("comentário", blank=True)

    class Meta:
        verbose_name = "avaliação"
        verbose_name_plural = "avaliações"

    def __str__(self):
        return f"Avaliação {self.rating} na mensagem #{self.message_id}"
