#!/usr/bin/env python
"""Script de linha de comando do Django para o projeto Nexus Atendimento."""

import os
import sys


def main():
    """Executa utilitários administrativos do Django."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Não foi possível importar o Django. "
            "Verifique se as dependências estão instaladas e se o ambiente "
            "virtual está ativo (requirements.txt)."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
