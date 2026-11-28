"""Testes do serviço de embeddings (issue #7 — Sprint 02).

Usam o PostgreSQL + pgvector (docker compose up -d) e mockam a API externa
para não depender de chave nem de rede.
"""

from unittest import mock

from django.conf import settings
from django.test import TestCase

from apps.knowledge.models import Document
from apps.rag.embeddings import EmbeddingError, embed_document, embed_texts


def _fake_response(vectors, status_code=200, text=""):
    """Monta uma resposta falsa no formato da API de embeddings (OpenAI)."""
    response = mock.Mock()
    response.status_code = status_code
    response.text = text
    response.json.return_value = {
        "data": [
            {"index": index, "embedding": vector}
            for index, vector in enumerate(vectors)
        ]
    }
    return response


class EmbedTextsTestCase(TestCase):
    """Serviço em lote: envio, validação de dimensão e retry."""

    @mock.patch("apps.rag.embeddings.requests.post")
    def test_retorna_um_vetor_por_texto(self, post):
        dim = settings.EMBEDDING_DIMENSIONS
        post.return_value = _fake_response([[0.1] * dim, [0.2] * dim])

        vectors = embed_texts(["texto um", "texto dois"])

        self.assertEqual(len(vectors), 2)
        self.assertEqual(len(vectors[0]), dim)

    @mock.patch("apps.rag.embeddings.requests.post")
    def test_erro_de_dimensao_e_invalido(self, post):
        post.return_value = _fake_response([[0.1, 0.2]])  # dimensão errada

        with self.assertRaises(EmbeddingError):
            embed_texts(["texto"])

    @mock.patch("apps.rag.embeddings.requests.post")
    def test_erro_definitivo_nao_tenta_de_novo(self, post):
        # 401 = chave inválida: falha imediata, sem retry.
        post.return_value = _fake_response([], status_code=401, text="unauthorized")

        with self.assertRaises(EmbeddingError):
            embed_texts(["texto"])

        self.assertEqual(post.call_count, 1)

    @mock.patch("apps.rag.embeddings.requests.post")
    def test_erro_transitorio_tenta_de_novo(self, post):
        dim = settings.EMBEDDING_DIMENSIONS
        # Primeira tentativa falha (503), segunda retorna os vetores.
        post.side_effect = [
            _fake_response([], status_code=503, text="unavailable"),
            _fake_response([[0.1] * dim]),
        ]

        vectors = embed_texts(["texto"])

        self.assertEqual(len(vectors), 1)
        self.assertEqual(post.call_count, 2)


class EmbedDocumentTestCase(TestCase):
    """Indexação de um documento: gravação dos vetores e estado."""

    def _criar_documento(self, titulos_chunks):
        document = Document.objects.create(title="Política de devolução")
        for content in titulos_chunks:
            document.chunks.create(content=content)
        return document

    @mock.patch("apps.rag.embeddings.requests.post")
    def test_documento_indexado_com_vetores_corretos(self, post):
        dim = settings.EMBEDDING_DIMENSIONS
        post.return_value = _fake_response([[0.1] * dim, [0.2] * dim])
        document = self._criar_documento(["trecho um", "trecho dois"])

        sucesso = embed_document(document)

        self.assertTrue(sucesso)
        document.refresh_from_db()
        self.assertEqual(document.status, Document.Status.INDEXADO)
        for chunk in document.chunks.all():
            self.assertIsNotNone(chunk.embedding)
            self.assertEqual(len(chunk.embedding), dim)

    @mock.patch("apps.rag.embeddings.requests.post")
    def test_falha_na_api_marca_erro_e_nao_deixa_chunk_sem_vetor(self, post):
        # Erro definitivo (401): a API falhou antes de gerar qualquer vetor.
        post.return_value = _fake_response([], status_code=401, text="unauthorized")
        document = self._criar_documento(["trecho um", "trecho dois"])

        sucesso = embed_document(document)

        self.assertFalse(sucesso)
        document.refresh_from_db()
        self.assertEqual(document.status, Document.Status.ERRO)
        self.assertNotEqual(document.error_message, "")
        # Critério: nenhum chunk fica registrado sem vetor.
        self.assertEqual(document.chunks.filter(embedding__isnull=True).count(), 0)

    @mock.patch("apps.rag.embeddings.requests.post")
    def test_reprocessamento_nao_duplica_chunks(self, post):
        dim = settings.EMBEDDING_DIMENSIONS
        post.return_value = _fake_response([[0.1] * dim, [0.2] * dim])
        document = self._criar_documento(["antigo"])

        embed_document(document, texts=["trecho um", "trecho dois"])
        embed_document(document, texts=["trecho um", "trecho dois"])

        self.assertEqual(document.chunks.count(), 2)

    @mock.patch("apps.rag.embeddings.requests.post")
    def test_documento_sem_chunks_fica_com_erro(self, post):
        document = Document.objects.create(title="Vazio")

        sucesso = embed_document(document, texts=["   ", ""])

        self.assertFalse(sucesso)
        document.refresh_from_db()
        self.assertEqual(document.status, Document.Status.ERRO)
        self.assertEqual(post.call_count, 0)
