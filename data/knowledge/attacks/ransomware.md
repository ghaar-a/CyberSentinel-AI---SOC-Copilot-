# Ransomware

## Definição

Ransomware é um tipo de malware utilizado para impedir ou dificultar o acesso a dados e sistemas.

Em muitos casos, o atacante utiliza criptografia para tornar arquivos inacessíveis e exige pagamento para supostamente restaurar o acesso.

Campanhas modernas também podem envolver exfiltração de dados e extorsão.

---

## Funcionamento

Um ataque de ransomware pode envolver várias etapas:

1. Acesso inicial.
2. Comprometimento de sistemas.
3. Persistência.
4. Descoberta do ambiente.
5. Movimento lateral.
6. Escalonamento de privilégios.
7. Exfiltração de dados.
8. Criptografia ou destruição de dados.
9. Extorsão.

Nem todas as campanhas seguem exatamente essa sequência.

---

## Indicadores

Possíveis evidências incluem:

- grande quantidade de arquivos modificados;
- alterações repentinas em extensões;
- criação de notas de resgate;
- processos incomuns;
- desativação de mecanismos de segurança;
- atividade anormal de contas privilegiadas;
- uso de ferramentas administrativas fora do padrão;
- conexões suspeitas;
- transferência anormal de dados.

---

## Relação com MITRE ATT&CK

Ransomware não representa uma única técnica MITRE ATT&CK.

Dependendo do comportamento observado, podem existir técnicas relacionadas a:

- Initial Access;
- Execution;
- Persistence;
- Privilege Escalation;
- Defense Evasion;
- Credential Access;
- Discovery;
- Lateral Movement;
- Collection;
- Exfiltration;
- Impact.

A técnica deve ser atribuída com base na evidência observada.

---

## Mitigação

Medidas importantes incluem:

- backups offline ou imutáveis;
- segmentação de rede;
- MFA;
- princípio do menor privilégio;
- atualização de sistemas;
- EDR;
- monitoramento de endpoints;
- controle de aplicações;
- treinamento de usuários;
- plano de resposta a incidentes.

---

## Resposta a Incidentes

Em caso de suspeita:

1. Isolar sistemas afetados.
2. Preservar evidências.
3. Identificar o vetor inicial.
4. Determinar o escopo do comprometimento.
5. Avaliar possíveis credenciais comprometidas.
6. Verificar movimento lateral.
7. Proteger backups.
8. Investigar exfiltração.
9. Erradicar a ameaça.
10. Restaurar sistemas de forma controlada.

A decisão de desligar sistemas deve considerar preservação de evidências e continuidade operacional.

---

## Observação Analítica

A presença de arquivos criptografados não é suficiente para determinar automaticamente a família de ransomware ou o grupo responsável.

A atribuição deve depender de evidências adicionais.
