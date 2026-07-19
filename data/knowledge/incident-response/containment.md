# Contenção de Incidentes

## Definição

Contenção é o conjunto de ações destinadas a limitar o impacto e a propagação de um incidente de segurança.

O objetivo é impedir que o incidente continue causando danos enquanto a investigação prossegue.

---

## Tipos de Contenção

### Contenção de Curto Prazo

Busca reduzir rapidamente o impacto.

Exemplos:

- isolamento de endpoint;
- bloqueio temporário de IP;
- suspensão de conta;
- bloqueio de domínio;
- interrupção de comunicação suspeita.

### Contenção de Longo Prazo

Busca manter o ambiente operacional enquanto a causa do incidente é investigada.

Exemplos:

- segmentação de rede;
- aplicação de controles adicionais;
- restrição de privilégios;
- monitoramento reforçado.

---

## Critérios de Decisão

A escolha da estratégia deve considerar:

- criticidade do ativo;
- extensão do comprometimento;
- risco de propagação;
- impacto operacional;
- requisitos legais;
- preservação de evidências.

---

## Exemplos

Em um possível comprometimento de endpoint:

1. Isolar o dispositivo da rede.
2. Preservar evidências.
3. Identificar usuário e ativo.
4. Investigar processos e conexões.
5. Determinar se outros sistemas foram afetados.

Em um possível comprometimento de conta:

1. Suspender ou proteger a conta.
2. Revogar sessões.
3. Redefinir credenciais.
4. Verificar MFA.
5. Analisar atividades recentes.

---

## Observação Analítica

A contenção não significa necessariamente desligar imediatamente todos os sistemas.

A decisão deve considerar o risco de propagação, continuidade operacional e necessidade de preservar evidências.
