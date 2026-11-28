"""Geração de embeddings dos trechos com o modelo de embeddings do projeto.

Decisão registrada no README (seção 15): a geração usa uma API compatível
com OpenAI — endpoint, modelo, dimensão e lotes são configurados pelas
variáveis de ambiente `EMBEDDING_*` (veja `.env.example`).
"""

import logging
import time

import requests
from django.conf import settings
from django.db import transaction

from apps.knowledge.models import Chunk, Document

logger = logging.getLogger(__name__)


class EmbeddingError(Exception):
    """Erro ao gerar embeddings (API indisponível ou resposta inválida)."""


def embed_texts(texts):
    """Retorna um vetor (lista de floats) para cada texto recebido.

    Os textos são enviados em lotes de `EMBEDDING_BATCH_SIZE`, com retry e
    backoff exponencial em falhas transitórias (rede, 429, 5xx).
    """
    vectors = []
    batch_size = settings.EMBEDDING_BATCH_SIZE
    for start in range(0, len(texts), batch_size):
        batch = texts[start:start + batch_size]
        payload = _post_embeddings(batch)
        vectors.extend(_extract_vectors(payload, len(batch)))
    return vectors


def embed_document(document, texts=None):
    """Indexa um documento: grava os vetores dos chunks e atualiza o status.

    - `texts` (opcional): substitui os chunks do documento antes de gerar os
      vetores. Sempre apaga os antigos primeiro — o reprocessamento não
      duplica chunks.
    - Sucesso: todos os chunks recebem vetor e o documento fica "indexado".
    - Falha: o documento fica "erro" e nenhum chunk fica sem vetor.

    Retorna True em caso de sucesso e False em caso de falha.
    """
    if texts is not None:
        _replace_chunks(document, texts)

    chunks = list(document.chunks.all())
    if not chunks:
        _mark_error(document, "Nenhum chunk para indexar.")
        return False

    try:
        vectors = embed_texts([chunk.content for chunk in chunks])
    except EmbeddingError as exc:
        logger.error("Falha ao indexar documento %s: %s", document.pk, exc)
        with transaction.atomic():
            # Nenhum chunk pode ficar sem vetor: remove os que não receberam.
            document.chunks.filter(embedding__isnull=True).delete()
            _mark_error(document, str(exc))
        return False

    with transaction.atomic():
        for chunk, vector in zip(chunks, vectors):
            chunk.embedding = vector
            chunk.save(update_fields=["embedding"])
        document.status = Document.Status.INDEXADO
        document.error_message = ""
        document.save(update_fields=["status", "error_message"])

    logger.info("Documento %s indexado com %d chunks.", document.pk, len(chunks))
    return True


def _post_embeddings(batch):
    """Chama a API de embeddings uma vez por lote, com retry e backoff.

    Repete em erro de rede, 429 (rate limit) e 5xx. Erros 4xx (ex.: chave
    inválida) são definitivos e interrompem as tentativas.
    """
    url = settings.EMBEDDING_BASE_URL.rstrip("/") + "/embeddings"
    headers = {"Content-Type": "application/json"}
    if settings.EMBEDDING_API_KEY:
        headers["Authorization"] = f"Bearer {settings.EMBEDDING_API_KEY}"
    payload = {
        "model": settings.EMBEDDING_MODEL,
        "input": batch,
        "dimensions": settings.EMBEDDING_DIMENSIONS,
    }

    attempts = settings.EMBEDDING_MAX_RETRIES + 1
    last_error = "erro desconhecido"

    for attempt in range(attempts):
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=settings.EMBEDDING_TIMEOUT,
            )
        except requests.RequestException as exc:
            last_error, retryable = str(exc), True
        else:
            if response.status_code == 200:
                try:
                    return response.json()
                except ValueError as exc:
                    last_error, retryable = f"resposta sem JSON válido ({exc})", True
            else:
                last_error = f"HTTP {response.status_code}: {response.text[:300]}"
                retryable = response.status_code == 429 or response.status_code >= 500

        if not retryable:
            break
        if attempt < attempts - 1:
            time.sleep(settings.EMBEDDING_BACKOFF * (2 ** attempt))

    raise EmbeddingError(f"Falha ao chamar a API de embeddings: {last_error}")


def _extract_vectors(payload, expected_count):
    """Lê os vetores da resposta da API e valida a dimensão configurada."""
    data = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(data, list):
        raise EmbeddingError("Resposta da API de embeddings não contém 'data'.")

    # A API pode devolver os vetores fora de ordem; o campo "index" garante
    # que cada texto receba o seu próprio vetor.
    items = sorted(data, key=lambda item: item.get("index", 0))
    vectors = [item.get("embedding") for item in items]

    if len(vectors) != expected_count:
        raise EmbeddingError(
            f"API retornou {len(vectors)} vetores para {expected_count} textos."
        )

    dimensions = settings.EMBEDDING_DIMENSIONS
    for position, vector in enumerate(vectors):
        if not isinstance(vector, list) or len(vector) != dimensions:
            raise EmbeddingError(
                f"Vetor {position} com dimensão diferente de {dimensions}."
            )
    return vectors


def _replace_chunks(document, texts):
    """Recria os chunks do documento a partir dos textos recebidos.

    Apaga sempre os chunks antigos antes de criar os novos: o
    reprocessamento não duplica chunks.
    """
    with transaction.atomic():
        document.chunks.all().delete()
        Chunk.objects.bulk_create(
            [
                Chunk(document=document, content=text)
                for text in texts
                if text and text.strip()
            ]
        )


def _mark_error(document, message):
    """Marca o documento como erro e registra o motivo (observabilidade)."""
    document.status = Document.Status.ERRO
    document.error_message = message
    document.save(update_fields=["status", "error_message"])
