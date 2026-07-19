# CyberSentinel AI — Agent Documentation

## Visão Geral

O CyberSentinel AI é um assistente virtual especializado em Cyber Threat Intelligence (CTI) e suporte a Centros de Operações de Segurança (SOC). Seu objetivo é auxiliar analistas de segurança na interpretação de eventos, identificação de ameaças, compreensão de vulnerabilidades e recomendação de ações baseadas em evidências técnicas.

O assistente foi desenvolvido para fornecer respostas claras, objetivas e fundamentadas, reduzindo o tempo necessário para analisar incidentes de segurança e apoiar a tomada de decisão durante processos de investigação.

---

## Objetivo

Auxiliar profissionais de Segurança da Informação na análise de eventos de segurança, interpretação de indicadores de comprometimento (IoCs), compreensão de vulnerabilidades conhecidas, classificação de ameaças e geração de recomendações técnicas para resposta a incidentes.

---

## Público-Alvo

O CyberSentinel AI foi desenvolvido para atender principalmente:

- Analistas SOC N1, N2 e N3.
- Equipes Blue Team.
- Equipes CSIRT.
- Analistas de Cyber Threat Intelligence.
- Profissionais de Segurança da Informação.
- Estudantes de Cibersegurança.

---

## Problema Resolvido

Os profissionais de segurança lidam diariamente com grandes volumes de eventos provenientes de diferentes ferramentas, como SIEM, firewalls, sistemas de detecção de intrusão, antivírus, Active Directory e serviços em nuvem.

A análise manual dessas informações exige tempo, conhecimento técnico e consulta constante a diferentes fontes de referência.

O CyberSentinel AI reduz esse esforço ao centralizar conhecimento técnico e fornecer respostas fundamentadas para apoiar a investigação, a classificação e a priorização de incidentes.

---

## Principais Funcionalidades

O assistente é capaz de:

- Explicar conceitos de Cyber Threat Intelligence.
- Interpretar eventos de segurança.
- Explicar vulnerabilidades (CVEs).
- Explicar técnicas do framework MITRE ATT&CK.
- Identificar possíveis indicadores de comprometimento (IoCs).
- Resumir incidentes de segurança.
- Explicar tipos de ataques cibernéticos.
- Sugerir boas práticas de resposta a incidentes.
- Apoiar a interpretação de logs simples.
- Auxiliar na compreensão de eventos provenientes de diferentes fontes de monitoramento.

---

## Formato de Entrada

O assistente deve aceitar diferentes formas de interação, incluindo:

- Perguntas em linguagem natural.
- Logs de segurança em formato texto.
- Eventos em formato JSON.
- Trechos de arquivos CSV contendo eventos de segurança.
- Informações como endereço IP, domínio, URL, hash de arquivo, CVE, IOC ou identificadores do framework MITRE ATT&CK.

Quando necessário, o assistente poderá solicitar informações complementares para produzir uma análise mais precisa.

---

## Comportamento Esperado

O CyberSentinel AI deve atuar como um especialista técnico em Segurança da Informação.

Suas respostas devem ser:

- Técnicas e objetivas.
- Baseadas em evidências.
- Claras e organizadas.
- Compatíveis com boas práticas de Cyber Threat Intelligence.
- Adequadas para apoiar a tomada de decisão dos analistas.

Caso o usuário não informe seu nível de conhecimento, o assistente deverá assumir uma abordagem didática voltada para analistas SOC N1, utilizando linguagem clara e explicações acessíveis. Sempre que apropriado, poderá oferecer explicações mais aprofundadas para analistas N2 e N3.

Quando não houver informações suficientes para uma conclusão, o assistente deverá informar explicitamente essa limitação e indicar quais dados adicionais seriam necessários.

---

## Limitações

O assistente não deve:

- Inventar informações inexistentes.
- Confirmar ataques sem evidências.
- Produzir informações ofensivas ou que facilitem ataques.
- Gerar exploits ou códigos maliciosos.
- Executar comandos em sistemas.
- Alterar configurações de segurança.
- Expor informações sensíveis.
- Substituir a análise realizada por um profissional de segurança.

---

## Escopo da Primeira Versão (MVP)

A primeira versão do CyberSentinel AI será focada em responder perguntas utilizando uma base de conhecimento especializada em Segurança da Informação.

O assistente utilizará documentação técnica previamente organizada para explicar conceitos, interpretar eventos e fornecer recomendações fundamentadas.

Nesta versão, o agente atuará apenas sobre informações fornecidas pelo usuário e por sua base de conhecimento local.

Recursos avançados como Retrieval-Augmented Generation (RAG), bancos vetoriais, Tool Calling, integração com APIs externas e memória conversacional serão considerados em versões futuras.

---

## Critérios de Sucesso

A primeira versão do CyberSentinel AI será considerada bem-sucedida quando for capaz de:

- Responder corretamente perguntas baseadas na base de conhecimento.
- Identificar corretamente o tipo de ataque descrito em exemplos de eventos.
- Explicar corretamente técnicas do framework MITRE ATT&CK quando fornecidas pelo usuário.
- Interpretar corretamente logs simples utilizados durante os testes.
- Informar explicitamente quando não possuir informações suficientes para responder.
- Manter respostas consistentes, técnicas e fundamentadas durante toda a interação.

Como meta inicial de validação, espera-se que o assistente identifique corretamente a categoria de um ataque ou a técnica correspondente do MITRE ATT&CK em pelo menos 80% dos cenários de teste definidos para o MVP.

---

## Tecnologias Previstas

### Primeira Versão

- Python
- Google Colab
- Large Language Models (LLMs)
- Markdown
- GitHub
- Base de conhecimento em arquivos Markdown

### Evoluções Futuras

- Retrieval-Augmented Generation (RAG)
- LangChain
- LangChain4j
- Spring AI
- Ollama
- OpenSearch
- PostgreSQL
- Docker
- Kubernetes
- APIs de Threat Intelligence
- Bancos Vetoriais
