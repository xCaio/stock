# Stock API

## Visão geral

A Stock API é uma aplicação backend em FastAPI para gestão de insumos e produtos com controle de estoque, histórico de movimentações, autenticação por JWT e administração de usuários.

O projeto foi estruturado para funcionar como uma base sólida para sistemas de controle de estoque com regras simples de acesso e operações registradas para auditoria.

---

## Funcionalidades implementadas

### Autenticação e segurança
- Registro de usuários
- Login com e-mail e senha
- Login compatível com OAuth2 form data
- Emissão de access token e refresh token
- Proteção de rotas com autenticação JWT
- Controle de permissões por role (user/admin)

### Gestão de produtos e estoque
- Cadastro de produtos com código único
- Listagem de produtos com filtros por tipo, status ativo/inativo e busca por código
- Busca de produto por código
- Edição de dados do produto
- Ativação e inativação de produtos sem exclusão física
- Consulta de produtos com estoque baixo
- Registro de entradas e saídas de estoque
- Ajuste manual de inventário
- Histórico de movimentações por produto

### Dashboard e auditoria
- Endpoint de dashboard com métricas gerais
- Contagem de entradas e saídas do dia
- Identificação de produtos sem estoque
- Listagem de produtos com estoque abaixo do mínimo
- Últimas movimentações registradas

### Administração de usuários
- Listagem de usuários (apenas admin)
- Consulta de usuário por ID (apenas admin)
- Atualização de dados de usuário (apenas admin)
- Alteração de role entre user e admin

---

## Stack tecnológica

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- Alembic
- PostgreSQL
- JWT (python-jose)
- bcrypt/passlib
- Uvicorn
- python-dotenv

---

## Estrutura do projeto

- [main.py](main.py) – ponto de entrada da aplicação e inclusão dos routers
- [auth_routes.py](auth_routes.py) – rotas de autenticação e token
- [supplies_routes.py](supplies_routes.py) – gestão de produtos, estoque e movimentações
- [movements_routes.py](movements_routes.py) – histórico de movimentações
- [dashboard_routes.py](dashboard_routes.py) – métricas e resumo do estoque
- [users_routes.py](users_routes.py) – administração de usuários
- [models.py](models.py) – modelos SQLAlchemy
- [schemas.py](schemas.py) – validação de entrada e saída
- [database.py](database.py) – configuração do banco
- [dependencies.py](dependencies.py) – dependências de sessão e autenticação
- [security.py](security.py) – configuração de segurança e hashing
- [alembic/](alembic) – migrações do banco
- [docs/](docs) – documentação do projeto

---

## Principais modelos

### User
Representa um usuário do sistema com:
- id
- name
- email
- password (armazenada de forma criptografada)
- role

### Product
Representa um produto ou insumo com:
- id
- code
- product_type
- stock
- stock_minimum
- active
- created_at
- updated_at

### StockMovement
Representa uma movimentação de estoque com:
- product_id
- user_id
- movement_type
- quantity
- stock_before
- stock_after
- observation
- created_at

---

## Endpoints principais

### Autenticação
- POST /auth/register
- POST /auth/login
- POST /auth/login-form
- GET /auth/refresh

### Produtos e estoque
- GET /supplies/
- POST /supplies/products
- GET /supplies/products
- GET /supplies/products/{code}
- PUT /supplies/products/{code}
- PATCH /supplies/products/{code}/inactive
- PATCH /supplies/products/{code}/active
- GET /supplies/products/low-stock
- POST /supplies/products/{code}/entry
- POST /supplies/products/{code}/exit
- POST /supplies/products/{id}/adjustment
- GET /supplies/products/{code}/movements

### Movimentações
- GET /movements

### Dashboard
- GET /dashboard

### Usuários
- GET /users
- GET /users/{id}
- PUT /users/{id}
- PATCH /users/{id}/role

---

## Variáveis de ambiente

Configure as seguintes variáveis antes de executar a aplicação:

```env
DATABASE_URL=postgresql://usuario:senha@localhost:5432/stock
SECRET_KEY=sua-chave-secreta
ALGORITHM=HS256
TOKEN_ACESS_EXPIRES_MINUTES=30
```

---

## Como executar

### 1. Criar ambiente virtual

```bash
python -m venv venv
```

### 2. Instalar dependências

```bash
pip install -r requirements.txt
```

### 3. Aplicar migrações

```bash
alembic upgrade head
```

### 4. Subir a aplicação

```bash
uvicorn main:app --reload
```

A API ficará disponível em:
- http://127.0.0.1:8000

Documentação interativa:
- http://127.0.0.1:8000/docs
- http://127.0.0.1:8000/redoc

---

## Observações finais

Este projeto já contempla os principais blocos de uma API de estoque funcional: autenticação, gestão de produtos, entradas e saídas, histórico de movimentos, dashboard e controle administrativo. A estrutura está preparada para evolução com novas regras de negócio e funcionalidades adicionais.
