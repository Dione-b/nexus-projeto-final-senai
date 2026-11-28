# **Storybook do projeto — Atendimento Inteligente com RAG**

## **1. Visão do produto**

Desenvolver uma plataforma inteligente de atendimento ao cliente para uma empresa fictícia, utilizando Retrieval-Augmented Generation (RAG) para fornecer respostas contextualizadas com base nos documentos, políticas, produtos e serviços da organização.

A solução disponibilizará dois canais de atendimento, Web e Telegram, compartilhando a mesma infraestrutura de processamento, conhecimento e gerenciamento de conversas.

| Característica    | Definição                      |
| ----------------- | ------------------------------ |
| Nome fictício     | Nexus Atendimento              |
| Segmento          | Atendimento ao cliente         |
| Produto           | Assistente virtual inteligente |
| Público-alvo      | Clientes e administradores     |
| Plataformas       | Web e Telegram                 |
| Interface         | Mobile-first                   |
| Tecnologia de IA  | RAG                            |
| Modelo de entrega | MVP                            |

## **2. Arquitetura do sistema**

Arquitetura centralizada com múltiplos canais de atendimento e armazenamento relacional e vetorial na mesma instância PostgreSQL.

## **3. Stack tecnológica**

| Tecnologia           | Responsabilidade                  |
| -------------------- | --------------------------------- |
| Python               | Linguagem principal               |
| Django               | Backend e regras de negócio       |
| Django Templates     | Renderização das interfaces       |
| HTMX                 | Interatividade no frontend        |
| HTML e CSS           | Interface mobile-first            |
| PostgreSQL           | Persistência relacional           |
| pgvector             | Armazenamento e busca vetorial    |
| Telegram Bot API     | Integração com Telegram           |
| LLM                  | Geração de respostas              |
| Modelo de embeddings | Representação vetorial dos textos |

## **4. Personas**

**Cliente**

Deseja esclarecer dúvidas sobre produtos, serviços e políticas da empresa sem depender inicialmente de um atendente humano.

**Administrador**

Responsável por cadastrar documentos, atualizar a base de conhecimento, acompanhar atendimentos e avaliar a qualidade das respostas.

## **5. Storyboard — Jornada do usuário**

**Cena 01 — Acesso**

O cliente acessa a plataforma Web pelo celular ou inicia uma conversa pelo Telegram.

**Cena 02 — Solicitação**

O cliente envia uma pergunta sobre a política de devolução da empresa.

**Cena 03 — Processamento**

O backend recebe a pergunta. O RAG recupera os trechos relevantes dos documentos da empresa e os encaminha ao modelo de linguagem.

**Cena 04 — Resposta**

O cliente recebe uma resposta fundamentada na base de conhecimento, com referência ao documento consultado.

**Cena 05 — Monitoramento**

O administrador acompanha o atendimento, verifica as fontes utilizadas e analisa o feedback recebido.

## **6. Épicos e User Stories**

### **Épico 01 — Atendimento Web**

| ID   | História de usuário                                       | Prioridade |
| ---- | --------------------------------------------------------- | ---------- |
| US01 | Como cliente, quero acessar o atendimento pelo navegador. | Alta       |
| US02 | Como cliente, quero enviar perguntas e receber respostas. | Alta       |
| US03 | Como cliente, quero utilizar o chat pelo celular.         | Alta       |
| US04 | Como cliente, quero consultar meu histórico de conversas. | Média      |
| US05 | Como cliente, quero avaliar as respostas recebidas.       | Média      |

### **Épico 02 — Atendimento via Telegram**

| ID   | História de usuário                                              | Prioridade |
| ---- | ---------------------------------------------------------------- | ---------- |
| US06 | Como cliente, quero iniciar um atendimento pelo Telegram.        | Alta       |
| US07 | Como cliente, quero receber respostas contextualizadas pelo bot. | Alta       |
| US08 | Como cliente, quero manter o contexto durante uma conversa.      | Alta       |
| US09 | Como cliente, quero iniciar uma nova conversa.                   | Média      |

### **Épico 03 — Base de conhecimento**

| ID   | História de usuário                                              | Prioridade |
| ---- | ---------------------------------------------------------------- | ---------- |
| US10 | Como administrador, quero cadastrar documentos.                  | Alta       |
| US11 | Como administrador, quero indexar os documentos automaticamente. | Alta       |
| US12 | Como administrador, quero atualizar documentos existentes.       | Alta       |
| US13 | Como administrador, quero excluir documentos obsoletos.          | Alta       |
| US14 | Como administrador, quero visualizar o estado da indexação.      | Média      |

### **Épico 04 — Inteligência Artificial e RAG**

