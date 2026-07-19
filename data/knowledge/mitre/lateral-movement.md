# MITRE ATT&CK — Lateral Movement

## Definição

Lateral Movement representa técnicas utilizadas por adversários para movimentar-se de um sistema comprometido para outros sistemas dentro de um ambiente.

O objetivo pode ser alcançar ativos mais importantes, obter privilégios adicionais ou ampliar o comprometimento.

---

## Exemplos

Comportamentos relacionados incluem:

- uso de credenciais válidas;
- utilização de serviços remotos;
- movimentação entre hosts;
- acesso remoto administrativo;
- exploração de recursos internos.

---

## Evidências

Possíveis indicadores:

- autenticações entre hosts incomuns;
- uso inesperado de RDP ou SSH;
- conexões internas fora do padrão;
- acesso de uma conta a sistemas nunca utilizados anteriormente;
- atividade administrativa em horários incomuns.

---

## Investigação

A análise deve correlacionar:

- origem;
- destino;
- usuário;
- horário;
- protocolo;
- processo;
- histórico de comportamento.

---

## Mitigação

Medidas incluem:

- segmentação de rede;
- menor privilégio;
- MFA;
- administração segura;
- monitoramento de autenticações;
- restrição de protocolos remotos.

---

## Observação Analítica

Uma conexão entre dois sistemas internos não representa automaticamente movimento lateral.

O comportamento deve ser comparado ao padrão normal do ambiente.
