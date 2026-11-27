"""Testes de fumaça da aplicação.

Verificam que o projeto está configurado corretamente sem depender
de banco de dados (usam apenas ``SimpleTestCase``).
"""

import importlib

from django.conf import settings
from django.test import SimpleTestCase

MODULOS_APPS = (
    "apps.accounts.apps",
    "apps.conversations.apps",
    "apps.knowledge.apps",
    "apps.rag.apps",
    "apps.telegram.apps",
    "apps.feedback.apps",
    "apps.monitoring.apps",
)


class SmokeTestCase(SimpleTestCase):
    """Verifica a configuração básica do Django e dos apps do projeto."""

    def test_settings_carregadas(self):
        """As configurações do projeto são carregadas e DEBUG é booleano."""
        self.assertTrue(settings.configured)
        self.assertIsInstance(settings.DEBUG, bool)

    def test_pacotes_dos_apps_importaveis(self):
        """Todos os pacotes de apps previstos na seção 9 do README existem."""
        for modulo in MODULOS_APPS:
            with self.subTest(modulo=modulo):
                importlib.import_module(modulo)

    def test_template_base_existe(self):
        """O template base mobile-first está presente."""
        from pathlib import Path

        raiz = Path(__file__).resolve().parent.parent
        self.assertTrue((raiz / "templates" / "base.html").is_file())
        self.assertTrue((raiz / "static" / "css" / "base.css").is_file())