| ID   | História de usuário                                                        | Prioridade |
| ---- | -------------------------------------------------------------------------- | ---------- |
| US15 | Como cliente, quero respostas fundamentadas nos documentos da empresa.     | Alta       |
| US16 | Como cliente, quero identificar as fontes das respostas.                   | Alta       |
| US17 | Como cliente, quero ser informado quando não houver informação suficiente. | Alta       |
| US18 | Como administrador, quero impedir respostas fora do escopo da empresa.     | Alta       |
| US19 | Como administrador, quero configurar parâmetros de recuperação.            | Média      |

### **Épico 05 — Administração e governança**

| ID   | História de usuário                                                   | Prioridade |
| ---- | --------------------------------------------------------------------- | ---------- |
| US20 | Como administrador, quero acessar um painel administrativo.           | Alta       |
| US21 | Como administrador, quero consultar os atendimentos realizados.       | Alta       |
| US22 | Como administrador, quero monitorar falhas de processamento.          | Média      |
| US23 | Como administrador, quero acompanhar avaliações das respostas.        | Média      |
| US24 | Como administrador, quero identificar tentativas de Prompt Injection. | Alta       |
| US25 | Como administrador, quero gerenciar permissões de acesso.             | Alta       |

## **7. Funcionamento do RAG**

O RAG será dividido em dois processos independentes: ingestão de conhecimento e recuperação de informação.

**Pipeline de ingestão**

**Pipeline de recuperação**

## **8. Modelagem de dados**

\#chatgpt-mermaid-\_r_5m\_{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;fill:rgb(13, 13, 13);}@keyframes edge-animation-frame{from{stroke-dashoffset:0;}}@keyframes dash{to{stroke-dashoffset:0;}}#chatgpt-mermaid-\_r_5m\_ .edge-animation-slow{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 50s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_5m\_ .edge-animation-fast{stroke-dasharray:9,5!important;stroke-dashoffset:900;animation:dash 20s linear infinite;stroke-linecap:round;}#chatgpt-mermaid-\_r_5m\_ .error-icon{fill:rgb(243, 243, 243);}#chatgpt-mermaid-\_r_5m\_ .error-text{fill:rgb(13, 13, 13);stroke:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_5m\_ .edge-thickness-normal{stroke-width:1px;}#chatgpt-mermaid-\_r_5m\_ .edge-thickness-thick{stroke-width:3.5px;}#chatgpt-mermaid-\_r_5m\_ .edge-pattern-solid{stroke-dasharray:0;}#chatgpt-mermaid-\_r_5m\_ .edge-thickness-invisible{stroke-width:0;fill:none;}#chatgpt-mermaid-\_r_5m\_ .edge-pattern-dashed{stroke-dasharray:3;}#chatgpt-mermaid-\_r_5m\_ .edge-pattern-dotted{stroke-dasharray:2;}#chatgpt-mermaid-\_r_5m\_ .marker{fill:rgb(143, 143, 143);stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_5m\_ .marker.cross{stroke:rgb(143, 143, 143);}#chatgpt-mermaid-\_r_5m\_ svg{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";font-size:16px;}#chatgpt-mermaid-\_r_5m\_ p{margin:0;}#chatgpt-mermaid-\_r_5m\_ .entityBox{fill:rgb(222, 234, 251);stroke:rgb(83, 154, 248);}#chatgpt-mermaid-\_r_5m\_ .relationshipLabelBox{fill:rgb(243, 243, 243);opacity:0.7;background-color:rgb(243, 243, 243);}#chatgpt-mermaid-\_r_5m\_ .relationshipLabelBox rect{opacity:0.5;}#chatgpt-mermaid-\_r_5m\_ .labelBkg{background-color:rgba(243, 243, 243, 0.5);}#chatgpt-mermaid-\_r_5m\_ .edgeLabel{background-color:rgb(252, 252, 252);}#chatgpt-mermaid-\_r_5m\_ .edgeLabel .label rect{fill:rgb(252, 252, 252);}#chatgpt-mermaid-\_r_5m\_ .edgeLabel .label text{fill:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_5m\_ .edgeLabel .label{fill:rgb(83, 154, 248);font-size:14px;}#chatgpt-mermaid-\_r_5m\_ .label{font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";color:rgb(13, 13, 13);}#chatgpt-mermaid-\_r_5m\_ .edge-pattern-dashed{stroke-dasharray:8,8;}#chatgpt-mermaid-\_r_5m\_ .node rect,#chatgpt-mermaid-\_r_5m\_ .node circle,#chatgpt-mermaid-\_r_5m\_ .node ellipse,#chatgpt-mermaid-\_r_5m\_ .node polygon{fill:rgb(222, 234, 251);stroke:rgb(83, 154, 248);stroke-width:1px;}#chatgpt-mermaid-\_r_5m\_ .relationshipLine{stroke:rgb(143, 143, 143);stroke-width:1px;fill:none;}#chatgpt-mermaid-\_r_5m\_ .marker{fill:none!important;stroke:rgb(143, 143, 143)!important;stroke-width:1;}#chatgpt-mermaid-\_r_5m\_ [data-look=neo].labelBkg{background-color:rgba(243, 243, 243, 0.5);}#chatgpt-mermaid-\_r_5m\_ .node .neo-node{stroke:rgb(83, 154, 248);}#chatgpt-mermaid-\_r_5m\_ [data-look="neo"].node rect,#chatgpt-mermaid-\_r_5m\_ [data-look="neo"].cluster rect,#chatgpt-mermaid-\_r_5m\_ [data-look="neo"].node polygon{stroke:url(#chatgpt-mermaid-\_r_5m\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_5m\_ [data-look="neo"].swimlane.cluster rect{filter:none;}#chatgpt-mermaid-\_r_5m\_ [data-look="neo"].node path{stroke:url(#chatgpt-mermaid-\_r_5m\_-gradient);stroke-width:1px;}#chatgpt-mermaid-\_r_5m\_ [data-look="neo"].node .outer-path{filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_5m\_ [data-look="neo"].node .neo-line path{stroke:rgb(83, 154, 248);filter:none;}#chatgpt-mermaid-\_r_5m\_ [data-look="neo"].node circle{stroke:url(#chatgpt-mermaid-\_r_5m\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_5m\_ [data-look="neo"].node circle .state-start{fill:#000000;}#chatgpt-mermaid-\_r_5m\_ [data-look="neo"].icon-shape .icon{fill:url(#chatgpt-mermaid-\_r_5m\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_5m\_ [data-look="neo"].icon-shape .icon-neo path{stroke:url(#chatgpt-mermaid-\_r_5m\_-gradient);filter:drop-shadow( 1px 2px 2px rgba(185,185,185,1));}#chatgpt-mermaid-\_r_5m\_ :root{--mermaid-font-family:-apple-system-body,ui-sans-serif,-apple-system,system-ui,"Segoe UI",Helvetica,"Apple Color Emoji",Arial,sans-serif,"Segoe UI Emoji","Segoe UI Symbol";}USERintidPKstringnamestringemailstringroleCONVERSATIONintidPKintuser_idFKstringchanneldatetimecreated_atMESSAGEintidPKintconversation_idFKstringroletextcontentdatetimecreated_atDOCUMENTintidPKstringtitlestringstatusdatetimecreated_atCHUNKintidPKintdocument_idFKtextcontentvectorembeddingRETRIEVALintidPKintmessage_idFKintchunk_idFKfloatsimilarityFEEDBACKintidPKintmessage_idFKintratingtextcommentpossuicontempossuiutilizarecuperadorecebe

