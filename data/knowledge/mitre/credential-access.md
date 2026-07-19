# MITRE ATT&CK — Credential Access

## Definição

Credential Access representa técnicas utilizadas para obter credenciais ou informações relacionadas à autenticação.

Essas técnicas podem permitir que adversários obtenham acesso adicional a sistemas e contas.

---

## Exemplos de Técnicas

Exemplos incluem:

- Brute Force;
- Credentials from Password Stores;
- OS Credential Dumping;
- Phishing;
- Steal Web Session Cookie.

---

## Evidências

Possíveis indicadores incluem:

- tentativas anômalas de autenticação;
- acesso incomum a armazenamentos de credenciais;
- execução de ferramentas suspeitas;
- comportamento inesperado de contas privilegiadas;
- reutilização de credenciais comprometidas.

---

## Investigação

O analista deve avaliar:

- qual conta foi afetada;
- quais credenciais podem ter sido expostas;
- quais sistemas utilizam essas credenciais;
- se houve autenticação posterior;
- se houve escalonamento de privilégios.

---

## Mitigação

Controles relevantes incluem:

- MFA;
- menor privilégio;
- proteção de credenciais;
- rotação de segredos;
- monitoramento de autenticação;
- políticas de acesso condicional.

---

## Observação Analítica

A suspeita de Credential Access deve ser baseada em evidências observáveis.

Uma falha isolada de autenticação não confirma comprometimento de credenciais.
