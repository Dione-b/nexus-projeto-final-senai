"""Habilita a extensão pgvector no PostgreSQL.

Deve rodar antes de qualquer modelo que use campos vetoriais (ex.: Chunk).
"""

from django.contrib.postgres.operations import CreateExtension
from django.db import migrations


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        CreateExtension("vector"),
    ]
