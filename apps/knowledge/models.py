"""Modelos do app knowledge (base de conhecimento).

Corresponde à US10 (cadastrar documentos). A extração, chunking e indexação
vetorial dos documentos são tratadas nas issues seguintes do Sprint 02.
"""

from pathlib import Path

from django.conf import settings
from django.db import models
from django.utils import timezone


def caminho_do_arquivo(_instancia, nome: str) -> str:
    """Guarda o arquivo dentro de MEDIA_ROOT (pasta ``documents/``)."""
    return Path(nome).name


class Document(models.Model):
    """Documento enviado por um administrador à base de conhecimento."""

    class Status(models.TextChoices):
        PENDENTE = "pendente", "Pendente"
        INDEXADO = "indexado", "Indexado"
        ERRO = "erro", "Erro"

    titulo = models.CharField(
        "título",
        max_length=200,
        blank=True,
        help_text="Opcional: preenchido com o nome do arquivo quando vazio.",
    )
    arquivo = models.FileField(
        "arquivo",
        upload_to=caminho_do_arquivo,
        help_text="Arquivo armazenado em MEDIA_ROOT/documents.",
    )
    status = models.CharField(
        "status",
        max_length=20,
        choices=Status.choices,
        default=Status.PENDENTE,
    )
    enviado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documentos_enviados",
        verbose_name="enviado por",
    )
    criado_em = models.DateTimeField("criado em", default=timezone.now)
    atualizado_em = models.DateTimeField("atualizado em", auto_now=True)

    class Meta:
        ordering = ["-criado_em"]
        verbose_name = "documento"
        verbose_name_plural = "documentos"

    def save(self, *args, **kwargs):
        """Preenche o título com o nome do arquivo quando não informado."""
        if not self.titulo:
            self.titulo = Path(self.arquivo.name).stem or "Sem título"
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.titulo
