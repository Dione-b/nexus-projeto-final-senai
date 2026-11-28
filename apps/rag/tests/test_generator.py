"""Testes do generator (Sprint 03 — issue #11).

Não acessam banco de dados (SimpleTestCase) nem a API real da Anthropic:
o cliente é substituído por um mock.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest import mock

import anthropic
import httpx2
from django.test import SimpleTestCase

from apps.rag import generator


def _http_response(status_code: int) -> httpx2.Response:
    return httpx2.Response(
        status_code,
        request=httpx2.Request("POST", "https://api.anthropic.com/v1/messages"),
    )


def _api_error(cls, status_code: int):
    return cls("erro do provedor", response=_http_response(status_code), body=None)


def _llm_response(text: str = "Resposta da Nexus. [Fonte 1]"):
    return SimpleNamespace(
        content=[SimpleNamespace(type="text", text=text)],
        usage=SimpleNamespace(input_tokens=120, output_tokens=45),
    )


def _new_client_mock(*side_effects):
    client = mock.Mock()
    client.messages.create.side_effect = side_effects
    return client


CONTEXT = [
    {"content": "A devolução é permitida em até 30 dias.", "source": "Politica de devolucao.pdf"},
    {"content": "O prazo de entrega é de 5 dias úteis.", "source": "Prazos.md"},
]
HISTORY = [
    {"role": "user", "content": "Olá, boa tarde"},
    {"role": "assistant", "content": "Olá! Como posso ajudar?"},
]


class GeneratorTestCase(SimpleTestCase):
    """Cenários de geração de resposta com o cliente da Anthropic simulado."""

    def setUp(self):
        self.env = mock.patch.dict(
            "os.environ",
            {
                "ANTHROPIC_API_KEY": "chave-de-teste",
                "ANTHROPIC_MODEL": "claude-haiku-5-5",
                "LLM_MAX_RETRIES": "2",
                # Força os padrões do código, ignorando o .env da máquina.
                "LLM_SYSTEM_PROMPT": "",
                "LLM_FALLBACK_MESSAGE": "",
            },
        )
        self.env.start()
        generator._client = None
        self.addCleanup(self._stop)

    def _stop(self):
        generator._client = None
        self.env.stop()

    def _patch_client(self, client):
        patcher = mock.patch.object(generator, "Anthropic", return_value=client)
        patcher.start()
        self.addCleanup(patcher.stop)
        return client

    def test_resposta_gerada_com_sucesso(self):
        client = self._patch_client(_new_client_mock(_llm_response()))

        result = generator.generate_answer(
            "Posso devolver um produto?", context=CONTEXT, history=HISTORY
        )

        self.assertEqual(result.text, "Resposta da Nexus. [Fonte 1]")
        self.assertEqual(result.model, "claude-haiku-5-5")
        self.assertEqual(result.input_tokens, 120)
        self.assertEqual(result.output_tokens, 45)
        self.assertEqual(result.attempts, 1)
        self.assertFalse(result.fallback)
        self.assertGreaterEqual(result.latency_ms, 0)

    def test_envia_system_prompt_contexto_e_historico(self):
        client = self._patch_client(_new_client_mock(_llm_response()))

        generator.generate_answer(
            "Posso devolver um produto?", context=CONTEXT, history=HISTORY
        )

        kwargs = client.messages.create.call_args.kwargs
        self.assertIn("Nexus Atendimento", kwargs["system"])
        self.assertIn("[Fonte 1]", kwargs["system"])

        messages = kwargs["messages"]
        self.assertEqual([m["role"] for m in messages], ["user", "assistant", "user"])
        user_message = messages[-1]["content"]
        self.assertIn("[Fonte 1] Politica de devolucao.pdf", user_message)
        self.assertIn("[Fonte 2] Prazos.md", user_message)
        self.assertIn("Pergunta do cliente: Posso devolver um produto?", user_message)

    def test_contexto_e_historico_sao_opcionais(self):
        self._patch_client(_new_client_mock(_llm_response()))

        result = generator.generate_answer("Olá", context=[], history=None)

        self.assertFalse(result.fallback)
        self.assertEqual(result.attempts, 1)

    def test_retry_em_rate_limit(self):
        client = self._patch_client(
            _new_client_mock(
                _api_error(anthropic.RateLimitError, 429),
                _llm_response(),
            )
        )

        with mock.patch.object(generator.time, "sleep") as sleep:
            result = generator.generate_answer("Pergunta", context=CONTEXT)

        self.assertFalse(result.fallback)
        self.assertEqual(result.attempts, 2)
        self.assertEqual(client.messages.create.call_count, 2)
        sleep.assert_called_once()

    def test_retry_em_timeout(self):
        request = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")
        self._patch_client(
            _new_client_mock(
                anthropic.APITimeoutError(request=request),
                _llm_response(),
            )
        )

        with mock.patch.object(generator.time, "sleep"):
            result = generator.generate_answer("Pergunta", context=CONTEXT)

        self.assertFalse(result.fallback)
        self.assertEqual(result.attempts, 2)

    def test_erro_de_autenticacao_usa_fallback_sem_retry(self):
        client = self._patch_client(
            _new_client_mock(_api_error(anthropic.AuthenticationError, 401))
        )

        with mock.patch.object(generator.time, "sleep") as sleep:
            result = generator.generate_answer("Pergunta", context=CONTEXT)

        self.assertTrue(result.fallback)
        self.assertEqual(result.text, generator.FALLBACK_MESSAGE)
        self.assertEqual(client.messages.create.call_count, 1)
        sleep.assert_not_called()

    def test_tentativas_esgotadas_usa_fallback(self):
        self._patch_client(
            _new_client_mock(
                _api_error(anthropic.InternalServerError, 500),
                _api_error(anthropic.InternalServerError, 500),
                _api_error(anthropic.InternalServerError, 500),
            )
        )

        with mock.patch.object(generator.time, "sleep"):
            result = generator.generate_answer("Pergunta", context=CONTEXT)

        self.assertTrue(result.fallback)
        self.assertEqual(result.attempts, 3)

    def test_chave_ausente_usa_fallback_sem_chamar_o_provedor(self):
        with mock.patch.dict("os.environ", {"ANTHROPIC_API_KEY": ""}):
            client = self._patch_client(_new_client_mock(_llm_response()))
            result = generator.generate_answer("Pergunta", context=CONTEXT)

        self.assertTrue(result.fallback)
        self.assertEqual(result.attempts, 0)
        client.messages.create.assert_not_called()

    def test_fallback_nao_expoem_dados_internos(self):
        request = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")
        self._patch_client(
            _new_client_mock(anthropic.APIError("erro interno", request, body=None))
        )

        result = generator.generate_answer("Pergunta", context=CONTEXT)

        self.assertTrue(result.fallback)
        texto = result.text.lower()
        for segredo in ("anthropic", "api key", "chave", "traceback", "500"):
            self.assertNotIn(segredo, texto)

    def test_system_prompt_configuravel_por_variavel(self):
        client = self._patch_client(_new_client_mock(_llm_response()))

        with mock.patch.dict(
            "os.environ", {"LLM_SYSTEM_PROMPT": "Prompt personalizado da empresa."}
        ):
            generator.generate_answer("Pergunta", context=CONTEXT)

        self.assertEqual(
            client.messages.create.call_args.kwargs["system"],
            "Prompt personalizado da empresa.",
        )

    def test_fallback_configuravel_por_variavel(self):
        request = httpx2.Request("POST", "https://api.anthropic.com/v1/messages")
        self._patch_client(
            _new_client_mock(anthropic.APIError("erro interno", request, body=None))
        )

        with mock.patch.dict(
            "os.environ", {"LLM_FALLBACK_MESSAGE": "Serviço instável, tente mais tarde."}
        ):
            result = generator.generate_answer("Pergunta", context=CONTEXT)

        self.assertEqual(result.text, "Serviço instável, tente mais tarde.")

    def test_valores_do_env_example_sao_usados_pelo_generator(self):
        """Simula o .env real: o prompt e o fallback do .env.example devem valer."""
        from dotenv import dotenv_values

        from django.conf import settings

        valores = {
            chave: valor
            for chave, valor in dotenv_values(settings.BASE_DIR / ".env.example").items()
            if valor is not None
        }
        client = self._patch_client(_new_client_mock(_llm_response()))

        with mock.patch.dict("os.environ", valores):
            generator.generate_answer("Pergunta", context=CONTEXT)

        self.assertEqual(
            client.messages.create.call_args.kwargs["system"],
            valores["LLM_SYSTEM_PROMPT"],
        )


class SystemPromptTestCase(SimpleTestCase):
    """O system prompt precisa fixar papel, escopo, fontes e restrições."""

    def test_contem_papel_escopo_fontes_e_restricoes(self):
        prompt = generator.SYSTEM_PROMPT
        self.assertIn("Nexus Atendimento", prompt)
        self.assertIn("[Fonte 1]", prompt)
        self.assertIn("não possui essa informação", prompt)
        self.assertIn("RN10", prompt)
        self.assertIn("RN08", prompt)

    def test_env_example_documenta_system_prompt_e_fallback(self):
        """O .env.example é a fonte das variáveis de configuração (RNF Portabilidade)."""
        from dotenv import dotenv_values

        from django.conf import settings

        env_example = settings.BASE_DIR / ".env.example"
        valores = dotenv_values(env_example)

        texto = env_example.read_text(encoding="utf-8")
        self.assertIn("LLM_SYSTEM_PROMPT=", texto)
        self.assertIn("LLM_FALLBACK_MESSAGE=", texto)
        self.assertIn("LLM_SYSTEM_PROMPT", valores)
        self.assertIn("LLM_FALLBACK_MESSAGE", valores)
        # O valor precisa estar no formato aceito pelo python-dotenv.
        self.assertIn("Nexus Atendimento", valores["LLM_SYSTEM_PROMPT"])
        self.assertIn("não possui essa informação", valores["LLM_SYSTEM_PROMPT"])
        self.assertIn("atendente humano", valores["LLM_FALLBACK_MESSAGE"])
