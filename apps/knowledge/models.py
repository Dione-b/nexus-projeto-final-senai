from pathlib import Path

from django.conf import settings
from django.db import models
from pgvector.django import HnswIndex, VectorField


def caminho_do_arquivo(_instancia, nome: str) -> str:
    """Guarda o arquivo dentro de MEDIA_ROOT (pasta ``documents/``)."""
    return Path(nome).name


class Document(models.Model):
    """Documento da base de conhecimento cadastrado pelo administrador."""

    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        INDEXADO = "indexado", "Indexado"
        ERRO = "erro", "Erro na indexação"

    title = models.CharField(
        "título",
        max_length=255,
        blank=True,
        help_text="Opcional: preenchido com o nome do arquivo quando vazio.",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
        verbose_name="status",
    )
    # Motivo do status "erro" (issue #7): registra o que falhou na
    # indexação para observabilidade (RNF — logs e erros).
    error_message = models.TextField(
        "mensagem de erro",
        blank=True,
        default="",
    )
    created_at = models.DateTimeField("criado em", auto_now_add=True)

    # Campos de upload (issue #5 - US10).
    arquivo = models.FileField(
        "arquivo",
        upload_to=caminho_do_arquivo,
        default="",
        help_text="Arquivo armazenado em MEDIA_ROOT/documents.",
    )
    enviado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documentos_enviados",
        verbose_name="enviado por",
    )
    atualizado_em = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        verbose_name = "documento"
        verbose_name_plural = "documentos"
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        """Preenche o título com o nome do arquivo quando não informado."""
        if not self.title:
            self.title = Path(self.arquivo.name).stem or "Sem título"
        super().save(*args, **kwargs)

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
