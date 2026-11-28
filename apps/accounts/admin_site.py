"""Painel administrativo do Nexus (RN01 — somente administradores)."""

from django.contrib.admin import AdminSite


class NexusAdminSite(AdminSite):
    """Administração do Nexus Atendimento.

    RN01: apenas administradores podem gerenciar a base de conhecimento.
    Superusuários sempre entram, mesmo com o papel `cliente`, porque o
    Django os trata como detentores de todas as permissões.
    """

    site_header = "Nexus Atendimento — Administração"
    site_title = "Nexus Admin"
    index_title = "Gestão da base de conhecimento"

    def has_permission(self, request):
        """Autentica o usuário e aplica a RN01 antes de liberar a tela."""
        user = request.user
        if not (user and user.is_authenticated and user.is_active):
            return False
        return bool(user.is_superuser or getattr(user, "is_administrator", False))


# O nome "admin" mantém o namespace padrão das URLs (`admin:index`), que
# as templates internas do Django usam para montar os links.
nexus_admin_site = NexusAdminSite(name="admin")
