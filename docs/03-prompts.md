# Prompt Engineering

O CyberSentinel AI utiliza uma arquitetura baseada em diferentes tipos de prompts, cada um com uma responsabilidade específica.

## Objetivos

- Definir o comportamento do agente.
- Padronizar respostas.
- Reduzir alucinações.
- Garantir respostas técnicas.
- Facilitar manutenção.

## Estrutura

System Prompt

Define identidade.

User Prompt

Representa perguntas do usuário.

Context

Informações recuperadas da Base de Conhecimento.

Response Template

Padroniza a saída.

Evaluation Prompt

Utilizado para validar respostas durante testes.

## Fluxo

Usuário

↓

Pergunta

↓

Contexto

↓

System Prompt

↓

LLM

↓

Resposta Padronizada