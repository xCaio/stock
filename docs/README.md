# Documentação do projeto Stock API

## Visão geral

Este projeto é uma API REST desenvolvida com FastAPI para gerenciar usuários, autenticação e cadastro de insumos/produtos com controle básico de estoque.

A ideia principal é oferecer um backend simples, modular e extensível para operações como:

- cadastro e autenticação de usuários;
- criação, listagem, busca, edição e ativação/inativação de produtos;
- proteção de rotas por autenticação via JWT;
- persistência em banco relacional com SQLAlchemy e Alembic.

---

## Objetivo do sistema

O sistema foi pensado para servir como base para um controle de estoque de insumos, permitindo:

- registrar produtos com código único;
- armazenar tipo do produto e quantidade em estoque;
- manter estoque mínimo para controle de reposição;
- restringir certas operações a usuários com papel de administrador.

---

## Stack tecnológica

As principais tecnologias utilizadas são:

- Python 3.x
- FastAPI para construção da API
- SQLAlchemy como ORM
- Pydantic para validação de dados
- PostgreSQL via SQLAlchemy
- Alembic para migrações de banco
- JWT para autenticação
- bcrypt para hashing de senhas
- Uvicorn para execução da aplicação

---

## Arquitetura do projeto

A aplicação segue uma arquitetura simples em camadas, com separação por responsabilidade:

1. Camada de entrada (rotas)
   - Responsável por receber requisições HTTP.
   - Os endpoints estão organizados em módulos por domínio.

2. Camada de dependências
   - Centraliza a criação de sessões do banco e a verificação de tokens.

3. Camada de modelo
   - Define as entidades do banco com SQLAlchemy.

4. Camada de schemas
   - Define os dados esperados nas entradas e saídas da API.

5. Camada de persistência
   - Usa SQLAlchemy e Alembic para conectar e migrar o banco.

---

## Estrutura de arquivos

- [main.py](../main.py)  
  Ponto de entrada da aplicação. Monta os routers da API.

- [auth_routes.py](../auth_routes.py)  
  Contém as rotas de autenticação: registro, login e refresh token.

- [supplies_routes.py](../supplies_routes.py)  
  Contém as rotas de gestão de produtos/insumos.

- [models.py](../models.py)  
  Define as entidades do banco: User e Product.

- [schemas.py](../schemas.py)  
  Define os modelos de entrada/saída usados pelo FastAPI.

- [database.py](../database.py)  
  Configura a engine do SQLAlchemy e a base declarativa.

- [dependencies.py](../dependencies.py)  
  Implementa a injeção de dependência do banco e a verificação de token JWT.

- [security.py](../security.py)  
  Centraliza a configuração de segurança, hashing e OAuth2.

- [alembic/](../alembic)  
  Contém as migrações e configuração do Alembic.

- [docs/](.)  
  Armazena a documentação do projeto.

---

## Modelos principais

### Usuário

A entidade User representa um usuário do sistema.

Campos:

- id: identificador único
- name: nome do usuário
- email: e-mail único
- password: senha criptografada
- role: papel do usuário (atualmente o fluxo usa admin e user)

### Produto

A entidade Product representa um item de estoque.

Campos:

- id: identificador único
- code: código do produto, único
- product_type: tipo/nome do produto
- stock: quantidade em estoque
- stock_minimum: quantidade mínima desejada
- created_at: data de criação
- updated_at: data da última atualização
- active: indica se o produto está ativo

---

## Fluxo de autenticação

O fluxo de autenticação funciona da seguinte forma:

1. O cliente envia e-mail e senha para a rota de login.
2. O backend valida as credenciais contra o banco.
3. Se válidas, gera um token JWT de acesso.
4. O token é enviado ao cliente e usado nas rotas protegidas.
5. O middleware de dependência valida o token e recupera o usuário autenticado.

### Rotas de autenticação

- POST /auth/register: cria um novo usuário
- POST /auth/login: realiza login e retorna tokens
- POST /auth/login-form: login compatível com OAuth2 form data
- GET /auth/refresh: gera um novo access token

---

## Gestão de produtos

As rotas de produtos permitem o controle básico de estoque.

### Rotas atuais

- GET /supplies/  
  Retorna uma mensagem inicial da rota de insumos.

- POST /supplies/products  
  Cria um novo produto. A operação exige autenticação e, no fluxo atual, apenas usuários com role admin podem criar produto.

- GET /supplies/products/{code}  
  Busca um produto pelo código.

- PUT /supplies/products/{code}  
  Atualiza os dados de um produto.

- GET /supplies/products  
  Lista produtos com filtros opcionais por tipo, status ativo/inativo e busca por código.

- PATCH /supplies/products/{code}/inactive  
  Inativa um produto sem removê-lo do banco.

- PATCH /supplies/products/{code}/active  
  Reativa um produto.

---

## Fluxo de execução da aplicação

A aplicação é iniciada a partir de [main.py](../main.py), que inclui os routers principais:

- router de autenticação
- router de supplies

Ao subir a aplicação, o FastAPI expõe os endpoints e usa as dependências definidas para sessão de banco e autenticação.

---

## Requisitos de ambiente

Antes de rodar o projeto, é necessário configurar as variáveis de ambiente.

Exemplo de variáveis esperadas:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/stock
SECRET_KEY=sua-chave-secreta
ALGORITHM=HS256
TOKEN_ACESS_EXPIRES_MINUTES=30
```

> O projeto utiliza essas variáveis em [database.py](../database.py), [security.py](../security.py) e [auth_routes.py](../auth_routes.py).

---

## Como rodar o projeto

### 1. Criar ambiente virtual

```bash
python -m venv venv
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Configurar o banco

Aplicar as migrações com Alembic:

```bash
alembic upgrade head
```

### 4. Subir a aplicação

```bash
uvicorn main:app --reload
```

A API ficará disponível em:

- http://127.0.0.1:8000

A documentação automática do FastAPI pode ser acessada em:

- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

---

## Pontos importantes do projeto atual

O projeto já possui uma base funcional para:

- autenticação por JWT;
- cadastro de usuários;
- gestão de produtos;
- controle básico de status ativo/inativo.

No entanto, a documentação existente em [docs/routes.md](routes.md) mostra que o projeto ainda tem uma visão mais ampla planejada, incluindo funcionalidades futuras como:

- movimentações de entrada e saída de estoque;
- histórico de movimentações;
- dashboard com métricas;
- gestão de usuários admin;
- estoque baixo;
- histórico por produto.

Essas funcionalidades ainda não aparecem implementadas no código atual, mas servem como direção futura do projeto.

---

## Resumo executivo

Em resumo, o projeto atual é uma API backend em FastAPI para controle de insumos/produtos com autenticação, banco relacional e estrutura modular. Ele já possui os pilares básicos para crescer para um sistema completo de gestão de estoque.
