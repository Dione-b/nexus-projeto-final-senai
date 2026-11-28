"""Testes do Django Admin (Sprint 01, issue #4).

São testes sem banco de dados (``SimpleTestCase``): verificam registro,
configuração e regras de acesso do painel, o que permite validá-los sem
o PostgreSQL rodando.
"""

from django.contrib.admin import ModelAdmin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory, SimpleTestCase
from django.urls import reverse

from apps.accounts.admin import UserAdmin
from apps.accounts.admin_site import nexus_admin_site
from apps.accounts.models import User
from apps.conversations.admin import ConversationAdmin, MessageAdmin
from apps.conversations.models import Conversation, Message
from apps.feedback.admin import FeedbackAdmin
from apps.feedback.models import Feedback
from apps.knowledge.admin import ChunkAdmin, DocumentAdmin
from apps.knowledge.models import Chunk, Document
from apps.rag.admin import RetrievalAdmin
from apps.rag.models import Retrieval

MODELOS = (User, Conversation, Message, Document, Chunk, Retrieval, Feedback)
ADMINISTRADORES = (
    UserAdmin,
    ConversationAdmin,
    MessageAdmin,
    DocumentAdmin,
    ChunkAdmin,
    RetrievalAdmin,
    FeedbackAdmin,
)


class RegistroNoAdminTests(SimpleTestCase):
    """CRUD completo em /admin/ — os sete modelos da issue #4 registrados."""

    def test_os_sete_modelos_estao_registrados(self):
        faltando = set(MODELOS) - set(nexus_admin_site._registry)
        self.assertFalse(faltando, f"Modelos sem registro no admin: {faltando}")

    def test_registros_sao_model_admin(self):
        for modelo in MODELOS:
            with self.subTest(modelo=modelo.__name__):
                self.assertIsInstance(
                    nexus_admin_site._registry[modelo], ModelAdmin
                )

    def test_rota_do_admin_esta_mapeada(self):
        self.assertEqual(reverse("admin:index"), "/admin/")

    def test_listagem_filtro_e_busca_configurados(self):
        for admin_classe in ADMINISTRADORES:
            with self.subTest(admin=admin_classe.__name__):
                self.assertTrue(admin_classe.list_display)
                self.assertTrue(admin_classe.list_filter)
                self.assertTrue(admin_classe.search_fields)


class Rn01AcessoTests(SimpleTestCase):
    """RN01 — apenas superusuário ou administrador acessa o admin."""

    def setUp(self):
        self.factory = RequestFactory()

    def _permite(self, usuario):
        request = self.factory.get("/admin/")
        request.user = usuario
        return nexus_admin_site.has_permission(request)

    def test_anonimo_nao_aceessao(self):
        self.assertFalse(self._permite(AnonymousUser()))

    def test_cliente_nao_acessa(self):
        cliente = User(username="ana", is_active=True, role=User.Role.CLIENTE)
        self.assertFalse(self._permite(cliente))

    def test_usuario_inativo_nao_acessa(self):
        inativo = User(
            username="bia", is_active=False, role=User.Role.ADMINISTRADOR
        )
        self.assertFalse(self._permite(inativo))

    def test_administrador_acessa(self):
        admin = User(
            username="carlos", is_active=True, role=User.Role.ADMINISTRADOR
        )
        self.assertTrue(self._permite(admin))

    def test_superusucesso_acessa_mesmo_com_papel_cliente(self):
        """O critério de aceitação citam explicitamente o superusuário."""
        superuser = User(
            username="root", is_active=True, is_superuser=True,
            role=User.Role.CLIENTE,
        )
        self.assertTrue(self._permite(superuser))

    def test_superusucesso_inativo_nao_acessa(self):
        superuser = User(
            username="root", is_active=False, is_superuser=True,
            role=User.Role.CLIENTE,
        )
        self.assertFalse(self._permite(superuser))


class CamposSensiveisTests(SimpleTestCase):
    """A issue pede esconder hash de senha e embeddings crus."""

    def test_embedding_nao_entra_no_formulario(self):
        self.assertIn("embedding", ChunkAdmin.exclude)
        for inline in DocumentAdmin.inlines:
            with self.subTest(inline=inline.__name__):
                self.assertIn("embedding", inline.exclude)

    def test_hash_da_senha_nao_aparece_em_claro(self):
        # Senha codificada fictícia com um trecho facilmente identificável.
        codificada = (
            "pbkdf2_sha256$260000$abcdefghij$ZYXWVUTSRQPONMLKJIHGFEDCBA"
        )
        formulario = UserChangeForm(
            instance=User(username="ana", password=codificada)
        )
        html = formulario["password"].as_widget()

        self.assertNotIn(codificada, html)
        self.assertNotIn("ZYXWVUTSRQPONMLKJIHGFEDCBA", html)
        self.assertIn("*", html)


class AuditoriaSomenteLeituraTests(SimpleTestCase):
    """Campos de auditoria (created_at) configurados como somente leitura."""

    def test_created_at_somente_leitura(self):
        for admin_classe in (
            ConversationAdmin,
            MessageAdmin,
            DocumentAdmin,
            RetrievalAdmin,
        ):
            with self.subTest(admin=admin_classe.__name__):
                self.assertIn("created_at", admin_classe.readonly_fields)

    def test_admins_sem_campo_de_auditoria_nao_o_referenciam(self):
        """Chunk e Feedback não têm created_at: não pode ser referenciado."""
        for admin_classe in (ChunkAdmin, FeedbackAdmin):
            with self.subTest(admin=admin_classe.__name__):
                self.assertNotIn("created_at", admin_classe.readonly_fields)
                self.assertFalse(getattr(admin_classe, "date_hierarchy", None))
