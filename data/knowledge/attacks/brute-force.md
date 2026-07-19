# Brute Force

## Definição

Brute Force é uma técnica de ataque na qual um adversário tenta obter acesso a uma conta, sistema ou serviço realizando repetidas tentativas de autenticação até encontrar credenciais válidas.

O ataque pode utilizar combinações geradas automaticamente ou listas de usuários e senhas obtidas previamente.

Em ambientes corporativos, ataques de força bruta são frequentemente direcionados a serviços expostos à rede, como VPN, SSH, RDP, aplicações web, serviços de e-mail e portais de autenticação.

---

## Como Funciona

O atacante envia múltiplas tentativas de autenticação para um serviço.

As tentativas podem utilizar:

- diferentes combinações de usuário e senha;
- listas de senhas comuns;
- credenciais vazadas;
- senhas previamente utilizadas;
- combinações geradas automaticamente.

Quando uma combinação válida é encontrada, o atacante pode obter acesso ao recurso protegido.

---

## Tipos Relacionados

### Brute Force Tradicional

O atacante tenta muitas senhas contra uma única conta ou um pequeno conjunto de contas.

Esse comportamento pode gerar um grande volume de falhas de autenticação concentradas em poucos usuários.

### Password Spraying

O atacante utiliza uma mesma senha ou um pequeno conjunto de senhas contra muitas contas.

Essa técnica procura evitar mecanismos de bloqueio de conta acionados após várias tentativas consecutivas contra o mesmo usuário.

### Credential Stuffing

O atacante utiliza pares de usuário e senha obtidos em vazamentos anteriores.

O ataque explora a reutilização de credenciais entre diferentes serviços.

Embora seja relacionado a ataques de autenticação, Credential Stuffing não é necessariamente um ataque de força bruta tradicional.

---

## Indicadores de Comprometimento e Evidências

Possíveis evidências incluem:

- grande quantidade de falhas de autenticação;
- múltiplas tentativas originadas do mesmo endereço IP;
- tentativas contra várias contas em curto período;
- aumento repentino de eventos de autenticação;
- autenticações bem-sucedidas após diversas falhas;
- acessos provenientes de localizações incomuns;
- utilização de contas que normalmente não apresentam atividade;
- tentativas distribuídas entre múltiplos endereços IP.

Um único evento de falha de autenticação não é suficiente para caracterizar um ataque de força bruta.

A análise deve considerar frequência, volume, distribuição temporal, origem e contexto.

---

## Identificação em Logs

Eventos relevantes podem incluir:

- login failed;
- authentication failure;
- invalid password;
- invalid credentials;
- account locked;
- authentication succeeded.

Exemplo conceitual:

```text
User: admin
Source IP: 203.0.113.10
Event: Authentication Failed
Timestamp: 2026-01-10 10:00:01