O PostgreSQL será responsável tanto pelos dados transacionais quanto pelos embeddings, evitando a necessidade de manter dois serviços de banco de dados.

## **9. Organização do projeto**

```
nexus/
├── manage.py
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── apps/
│   ├── accounts/
│   ├── conversations/
│   ├── knowledge/
│   ├── rag/
│   │   ├── ingestion.py
│   │   ├── chunking.py
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   ├── generator.py
│   │   ├── pipeline.py
│   │   └── guardrails.py
│   │
│   ├── telegram/
│   ├── feedback/
│   └── monitoring/
│
├── templates/
│   ├── base.html
│   ├── chat/
│   ├── partials/
│   └── dashboard/
│
├── static/
│   ├── css/
│   └── js/
│
├── tests/
├── documents/
├── requirements.txt
├── docker-compose.yml
├── .env.example
└── README.md
```

A organização segue uma arquitetura de monólito modular, separando responsabilidades sem introduzir a complexidade de microsserviços.

## **10. Regras de negócio**

| ID   | Regra                                                                                         |
| ---- | --------------------------------------------------------------------------------------------- |
| RN01 | Apenas administradores podem gerenciar a base de conhecimento.                                |
| RN02 | Documentos não indexados não podem participar da recuperação.                                 |
| RN03 | Respostas factuais sobre a empresa devem ser fundamentadas nas fontes recuperadas.            |
| RN04 | O sistema deve informar quando não possuir conhecimento suficiente.                           |
| RN05 | Conversas de clientes distintos devem permanecer isoladas.                                    |
| RN06 | Os canais Web e Telegram devem utilizar o mesmo pipeline RAG.                                 |
| RN07 | Documentos excluídos devem deixar de participar das buscas.                                   |
| RN08 | Informações sensíveis não devem ser expostas nas respostas.                                   |
| RN09 | Cada resposta deve possuir um registro para auditoria.                                        |
| RN10 | Instruções presentes nos documentos recuperados devem ser tratadas como dados não confiáveis. |

