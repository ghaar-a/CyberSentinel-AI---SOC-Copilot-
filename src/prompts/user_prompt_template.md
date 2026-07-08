# CyberSentinel AI — User Prompt Template

Você recebeu uma solicitação de análise de um usuário.

Sua resposta deve ser construída utilizando obrigatoriamente:

1. O System Prompt.
2. Os Guardrails.
3. A Base de Conhecimento fornecida.
4. Os dados enviados pelo usuário.

Nunca ignore nenhuma dessas fontes.

---

## Contexto Recuperado da Base de Conhecimento

{{knowledge_base_context}}

---

## Histórico da Conversa (Opcional)

{{conversation_history}}

Caso não exista histórico, desconsidere esta seção.

---

## Dados Fornecidos pelo Usuário

{{user_data}}

Esses dados podem conter:

- logs de segurança;
- eventos em formato JSON;
- trechos de arquivos CSV;
- indicadores de comprometimento (IOCs);
- endereços IP;
- hashes;
- domínios;
- URLs;
- identificadores MITRE ATT&CK;
- identificadores CVE;
- perguntas em linguagem natural.

---

## Pergunta do Usuário

{{user_question}}

---

## Objetivo

Analise cuidadosamente todas as informações fornecidas.

Utilize prioritariamente a Base de Conhecimento.

Sempre identifique possíveis relações entre os dados enviados e o conhecimento disponível.

Caso não existam informações suficientes para responder, informe explicitamente essa limitação.

Nunca invente informações para preencher lacunas.

Produza sua resposta seguindo exatamente o Response Template definido pela aplicação.