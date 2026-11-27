from django.conf import settings
from django.db import models
from pgvector.django import HnswIndex, VectorField


class Document(models.Model):
    """Documento da base de conhecimento cadastrado pelo administrador."""

    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        INDEXADO = "indexado", "Indexado"
        ERRO = "erro", "Erro na indexação"

    title = models.CharField("título", max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
        verbose_name="status",
    )
    created_at = models.DateTimeField("criado em", auto_now_add=True)

    class Meta:
        verbose_name = "documento"
        verbose_name_plural = "documentos"
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Chunk(models.Model):
    """Trecho de um documento com seu vetor de embedding (pgvector)."""

    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name="chunks",
        verbose_name="documento",
    )
    content = models.TextField("conteúdo")
    # Vetor denso; dimensão definida por EMBEDDING_DIMENSIONS no settings.
    embedding = VectorField(
        dimensions=settings.EMBEDDING_DIMENSIONS,
        null=True,
        blank=True,
        verbose_name="embedding",
    )

    class Meta:
        verbose_name = "trecho"
        verbose_name_plural = "trechos"
        # Busca vetorial aproximada (issue #3): indice HNSW por similaridade
        # de cosseno sobre o embedding, usado pelo recuperador do RAG.
        indexes = [
            HnswIndex(
                name="knowledge_chunk_embedding_hnsw",
                fields=["embedding"],
                opclasses=["vector_cosine_ops"],
                m=16,
                ef_construction=64,
            ),
        ]

    def __str__(self):
        return f"Chunk #{self.pk} de {self.document.title}"
