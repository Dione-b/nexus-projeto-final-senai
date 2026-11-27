"""
URLs do projeto Nexus Atendimento.

Nenhum include de app por enquanto: a raiz fica vazia e apenas serve arquivos
estáticos e de mídia durante o desenvolvimento (DEBUG=True).
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

urlpatterns = [
    # As rotas dos apps serão incluídas nas próximas sprints.
]

# Serviço de arquivos estáticos e mídia apenas em desenvolvimento.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
