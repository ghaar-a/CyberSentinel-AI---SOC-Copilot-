# CyberSentinel AI — Knowledge Base

## Objetivo

A Base de Conhecimento do CyberSentinel AI reúne informações técnicas utilizadas pelo assistente para interpretar eventos de segurança, explicar conceitos de Cyber Threat Intelligence (CTI), responder perguntas especializadas e apoiar analistas durante investigações de incidentes.

Sua finalidade é fornecer conhecimento confiável, organizado e reutilizável, reduzindo respostas imprecisas e garantindo maior consistência nas análises realizadas pelo agente.

---

## Organização da Base de Conhecimento

A Base de Conhecimento é organizada em módulos independentes para facilitar manutenção, evolução e futura integração com mecanismos de Retrieval-Augmented Generation (RAG).

```text
data/
└── knowledge/
    ├── attacks/
    ├── mitre/
    ├── vulnerabilities/
    ├── incident-response/
    └── glossary/
```

Cada diretório representa um domínio específico do conhecimento utilizado pelo assistente.

Essa organização permite que novos documentos sejam adicionados sem alterar a estrutura existente, favorecendo escalabilidade e reutilização do conhecimento.

---

## Conteúdo da Base

### attacks/

Contém descrições técnicas dos principais ataques cibernéticos.

Cada documento apresenta:

- definição;
- funcionamento;
- comportamento esperado;
- indicadores de comprometimento (IoCs);
- formas de identificação;
- técnicas de mitigação;
- relação com o framework MITRE ATT&CK.

Exemplos:

- Brute Force
- SQL Injection
- Cross-Site Scripting (XSS)
- Ransomware
- Phishing

Além da documentação conceitual, esta pasta também reúne descrições textuais dos padrões observados em datasets públicos de segurança, como o CICIDS2017 e o CSE-CIC-IDS2018.

Essas descrições funcionam como assinaturas comportamentais utilizadas pelo assistente para compreender como determinados ataques normalmente se manifestam em logs, fluxos de rede e eventos de segurança.

---

### mitre/

Reúne documentação resumida sobre o framework MITRE ATT&CK.

Cada documento descreve:

- objetivo da tática;
- técnicas relacionadas;
- exemplos de utilização;
- possíveis evidências observáveis durante uma investigação.

---

### vulnerabilities/

Documenta conceitos relacionados à gestão de vulnerabilidades.

Inclui conteúdos como:

- CVE;
- CVSS;
- classificação de severidade;
- impacto das vulnerabilidades;
- priorização baseada em risco.

---

### incident-response/

Contém documentação baseada nas boas práticas de resposta a incidentes.

Inclui temas como:

- ciclo de resposta segundo o NIST;
- contenção;
- erradicação;
- recuperação;
- lições aprendidas.

---

### glossary/

Apresenta definições resumidas dos principais termos utilizados em Segurança da Informação.

Exemplos:

- IOC
- IOA
- SIEM
- SOAR
- EDR
- XDR
- SOC
- CTI
- APT

---

## Padrão de Escrita dos Documentos

Todos os documentos da Base de Conhecimento seguem um padrão único de organização para facilitar a leitura tanto por pessoas quanto por Modelos de Linguagem (LLMs).

Cada arquivo deve:

- utilizar Markdown (.md);
- possuir apenas um assunto principal;
- iniciar com um título de nível 1 (`#`);
- utilizar títulos hierárquicos (`##`, `###`);
- possuir parágrafos curtos e objetivos;
- utilizar listas para facilitar recuperação de contexto;
- evitar textos excessivamente longos sem divisão em seções;
- utilizar linguagem técnica, clara e consistente.

Sempre que possível, cada documento também deve conter:

- definição;
- contexto;
- funcionamento;
- exemplos;
- formas de identificação;
- formas de mitigação;
- referências técnicas.

Esse padrão facilita futuras integrações com mecanismos de busca semântica, bancos vetoriais e arquiteturas baseadas em RAG.

---

## Fontes de Conhecimento

A Base de Conhecimento utiliza documentação pública e materiais técnicos reconhecidos pela comunidade de Segurança da Informação, incluindo:

- MITRE ATT&CK
- OWASP
- NIST
- CISA
- Documentação oficial de fabricantes
- Materiais produzidos durante o desenvolvimento do projeto

Todas as informações adicionadas devem possuir origem confiável e estar alinhadas às boas práticas da área.

---

## Relação com os Datasets

Os datasets utilizados pelo projeto não fazem parte diretamente da Base de Conhecimento.

Eles representam os dados que serão analisados pelo assistente.

A Base de Conhecimento fornece o contexto técnico necessário para interpretar corretamente esses dados.

Os datasets utilizados durante o desenvolvimento incluem, principalmente:

- CICIDS2017
- CSE-CIC-IDS2018
- Logs de firewall
- Logs de autenticação
- Eventos exportados de SIEM

Os comportamentos característicos identificados nesses datasets são documentados na pasta `attacks/`, transformando padrões estatísticos em conhecimento textual que pode ser utilizado pelo agente durante suas respostas.

---

## Evolução da Base de Conhecimento

A estrutura atual é preparada para evoluir de forma incremental.

Nas próximas versões, a Base de Conhecimento será integrada a mecanismos de Retrieval-Augmented Generation (RAG), bancos vetoriais e APIs de Threat Intelligence.

Essa evolução permitirá consultas semânticas a documentos técnicos, recuperação dinâmica de contexto e atualização contínua do conhecimento utilizado pelo CyberSentinel AI.
