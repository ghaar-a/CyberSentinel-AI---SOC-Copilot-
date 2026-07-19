# SQL Injection

## Definição

SQL Injection é uma vulnerabilidade que ocorre quando entradas controladas pelo usuário são incorporadas de forma insegura em consultas SQL.

Um atacante pode manipular a estrutura lógica de uma consulta para alterar seu comportamento original.

---

## Impacto

Dependendo do contexto, uma SQL Injection pode permitir:

- leitura não autorizada de dados;
- alteração de registros;
- exclusão de dados;
- bypass de autenticação;
- acesso a informações sensíveis.

O impacto depende das permissões da aplicação e da configuração do banco de dados.

---

## Indicadores

Possíveis sinais incluem:

- erros SQL inesperados;
- padrões incomuns em parâmetros;
- aumento de respostas HTTP 500;
- consultas anômalas;
- comportamento diferente ao modificar parâmetros;
- alertas de WAF;
- padrões suspeitos nos logs da aplicação.

---

## Mitigação

A principal defesa consiste em utilizar consultas parametrizadas ou prepared statements.

Outras medidas incluem:

- validação de entrada;
- princípio do menor privilégio;
- uso seguro de ORMs;
- proteção WAF;
- tratamento adequado de erros;
- monitoramento de logs.

A validação de entrada deve ser considerada uma camada complementar e não substitui consultas parametrizadas.

---

## Relação com OWASP

SQL Injection é uma vulnerabilidade tradicionalmente associada ao OWASP Top 10.

A classificação exata depende da versão do OWASP Top 10 considerada.

---

## Investigação

Durante uma investigação, devem ser analisados:

- logs da aplicação;
- logs do banco de dados;
- alertas do WAF;
- parâmetros enviados;
- contas utilizadas;
- dados acessados;
- alterações realizadas.

---

## Observação Analítica

A presença de caracteres especiais em uma requisição não confirma SQL Injection.

A análise deve considerar contexto, comportamento da aplicação e evidências correlacionadas.
