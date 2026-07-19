# MITRE ATT&CK

## Definição

MITRE ATT&CK é uma base de conhecimento pública que organiza comportamentos e técnicas utilizados por adversários durante operações cibernéticas.

O framework é utilizado por equipes de segurança para:

- threat hunting;
- detecção;
- investigação;
- análise de ameaças;
- avaliação de controles.

---

## Táticas

As táticas representam objetivos adversários.

Exemplos incluem:

- Initial Access;
- Execution;
- Persistence;
- Privilege Escalation;
- Defense Evasion;
- Credential Access;
- Discovery;
- Lateral Movement;
- Collection;
- Command and Control;
- Exfiltration;
- Impact.

---

## Técnicas

As técnicas descrevem maneiras pelas quais adversários podem alcançar seus objetivos.

Uma técnica pode possuir subtécnicas para representar comportamentos mais específicos.

---

## Uso na Investigação

Durante uma investigação, uma técnica deve ser associada somente quando existirem evidências compatíveis.

Exemplo:

```text
Evento observado:
Múltiplas tentativas de autenticação utilizando diferentes contas.

Possível interpretação:
Password Spraying.

Possível técnica:
T1110.003 — Password Spraying.
