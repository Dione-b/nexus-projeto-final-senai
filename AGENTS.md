# AGENTS.md — Instruções para agentes

## Instrução principal

**Todo trabalho neste repositório deve seguir o `README.md`.**

O `README.md` é a fonte única de verdade do projeto **Nexus Atendimento** (Storybook do projeto — Atendimento Inteligente com RAG). Antes de começar qualquer tarefa, leia o `README.md` completo e use-o como referência para decisões de arquitetura, escopo, regras de negócio e prioridades.

## Ordem de leitura obrigatória

1. `README.md` — inteiro.
2. Somente depois, explore o código ou proponha mudanças.

## Regras ao seguir o README

- **Escopo (seção 14):** implemente apenas o que está "Dentro do escopo". Não crie recursos listados em "Fora do escopo" (voz, fine-tuning, multiagente, CRM, app nativo, microsserviços, multi-tenant etc.).
- **Stack (seção 3):** use exatamente as tecnologias definidas — Python, Django, Django Templates, HTMX, HTML/CSS mobile-first, PostgreSQL + pgvector, Telegram Bot API, LLM e modelo de embeddings. Não substitua sem justificativa e sem registrar a decisão.
- **Estrutura (seção 9):** respeite a organização do projeto (monólito modular com `config/`, `apps/`, `templates/`, `static/`, `tests/`, `documents/`). Crie código nos apps corretos:
  - `apps/accounts` — usuários e permissões
  - `apps/conversations` — conversas e mensagens
  - `apps/knowledge` — base de conhecimento (documentos)
  - `apps/rag` — `ingestion.py`, `chunking.py`, `embeddings.py`, `retriever.py`, `generator.py`, `pipeline.py`, `guardrails.py`
  - `apps/telegram` — canal Telegram
  - `apps/feedback` — avaliações
  - `apps/monitoring` — logs e métricas
- **Regras de negócio (seção 10):** trate RN01–RN10 como requisitos não negociáveis. Toda implementação relevante deve ser verificada contra elas (ex.: RN05 isolamento de conversas, RN06 mesmo pipeline RAG para Web e Telegram, RN10 documentos são dados não confiáveis).
- **User Stories (seção 6):** entregue no ordem de prioridade (Alta antes de Média) e agrupe o trabalho nos épicos correspondentes.
- **Roadmap (seção 12):** trabalhe sprint a sprint, na ordem — Fundação → Base de conhecimento → RAG → Atendimento Web → Telegram → Segurança e qualidade. Atualize o progresso no `README.md` (contador de tarefas) a cada sprint concluída.
- **Critérios de aceitação (seção 13):** cada entrega deve ser validada contra os cenários da tabela antes de ser considerada pronta.
- **Requisitos não funcionais (seção 11):** mobilidade por variáveis de ambiente (`.env.example`), configuração portável, logs/erros/métricas e rastreabilidade das respostas fazem parte da definição de pronto.
- **Decisões pendentes (seção 15):** provedor de LLM, modelo de embeddings, estratégia de chunking, autenticação entre canais, hospedagem e métricas ainda não estão definidos. Não presuma uma escolha silenciosamente — pergunte ao usuário ou registre a decisão no `README.md`.

## Regras gerais de trabalho

- **Simplicidade:** sempre busque o código mais simples possível e de fácil leitura humana. Prefira soluções diretas a abstrações desnecessárias.
- **Segurança e boas práticas:** implemente sempre boas práticas de segurança e desenvolvimento (validação de entrada, tratamento seguro de erros, não confiar em dados externos, seguir as convenções do projeto).
- **Dúvidas:** em caso de dúvida, sempre pergunte ao usuário antes de assumir uma direção.
- **Commit:** ao final de cada implementação, apresente uma mensagem de commit (padrão convencional, em português) para o usuário.
- **Branch por issue:** ao final de cada implementação, pergunte ao usuário se deseja criar uma branch com o nome da issue e commitar as alterações nela. Só crie a branch e faça o commit após a confirmação do usuário.
- **Gitflow:** sempre buscar seguir os conceitos de gitflow — `main` para produção, `develop` para integração, `feature/*` para novas funcionalidades, `release/*` para preparação de versão e `hotfix/*` para correções urgentes. Não commitar diretamente em `main` ou `develop`.
- **Paralelismo:** sempre utilize paralelismo (chamadas de ferramentas, tarefas ou subagentes concorrentes) sempre que possível para acelerar o trabalho.
- **Variáveis de ambiente:** nunca suba arquivos de variáveis de ambiente (`.env`, `.env.local` etc.) para a branch — mantenha apenas o `.env.example` (sem valores reais) versionado.

## Expectativas de trabalho

- Mantenha o `README.md` atualizado sempre que o escopo, a estrutura, o progresso ou uma decisão arquitetural mudar.
- Não remova nem reescreva seções do `README.md` sem pedido explícito.
- Siga o estilo e a estrutura existentes no código; não reescreva partes funcionais sem necessidade.
- Prefira soluções simples e modulares: o README pede monólito modular, não microsserviços nem complexidade arquitetural desnecessária.
- Confirme com o usuário antes de tomar qualquer uma das decisões pendentes da seção 15.
