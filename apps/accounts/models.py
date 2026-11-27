"""Modelos do app accounts (usuários e permissões)."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Usuário do sistema com papel (role) para controle de acesso.

    O papel permite aplicar a RN01 (apenas administradores podem gerenciar a
    base de conhecimento) sem depender somente de ``is_superuser``.
    """

    class Role(models.TextChoices):
        CLIENTE = "cliente", "Cliente"
        ADMINISTRADOR = "administrador", "Administrador"

    role = models.CharField(
        "papel",
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENTE,
    )

    @property
    def is_administrador(self) -> bool:
        """Indica se o usuário pode gerenciar a base de conhecimento (RN01)."""
        return self.is_superuser or self.role == self.Role.ADMINISTRADOR

    def __str__(self) -> str:
        return self.get_username()