## **11. Requisitos não funcionais**

| Categoria        | Requisito                                   |
| ---------------- | ------------------------------------------- |
| Usabilidade      | Interface responsiva e mobile-first         |
| Segurança        | Autenticação e controle de acesso           |
| Privacidade      | Minimização e proteção de dados pessoais    |
| Manutenibilidade | Separação de responsabilidades              |
| Desempenho       | Indexação e recuperação vetorial eficientes |
| Confiabilidade   | Tratamento de falhas da LLM e integrações   |
| Observabilidade  | Logs, latência, erros e métricas            |
| Governança       | Rastreabilidade das respostas               |
| Portabilidade    | Configuração por variáveis de ambiente      |

## **12. Roadmap de desenvolvimento**

Progresso do projeto

# **24%**

6 de 25 tarefas

**Sprint 01 — Fundação**

4/4

Configurar Django

Configurar PostgreSQL e pgvector

Criar modelos relacionais

Configurar Django Admin

**Sprint 02 — Base de conhecimento**

1/4

Implementar upload de documentos

Implementar extração e chunking

Gerar embeddings

Implementar indexação vetorial

**Sprint 03 — RAG**

1/4

Implementar busca semântica

Construir contexto

Integrar LLM

Implementar pipeline de respostas

**Sprint 04 — Atendimento Web**

0/4

Construir interface mobile-first

Integrar HTMX

Implementar conversas

Exibir respostas e fontes

**Sprint 05 — Telegram**

0/4

Configurar bot

Implementar integração

Gerenciar sessões

Reutilizar pipeline RAG

**Sprint 06 — Segurança e qualidade**

0/5

Implementar guardrails

Testar Prompt Injection

Implementar feedback e monitoramento

Executar testes de integração

Documentar a aplicação

&#x20;Copiar checklist

## **13. Critérios de aceitação do MVP**

O projeto será considerado funcional quando atender aos seguintes cenários:

| Cenário                            | Resultado esperado                                     |
| ---------------------------------- | ------------------------------------------------------ |
| Cadastro de documento              | Conteúdo extraído e indexado                           |
| Pergunta com informação disponível | Resposta fundamentada e fonte identificada             |
| Pergunta sem informação disponível | Comunicação explícita da insuficiência de conhecimento |
| Atendimento Web                    | Conversa funcional em desktop e mobile                 |
| Atendimento Telegram               | Resposta utilizando o mesmo RAG da Web                 |
| Exclusão de documento              | Conteúdo removido da recuperação                       |
| Prompt Injection                   | Tentativa de manipulação bloqueada ou neutralizada     |
| Falha da LLM                       | Erro tratado sem exposição de dados internos           |
| Histórico                          | Mensagens persistidas e isoladas por usuário           |

## **14. Escopo do MVP**

&#x20;Dentro do escopo

Atendimento Web

Atendimento Telegram

Base de conhecimento

Busca semântica

Pipeline RAG

Painel administrativo

Guardrails básicos

Histórico de conversas

&#x20;Fora do escopo

Atendimento por voz

Fine-tuning de modelos

Sistemas multiagentes

Integração com CRM

Aplicativos mobile nativos

Arquitetura de microsserviços

Atendimento humano integrado

Arquitetura multi-tenant

## **15. Decisões arquiteturais pendentes**

Algumas definições não foram fornecidas inicialmente. Adotei o nome fictício Nexus, uma arquitetura de monólito modular, pgvector e Django Templates como propostas para simplificar o desenvolvimento.

Decisões registradas:

- **Provedor e modelo de LLM:** Anthropic (família Claude), consumido pela API oficial da Anthropic (`anthropic`). O modelo é configurável por `ANTHROPIC_MODEL` (padrão `claude-haiku-5-5`), a chave por `ANTHROPIC_API_KEY`, e o system prompt e a mensagem de fallback por `LLM_SYSTEM_PROMPT` e `LLM_FALLBACK_MESSAGE` (ver `.env.example`). Detalhes na issue #28 e implementação em `apps/rag/generator.py` (issue #11).

Ainda precisam ser definidos:

- Modelo de embeddings.
- Estratégia de chunking e recuperação.
- Segmento comercial da empresa fictícia.
- Autenticação dos clientes e identificação entre canais.
- Infraestrutura de hospedagem.
- Métricas e limites aceitáveis de qualidade, custo e latência.

A proposta é manter o projeto suficientemente completo para exercitar desenvolvimento full-stack, integração com IA generativa, RAG, bancos vetoriais, segurança e governança, sem adicionar complexidade arquitetural desnecessária.
