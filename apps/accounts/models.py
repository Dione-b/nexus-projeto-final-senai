from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Usuário da plataforma (cliente ou administrador)."""

    class Role(models.TextChoices):
        CLIENTE = "cliente", "Cliente"
        ADMINISTRADOR = "administrador", "Administrador"

    name = models.CharField("nome", max_length=150)
    email = models.EmailField("e-mail", unique=True)
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CLIENTE,
    )

    class Meta:
        verbose_name = "usuário"
        verbose_name_plural = "usuários"

    def __str__(self):
        return self.name or self.email

    @property
    def is_administrator(self):
        return self.role == self.Role.ADMINISTRADOR

    def save(self, *args, **kwargs):
        # Administradores sempre têm acesso ao painel (RN01).
        if self.is_administrator:
            self.is_staff = True
        super().save(*args, **kwargs)
