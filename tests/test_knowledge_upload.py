"""Testes da issue #5 — Upload de documentos na base de conhecimento (US10).

Cobre os critérios de aceitação:
- administrador envia documento e o registro aparece com status "pendente";
- cliente não autenticado/sem papel recebe 403 (RN01);
- arquivo inválido gera mensagem de erro sem trace.
"""

import shutil
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from apps.accounts.models import User
from apps.knowledge.models import Document

ARQUIVO_PDF = b"%PDF-1.4\nconteudo de teste do pdf\n"
ARQUIVO_TXT = b"conteudo de texto simples\n"


class BaseDeConhecimentoTestCase(TestCase):
    """Base com mídia temporária e usuários de cada papel."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.media_root = tempfile.mkdtemp()
        cls._media = override_settings(MEDIA_ROOT=cls.media_root)
        cls._media.enable()
        cls.addClassCleanup(cls._media.disable)
        cls.addClassCleanup(shutil.rmtree, cls.media_root, ignore_errors=True)

    def setUp(self):
        self.admin = User.objects.create_user(
            username="admin",
            name="Administrador",
            email="admin@nexus.test",
            password="senha-forte-123",
            role=User.Role.ADMINISTRADOR,
        )
        self.cliente = User.objects.create_user(
            username="cliente",
            name="Cliente",
            email="cliente@nexus.test",
            password="senha-forte-123",
            role=User.Role.CLIENTE,
        )
        self.url = reverse("knowledge:document_list")
        self.url_upload = reverse("knowledge:document_upload")

    @staticmethod
    def arquivo(nome, conteudo, content_type):
        return SimpleUploadedFile(nome, conteudo, content_type=content_type)


class PermissaoTests(BaseDeConhecimentoTestCase):
    """RN01 — acesso restrito a administradores."""

    def test_nao_autenticado_recebe_403(self):
        """Visitante sem sessão recebe 403 na listagem e no upload."""
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code, 403)
        self.assertContains(resposta, "Acesso restrito", status_code=403)

        resposta = self.client.post(
            self.url_upload, {"arquivo": self.arquivo("doc.pdf", ARQUIVO_PDF, "application/pdf")}
        )
        self.assertEqual(resposta.status_code, 403)
        self.assertEqual(Document.objects.count(), 0)

    def test_cliente_sem_papel_recebe_403(self):
        """Usuário autenticado sem papel administrador recebe 403 (RN01)."""
        self.client.login(username="cliente", password="senha-forte-123")

        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code, 403)
        self.assertContains(resposta, "Acesso restrito", status_code=403)

        resposta = self.client.post(
            self.url_upload, {"arquivo": self.arquivo("doc.pdf", ARQUIVO_PDF, "application/pdf")}
        )
        self.assertEqual(resposta.status_code, 403)
        self.assertEqual(Document.objects.count(), 0)

    def test_administrador_acessa_a_listagem(self):
        """Administrador autenticado acessa a base de conhecimento."""
        self.client.login(username="admin", password="senha-forte-123")
        resposta = self.client.get(self.url)
        self.assertEqual(resposta.status_code, 200)


class UploadTests(BaseDeConhecimentoTestCase):
    """Critério: documento enviado aparece com status "pendente"."""

    def setUp(self):
        super().setUp()
        self.client.login(username="admin", password="senha-forte-123")

    def test_upload_pdf_cria_documento_pendente(self):
        """O documento é criado com status pendente e o arquivo fica em MEDIA_ROOT."""
        arquivo = self.arquivo("politica-devolucao.pdf", ARQUIVO_PDF, "application/pdf")
        resposta = self.client.post(self.url_upload, {"arquivo": arquivo})

        self.assertEqual(resposta.status_code, 302)
        documento = Document.objects.get()
        self.assertEqual(documento.status, Document.Status.PENDENTE)
        self.assertEqual(documento.title, "politica-devolucao")
        self.assertEqual(documento.enviado_por, self.admin)
        self.assertTrue(documento.arquivo.name.endswith("politica-devolucao.pdf"))
        # O arquivo físico existe dentro de MEDIA_ROOT (documents/).
        self.assertTrue(documento.arquivo.storage.exists(documento.arquivo.name))

        # O registro aparece na listagem com o status "pendente".
        listagem = self.client.get(self.url)
        self.assertContains(listagem, "politica-devolucao")
        self.assertContains(listagem, "Pendente")

    def test_upload_txt_e_md_sao_aceitos(self):
        """Formatos do MVP: PDF, TXT e MD."""
        casos = [
            ("leitura.txt", ARQUIVO_TXT, "text/plain"),
            ("notas.md", b"# notas\n\ntexto", "text/markdown"),
        ]
        for nome, conteudo, tipo in casos:
            with self.subTest(nome=nome):
                resposta = self.client.post(
                    self.url_upload, {"arquivo": self.arquivo(nome, conteudo, tipo)}
                )
                self.assertEqual(resposta.status_code, 302)
        self.assertEqual(Document.objects.count(), 2)

    def test_titulo_padrao_usa_nome_do_arquivo(self):
        """Sem título informado, o título é o nome do arquivo."""
        self.client.post(
            self.url_upload,
            {"arquivo": self.arquivo("politicas.txt", ARQUIVO_TXT, "text/plain")},
        )
        self.assertEqual(Document.objects.get().title, "politicas")

    def test_upload_htmx_retorna_hx_redirect(self):
        """A resposta HTMX instrui o navegador a recarregar a listagem."""
        resposta = self.client.post(
            self.url_upload,
            {"arquivo": self.arquivo("doc.pdf", ARQUIVO_PDF, "application/pdf")},
            headers={"HX-Request": "true"},
        )
        self.assertEqual(resposta.status_code, 200)
        self.assertEqual(resposta["HX-Redirect"], self.url)


class ValidacaoTests(BaseDeConhecimentoTestCase):
    """Critério: arquivo inválido gera mensagem de erro sem trace."""

    def setUp(self):
        super().setUp()
        self.client.login(username="admin", password="senha-forte-123")

    def assertErroDeFormulario(self, resposta, texto_esperado):
        """A resposta é um HTML de erro com a mensagem e sem trace."""
        self.assertEqual(resposta.status_code, 200)
        self.assertContains(resposta, texto_esperado)
        self.assertNotContains(resposta, "Traceback")
        self.assertEqual(Document.objects.count(), 0)

    def test_extensao_nao_permitida(self):
        """Formato fora do MVP (PDF, TXT, MD) é recusado."""
        resposta = self.client.post(
            self.url_upload,
            {"arquivo": self.arquivo("imagem.png", b"\x89PNG", "image/png")},
        )
        self.assertErroDeFormulario(resposta, "Formato n")

    def test_pdf_falso_e_recusado(self):
        """Arquivo com extensão .pdf mas conteúdo diferente de PDF."""
        resposta = self.client.post(
            self.url_upload,
            {"arquivo": self.arquivo("falso.pdf", b"nao sou um pdf", "application/pdf")},
        )
        self.assertErroDeFormulario(resposta, "não é um PDF válido")

    def test_tipo_de_conteudo_divergente(self):
        """Content-Type incompatível com a extensão é recusado."""
        resposta = self.client.post(
            self.url_upload,
            {"arquivo": self.arquivo("script.txt", b"alerta", "application/x-msdownload")},
        )
        self.assertErroDeFormulario(resposta, "não corresponde ao formato esperado")

    @override_settings(KNOWLEDGE_MAX_UPLOAD_MB=1)
    def test_arquivo_acima_do_limite(self):
        """Arquivo maior que KNOWLEDGE_MAX_UPLOAD_MB é recusado."""
        conteudo = b"0" * (1024 * 1024 + 1)
        resposta = self.client.post(
            self.url_upload,
            {"arquivo": self.arquivo("grande.txt", conteudo, "text/plain")},
        )
        self.assertErroDeFormulario(resposta, "muito grande")

    def test_arquivo_ausente(self):
        """Envio sem arquivo mostra mensagem de erro amigável."""
        resposta = self.client.post(self.url_upload, {})
        self.assertErroDeFormulario(resposta, "Este campo é obrigatório")
