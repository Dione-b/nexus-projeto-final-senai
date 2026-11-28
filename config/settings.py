"""
Configurações do projeto Nexus Atendimento.

Toda a configuração portável é lida de variáveis de ambiente (arquivo `.env`),
conforme o RNF de Portabilidade do README. Os valores padrão atendem apenas ao
desenvolvimento local.
"""

import os
from pathlib import Path

from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env (se existir).
load_dotenv()

# ---------------------------------------------------------------------
# Caminhos base
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


# ---------------------------------------------------------------------
# Helpers de leitura de variáveis de ambiente
# ---------------------------------------------------------------------
def env(key: str, default: str = "") -> str:
    """Lê uma variável de ambiente com valor padrão seguro para desenvolvimento."""
    return os.environ.get(key, default)


def env_bool(key: str, default: bool = False) -> bool:
    """Lê uma variável booleana (1/true/yes/on ativam; 0/false/no/off desativam)."""
    value = os.environ.get(key)
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_list(key: str, default: str = "") -> list[str]:
    """Lê uma variável separada por vírgulas e retorna uma lista sem espaços."""
    value = os.environ.get(key, default)
    return [item.strip() for item in value.split(",") if item.strip()]


# ---------------------------------------------------------------------
# Segurança
# ---------------------------------------------------------------------
# ATENÇÃO: a chave padrão é insegura e serve apenas para desenvolvimento local.
# Em produção, defina DJANGO_SECRET_KEY no ambiente.
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    "django-insecure-dev-only-substitua-em-producao",
)

DEBUG = env_bool("DJANGO_DEBUG", True)

ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1")

# ---------------------------------------------------------------------
# Aplicativos instalados (apps internos do monólito modular)
# ---------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Necessario para os indices vetoriais (HnswIndex) - issue #3
    "django.contrib.postgres",
    # Apps internos do Nexus Atendimento
    "apps.accounts.apps.AccountsConfig",
    "apps.conversations.apps.ConversationsConfig",
    "apps.knowledge.apps.KnowledgeConfig",
    "apps.rag.apps.RagConfig",
    "apps.telegram.apps.TelegramConfig",
    "apps.feedback.apps.FeedbackConfig",
    "apps.monitoring.apps.MonitoringConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ---------------------------------------------------------------------
# Banco de dados (PostgreSQL + pgvector)
# ---------------------------------------------------------------------
# O PostgreSQL é obrigatório: as migrations criam a extensão pgvector e o
# índice HNSW (issue #3). Sobe com `docker compose up -d`.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME", "nexus"),
        "USER": env("DB_USER", "nexus"),
        "PASSWORD": env("DB_PASSWORD", "nexus"),
        "HOST": env("DB_HOST", "127.0.0.1"),
        "PORT": env("DB_PORT", "5432"),
    }
}

# ---------------------------------------------------------------------
# Validação de senha
# ---------------------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

# ---------------------------------------------------------------------
# Internacionalização e fuso horário
# ---------------------------------------------------------------------
LANGUAGE_CODE = "pt-br"
TIME_ZONE = "America/Sao_Paulo"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------
# Arquivos estáticos e mídia
# ---------------------------------------------------------------------
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]

MEDIA_URL = "media/"
# A pasta `documents/` (seção 9 do README) é a MEDIA_ROOT: é nela que os
# arquivos enviados pela base de conhecimento são armazenados (issue #5).
MEDIA_ROOT = BASE_DIR / "documents"

# ---------------------------------------------------------------------
# Base de conhecimento (Sprint 02)
# ---------------------------------------------------------------------
# Tamanho máximo de upload configurável por variável de ambiente (RNF
# Portabilidade). Usado pela validação do formulário de documentos.
KNOWLEDGE_MAX_UPLOAD_MB = int(env("KNOWLEDGE_MAX_UPLOAD_MB", "10"))

# ---------------------------------------------------------------------
# Chave primária padrão
# ---------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------------------
# Autenticacao (issue #3 - modelos da secao 8)
# ---------------------------------------------------------------------
# Usuario proprio da plataforma (cliente/administrador).
AUTH_USER_MODEL = "accounts.User"

# ---------------------------------------------------------------------
# RAG / embeddings
# ---------------------------------------------------------------------
# Dimensao do vetor de embeddings; depende do modelo escolhido (secao 15
# do README - decisao ainda pendente). Precisa ser conhecida pela migration
# que cria a coluna "embedding vector(dim)".
EMBEDDING_DIMENSIONS = int(env("EMBEDDING_DIMENSIONS", "1536"))

# ---------------------------------------------------------------------
# Logging (RNF — Observabilidade: logs, erros e métricas)
# ---------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG" if DEBUG else "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "DEBUG" if DEBUG else "INFO",
            "propagate": False,
        },
    },
}
