"""Testes do banco de dados (PostgreSQL + pgvector).

Precisam do banco rodando: docker compose up -d
"""

from django.db import connection
from django.test import TestCase


class DatabaseTestCase(TestCase):
    """Verifica que o banco é PostgreSQL e que o pgvector está ativo."""

    def test_banco_e_postgresql(self):
        self.assertEqual(connection.vendor, "postgresql")

    def test_extensao_vector_habilitada(self):
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1 FROM pg_extension WHERE extname = 'vector'")
            self.assertIsNotNone(cursor.fetchone())
