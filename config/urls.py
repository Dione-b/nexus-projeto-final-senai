"""
URLs do projeto Nexus Atendimento.

O painel administrativo é servido pelo site próprio do Nexus, que aplica
a RN01 (somente administradores). As rotas dos apps serão incluídas nas
próximas sprints.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from apps.accounts.admin_site import nexus_admin_site

urlpatterns = [
    path("admin/", nexus_admin_site.urls),
]

# Serviço de arquivos estáticos e mídia apenas em desenvolvimento.
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
