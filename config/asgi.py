"""
Configuração ASGI do projeto Nexus Atendimento.

Usada por servidores ASGI (ex.: daphne, uvicorn) para servir a aplicação.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()
