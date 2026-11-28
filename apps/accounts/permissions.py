"""Decoradores de permissão do app accounts."""

from functools import wraps

from django.core.exceptions import PermissionDenied


def administrador_required(view_func):
    """Restringe a view a administradores autenticados (RN01).

    Quem não está autenticado ou não possui o papel ``administrador`` recebe
    HTTP 403. O login não é redirecionado para evitar revelar que a área
    existe.
    """

    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        usuario = request.user
        if not usuario.is_authenticated or not usuario.is_administrator:
            raise PermissionDenied("Acesso restrito a administradores.")
        return view_func(request, *args, **kwargs)

    return _wrapped
