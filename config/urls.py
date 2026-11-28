"""
URLs do projeto Nexus Atendimento.

O painel administrativo é servido pelo site próprio do Nexus, que aplica
a RN01 (somente administradores).
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path

from apps.accounts.admin_site import nexus_admin_site

urlpatterns = [
    # Django Admin (Sprint 01 — issue #4): também serve de login para o
    # administrador acessar a base de conhecimento.
    path("admin/", nexus_admin_site.urls),
    # Base de conhecimento (Sprint 02 — US10).
    path("base-conhecimento/", include("apps.knowledge.urls", namespace="knowledge")),
    # As demais rotas serão incluídas nas próximas sprints.
]

handler403 = "config.views.permission_denied"

# Serviço de arquivos estáticos e mídia apenas em desenvolvimento.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
