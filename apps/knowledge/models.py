"""Modelos do app knowledge (base de conhecimento).

Implementação mínima para a issue #7 (gerar embeddings dos chunks):
`Document` com estado de indexação e `Chunk` com o vetor pgvector.
A modelagem completa da seção 8 do README será concluída na issue #3.
"""

from django.conf import settings
from django.db import models
from pgvector.django import VectorField


class Document(models.Model):
    """Documento da base de conhecimento e seu estado de indexação."""

    STATUS_PENDING = "pendente"
    STATUS_INDEXED = "indexado"
    STATUS_ERROR = "erro"

    STATUS_CHOICES = [
        (STATUS_PENDING, "Pendente"),
        (STATUS_INDEXED, "Indexado"),
        (STATUS_ERROR, "Erro"),
    ]

    title = models.CharField("título", max_length=255)
    status = models.CharField(
        "status",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )
    error_message = models.TextField(
        "mensagem de erro",
        blank=True,
        default="",
    )
    created_at = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        verbose_name = "documento"
        verbose_name_plural = "documentos"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return self.title


class Chunk(models.Model):
    """Trecho de um documento, com o vetor (embedding) para busca semântica.

    O campo `embedding` usa pgvector (extensão habilitada na migração
    0001_enable_pgvector). Fica nulo até a geração de embeddings (issue #7);
    o serviço em `apps/rag/embeddings.py` garante que nenhum chunk de um
    documento indexado permaneça sem vetor.
    """

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="chunks",
        verbose_name="documento",
    )
    content = models.TextField("conteúdo")
    embedding = VectorField(
        "embedding",
        dimensions=settings.EMBEDDING_DIMENSIONS,
        null=True,
    )

    class Meta:
        verbose_name = "trecho"
        verbose_name_plural = "trechos"
        ordering = ["id"]

    def __str__(self) -> str:
        return f"{self.document.title} [{self.pk}]"
