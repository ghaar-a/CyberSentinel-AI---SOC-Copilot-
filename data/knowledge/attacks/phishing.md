# Phishing

## Definição

Phishing é uma técnica de engenharia social utilizada para induzir uma vítima a realizar uma ação que favoreça o atacante.

O objetivo pode incluir:

- obtenção de credenciais;
- instalação de malware;
- execução de arquivos maliciosos;
- acesso a páginas fraudulentas;
- transferência de informações sensíveis;
- comprometimento de contas.

O phishing pode ocorrer por e-mail, mensagens instantâneas, redes sociais, SMS e outros canais de comunicação.

---

## Como Funciona

Um ataque de phishing normalmente utiliza uma mensagem que aparenta ser legítima.

O atacante pode tentar imitar:

- empresas;
- bancos;
- serviços de nuvem;
- equipes internas;
- provedores de tecnologia;
- instituições governamentais.

A mensagem pode conter:

- links fraudulentos;
- anexos maliciosos;
- solicitações urgentes;
- solicitações de pagamento;
- pedidos de atualização de credenciais.

---

## Indicadores

Possíveis indicadores incluem:

- domínio semelhante ao domínio legítimo;
- endereço de remetente suspeito;
- URL com domínio inesperado;
- linguagem de urgência;
- solicitação inesperada de credenciais;
- anexos não solicitados;
- redirecionamentos incomuns;
- páginas que imitam serviços legítimos.

Nenhum indicador isolado confirma um ataque.

A análise deve considerar o contexto completo da mensagem.

---

## Análise de URLs

Durante a análise, devem ser observados:

- domínio;
- subdomínio;
- protocolo;
- caminho da URL;
- redirecionamentos;
- presença de encurtadores;
- similaridade com domínios legítimos.

O uso de HTTPS não significa que um site seja legítimo.

HTTPS protege a comunicação entre cliente e servidor, mas não garante a legitimidade do domínio.

---

## Relação com MITRE ATT&CK

Phishing está associado à técnica:

- T1566 — Phishing.

Subtécnicas:

- T1566.001 — Spearphishing Attachment;
- T1566.002 — Spearphishing Link;
- T1566.003 — Spearphishing via Service;
- T1566.004 — Spearphishing Voice.

---

## Mitigação

Medidas recomendadas incluem:

- treinamento de usuários;
- autenticação multifator;
- filtros de e-mail;
- análise de URLs;
- sandboxing de anexos;
- proteção de endpoints;
- DMARC, DKIM e SPF;
- monitoramento de domínios similares.

---

## Resposta a Incidentes

Quando um phishing for identificado:

1. Preservar a mensagem original.
2. Analisar remetente e cabeçalhos.
3. Verificar URLs e anexos.
4. Identificar usuários afetados.
5. Determinar se houve interação.
6. Verificar possível comprometimento de credenciais.
7. Revogar sessões quando necessário.
8. Redefinir credenciais comprometidas.
9. Bloquear indicadores maliciosos.
10. Investigar atividades posteriores.

---

## Observação Analítica

Uma mensagem suspeita não é automaticamente maliciosa.

A classificação deve considerar evidências técnicas, contexto e comportamento observado.
