"""Formulários do app knowledge (base de conhecimento)."""

from pathlib import Path

from django import forms
from django.conf import settings

from .models import Document

# Formatos do MVP (README seção 6 — US10): PDF, TXT e MD.
FORMATOS_PERMITIDOS = {
    ".pdf": {"application/pdf"},
    ".txt": {"text/plain", "application/octet-stream"},
    ".md": {"text/markdown", "text/plain", "text/x-markdown", "application/octet-stream"},
}

EXTENSOES_ACEITAS = "PDF, TXT e MD"


class DocumentUploadForm(forms.ModelForm):
    """Valida tipo e tamanho do arquivo antes de gravar o documento."""

    arquivo = forms.FileField(
        label="Arquivo",
        help_text=f"Formatos aceitos: {EXTENSOES_ACEITAS}.",
    )

    class Meta:
        model = Document
        fields = ["title", "arquivo"]

    # ------------------------------------------------------------------
    # Validações
    # ------------------------------------------------------------------
    @property
    def limite_bytes(self) -> int:
        """Tamanho máximo permitido, configurado por variável de ambiente."""
        return int(settings.KNOWLEDGE_MAX_UPLOAD_MB) * 1024 * 1024

    def clean_arquivo(self):
        arquivo = self.cleaned_data["arquivo"]
        extensao = Path(arquivo.name).suffix.lower()

        # 1) Extensão (formatos do MVP)
        if extensao not in FORMATOS_PERMITIDOS:
            raise forms.ValidationError(
                f"Formato não permitido ({extensao or 'sem extensão'}). "
                f"Envie um arquivo {EXTENSOES_ACEITAS}."
            )

        # 2) Tamanho máximo
        if arquivo.size > self.limite_bytes:
            limite_mb = settings.KNOWLEDGE_MAX_UPLOAD_MB
            raise forms.ValidationError(
                f"Arquivo muito grande ({arquivo.size // 1024 // 1024} MB). "
                f"O limite é de {limite_mb} MB."
            )

        # 3) Tipo de conteúdo enviado pelo navegador
        content_type = (arquivo.content_type or "").lower()
        if content_type and content_type not in FORMATOS_PERMITIDOS[extensao]:
            if not content_type.startswith("text/"):
                raise forms.ValidationError(
                    "O tipo do arquivo não corresponde ao formato esperado."
                )

        # 4) Conteúdo do arquivo (PDF precisa começar com %PDF-)
        cabecalho = arquivo.read(5)
        arquivo.seek(0)
        if extensao == ".pdf" and cabecalho != b"%PDF-":
            raise forms.ValidationError("O arquivo enviado não é um PDF válido.")
        if extensao != ".pdf" and cabecalho == b"%PDF-":
            raise forms.ValidationError("O conteúdo do arquivo não corresponde à extensão.")

        return arquivo
