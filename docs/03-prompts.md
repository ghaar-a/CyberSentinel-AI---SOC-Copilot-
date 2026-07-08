# Prompt Engineering

## Objetivo

O CyberSentinel AI utiliza uma arquitetura de prompts modular para garantir respostas consistentes, reduzir ambiguidades e facilitar a manutenção do agente.

Em vez de concentrar todas as instruções em um único prompt, cada componente possui uma responsabilidade específica. Essa abordagem segue boas práticas utilizadas em plataformas modernas de desenvolvimento de agentes de Inteligência Artificial.

A modularização permite evoluir o projeto sem alterar o comportamento global do assistente, facilitando futuras integrações com Retrieval-Augmented Generation (RAG), bancos vetoriais, ferramentas externas e múltiplos agentes.

---

# Arquitetura dos Prompts

O CyberSentinel AI organiza suas instruções em cinco componentes principais.

| Componente | Responsabilidade |
|------------|------------------|
| Guardrails | Define regras obrigatórias que nunca podem ser violadas. |
| System Prompt | Define identidade, objetivos, comportamento e estratégia de raciocínio do agente. |
| Knowledge Context | Injeta documentos recuperados da Base de Conhecimento para fornecer contexto especializado durante a geração da resposta. |
| User Prompt | Contém a pergunta do usuário e os dados enviados para análise. |
| Response Template | Padroniza o formato da resposta produzida pelo modelo. |

---

# Fluxo de Execução

O processamento das perguntas segue a sequência abaixo.

```text
Usuário
        │
        ▼
User Prompt
        │
        ▼
Knowledge Loader
        │
        ▼
Knowledge Context
        │
        ▼
Guardrails
        │
        ▼
System Prompt
        │
        ▼
Large Language Model
        │
        ▼
Response Template
        │
        ▼
Resposta Final
```

---

# Hierarquia das Instruções

Os componentes possuem níveis diferentes de prioridade.

1. Guardrails
2. System Prompt
3. Knowledge Context
4. User Prompt
5. Response Template

Caso exista conflito entre instruções, o modelo deve obedecer sempre ao componente de maior prioridade.

---

# Modular Prompting

Cada prompt possui apenas uma responsabilidade.

Essa separação reduz redundâncias, melhora a reutilização dos arquivos e simplifica futuras alterações.

A arquitetura também facilita testes independentes de cada componente, permitindo validar comportamento, segurança e qualidade das respostas de forma isolada.

---

# Integração com a Base de Conhecimento

O Knowledge Context é responsável por fornecer ao modelo os documentos relevantes recuperados da Base de Conhecimento.

Esses documentos são carregados dinamicamente durante a execução da aplicação e inseridos antes da pergunta do usuário.

Dessa forma, o modelo utiliza prioritariamente informações específicas do projeto em vez de depender exclusivamente de seu conhecimento pré-treinado.

---

# Benefícios da Arquitetura

A arquitetura adotada oferece diversas vantagens:

- Redução de alucinações.
- Respostas mais consistentes.
- Facilidade de manutenção.
- Separação entre regras, comportamento e contexto.
- Facilidade para evolução futura com RAG.
- Melhor rastreabilidade durante testes.
- Reutilização dos prompts em diferentes aplicações.

---

# Estrutura dos Arquivos

```text
src/
└── prompts/
    ├── guardrails.md
    ├── system_prompt.md
    ├── user_prompt_template.md
    ├── response_template.md
    └── evaluation_prompt.md
```

Cada arquivo possui uma responsabilidade única e pode ser atualizado independentemente dos demais.