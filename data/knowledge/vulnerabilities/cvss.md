# CVSS — Common Vulnerability Scoring System

## Definição

CVSS é uma metodologia utilizada para comunicar a severidade técnica de vulnerabilidades de segurança.

A pontuação auxilia na avaliação do risco técnico, mas não deve ser utilizada isoladamente para definir prioridade operacional.

---

## Faixas de Severidade

As pontuações CVSS são normalmente classificadas em categorias de severidade.

De forma geral:

- None: 0.0;
- Low: 0.1–3.9;
- Medium: 4.0–6.9;
- High: 7.0–8.9;
- Critical: 9.0–10.0.

A versão específica do CVSS deve ser considerada durante a análise.

---

## Métricas

A avaliação pode considerar fatores como:

- vetor de ataque;
- complexidade;
- privilégios necessários;
- interação do usuário;
- impacto sobre confidencialidade;
- impacto sobre integridade;
- impacto sobre disponibilidade.

---

## CVSS não é Risco Operacional

Uma vulnerabilidade com pontuação alta pode ter baixo risco operacional quando:

- o ativo não está exposto;
- o produto não está presente;
- existe mitigação eficaz;
- o sistema não é crítico.

Da mesma forma, uma vulnerabilidade com pontuação moderada pode ser altamente relevante quando afeta um ativo crítico ou amplamente exposto.

---

## Priorização

A organização deve combinar CVSS com:

- criticidade do ativo;
- exposição;
- existência de exploit;
- exploração observada;
- inteligência de ameaças;
- controles compensatórios.

---

## Uso pelo CyberSentinel AI

O agente pode auxiliar na interpretação da severidade.

Entretanto, não deve recomendar prioridade exclusivamente com base na pontuação CVSS.

A recomendação deve considerar o contexto fornecido pelo usuário.

---

## Observação

A pontuação CVSS deve ser interpretada de acordo com a versão utilizada e com as métricas correspondentes.
