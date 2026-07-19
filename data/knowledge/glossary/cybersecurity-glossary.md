# Glossário de Cyber Security

## IOC — Indicator of Compromise

Indicador de Comprometimento é uma evidência que pode estar associada a uma atividade maliciosa.

Exemplos:

- endereço IP;
- domínio;
- URL;
- hash de arquivo;
- nome de arquivo;
- artefato de sistema.

Um IOC isolado não confirma necessariamente um comprometimento.

---

## IOA — Indicator of Attack

Indicador de Ataque representa um comportamento ou padrão que pode indicar atividade maliciosa.

Exemplos:

- execução anômala de processos;
- comportamento incomum de autenticação;
- movimentação lateral suspeita.

IOAs são orientados ao comportamento, enquanto IOCs normalmente representam artefatos observáveis.

---

## SIEM

Security Information and Event Management.

Plataforma utilizada para centralizar, correlacionar e analisar eventos de segurança provenientes de diferentes fontes.

---

## SOAR

Security Orchestration, Automation and Response.

Tecnologia utilizada para automatizar e orquestrar processos de segurança.

Pode integrar ferramentas e executar fluxos de resposta automatizados.

---

## EDR

Endpoint Detection and Response.

Solução voltada ao monitoramento e detecção de atividades em endpoints.

Pode coletar:

- processos;
- conexões;
- arquivos;
- eventos de segurança.

---

## XDR

Extended Detection and Response.

Abordagem que integra sinais de diferentes camadas do ambiente.

Pode combinar dados de:

- endpoints;
- redes;
- identidade;
- e-mail;
- nuvem.

---

## SOC

Security Operations Center.

Equipe ou estrutura responsável por monitorar e responder a eventos de segurança.

---

## CTI

Cyber Threat Intelligence.

Processo de coleta, análise e interpretação de informações sobre ameaças cibernéticas.

O objetivo é transformar dados em inteligência útil para tomada de decisão.

---

## APT

Advanced Persistent Threat.

Termo utilizado para descrever adversários ou campanhas caracterizadas por capacidade avançada e persistência.

A identificação de um APT exige evidências suficientes e não deve ser baseada em um único indicador.

---

## RAG

Retrieval-Augmented Generation.

Arquitetura que combina recuperação de informações com geração de texto por um modelo de linguagem.

No CyberSentinel AI, o RAG permite recuperar conhecimento técnico relevante antes de solicitar uma resposta ao LLM.

Fluxo conceitual:

```text
Pergunta
   ↓
Embedding
   ↓
Busca Vetorial
   ↓
Chunks Relevantes
   ↓
Contexto
   ↓
LLM
   ↓
Resposta
