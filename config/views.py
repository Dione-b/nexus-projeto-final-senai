"""Views genéricas de configuração (páginas de erro)."""

from django.shortcuts import render


def permission_denied(request, exception=None):
    """Página amigável para HTTP 403 (RN01 — acesso restrito)."""
    return render(request, "403.html", status=403)
