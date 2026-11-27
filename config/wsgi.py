"""
Configuração WSGI do projeto Nexus Atendimento.

Usada por servidores WSGI (ex.: gunicorn, waitress) para servir a aplicação.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_wsgi_application()
