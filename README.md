# Stock API

API REST para controle de estoque de etiquetas e ribbons. O projeto oferece cadastro e consulta de produtos, movimentações auditáveis, autenticação JWT, administração de usuários, indicadores de estoque e exportação de produtos em Excel.

## Tecnologias

- Python 3
- FastAPI e Uvicorn
- SQLAlchemy 2 e PostgreSQL
- Alembic para migrations
- Pydantic 2 para validação de dados
- JWT (`python-jose`) e hash de senhas com `passlib`/bcrypt
- Pandas e OpenPyXL para exportação `.xlsx`

## Arquitetura

O código foi organizado por responsabilidade, separando configuração, persistência, contratos HTTP e endpoints:

```text
app/
├── core/
│   ├── database.py       # engine SQLAlchemy e Base dos modelos
│   └── security.py       # JWT, OAuth2 e contexto bcrypt
├── dependencies/
│   └── auth.py           # sessão do banco e validação do token
├── enums/
│   └── types.py          # tipos de movimentação
├── models/
│   ├── user.py
│   ├── product.py
│   └── stock_movement.py # entidades SQLAlchemy
├── routers/
│   ├── auth.py
│   ├── supplies.py
│   ├── movements.py
│   ├── dashboard.py
│   └── users.py          # módulos HTTP da API
├── schemas/
│   ├── auth.py
│   ├── product.py
│   ├── stock_movement.py
│   └── user.py           # validação e serialização Pydantic
└── main.py               # aplicação FastAPI, routers e CORS
alembic/                  # configuração e histórico de migrations
docs/                     # documentação complementar
```

`app/main.py` compõe a aplicação e registra os routers. Os routers usam as dependências para obter uma sessão do banco e o usuário autenticado; os modelos representam as tabelas e os schemas validam os dados recebidos e formatam as respostas.

## Recursos disponíveis

- Registro, login por JSON ou formulário OAuth2 e renovação de token.
- Produtos com código único, tipo `etiqueta` ou `ribbon`, estoque mínimo e ativação/inativação.
- Filtros por tipo, status e código; alerta de baixo estoque.
- Exportação da listagem filtrada em Excel, com filtros, cabeçalho fixado e destaque para estoque baixo.
- Entradas e saídas com registro de produto, usuário, quantidade, saldo anterior/posterior, observação e data.
- Histórico global de movimentações com filtros e histórico por produto.
- Dashboard com indicadores de estoque e últimas movimentações.
- Administração de usuários e papéis `user` e `admin`.

## Autenticação e permissões

Envie o token de acesso nas rotas protegidas:

```http
Authorization: Bearer <access_token>
```

Os módulos `/supplies`, `/movements` e `/users` exigem autenticação. Cadastro de produto, entrada, saída e ajuste de estoque exigem adicionalmente o papel `admin`; a administração de usuários também é exclusiva de administradores. As rotas de autenticação e dashboard estão disponíveis sem token na implementação atual.

## Endpoints

| Módulo | Método | Rota | Descrição |
| --- | --- | --- | --- |
| Autenticação | `GET` | `/auth/` | Verifica o módulo de autenticação |
|  | `POST` | `/auth/register` | Cria uma conta |
|  | `POST` | `/auth/login` | Login com corpo JSON; retorna access e refresh token |
|  | `POST` | `/auth/login-form` | Login compatível com OAuth2 form data |
|  | `GET` | `/auth/refresh` | Gera novo access token |
|  | `GET` | `/auth/me` | Retorna o usuário do token |
| Produtos | `GET` | `/supplies/` | Verifica o módulo de insumos |
|  | `POST` | `/supplies/products` | Cria produto (admin) |
|  | `GET` | `/supplies/products` | Lista produtos e aceita `type`, `active` e `search` |
|  | `GET` | `/supplies/products/export` | Exporta a listagem filtrada em Excel |
|  | `GET` | `/supplies/products/low-stock` | Lista itens com `stock <= stock_minimum` |
|  | `GET` | `/supplies/products/{code}` | Busca produto pelo código |
|  | `PUT` | `/supplies/products/{code}` | Atualiza código e tipo |
|  | `PATCH` | `/supplies/products/{code}/active` | Ativa produto |
|  | `PATCH` | `/supplies/products/{code}/inactive` | Inativa produto |
|  | `POST` | `/supplies/products/{code}/entry` | Registra entrada (admin) |
|  | `POST` | `/supplies/products/{code}/exit` | Registra saída (admin) |
|  | `GET` | `/supplies/products/{code}/movements` | Histórico de um produto |
|  | `POST` | `/supplies/products/{id}/adjustment` | Ajuste de inventário (admin) |
| Movimentações | `GET` | `/movements/` | Lista e filtra movimentações |
| Dashboard | `GET` | `/dashboard/` | Retorna indicadores do estoque |
| Usuários | `GET` | `/users/` | Lista usuários (admin) |
|  | `GET` | `/users/{id}` | Busca usuário (admin) |
|  | `PUT` | `/users/{id}` | Atualiza usuário (admin) |
|  | `PATCH` | `/users/{id}/role` | Altera papel (admin) |

### Filtros de produtos e movimentações

```http
GET /supplies/products?type=etiqueta&active=true&search=PA
GET /movements/?product_code=PA123&user_id=1&movement_type=entrada&start=2026-08-01&end=2026-08-31
```

Os tipos de produto aceitos são `etiqueta` e `ribbon`; as formas plurais também são normalizadas na criação e edição. Os tipos de movimentação são `entrada`, `saida` e `ajuste`.

## Exemplos de requisição

Criar produto:

```json
{
  "code": "PA12345",
  "product_type": "etiqueta",
  "stock": 20,
  "stock_minimum": 5
}
```

Registrar entrada ou saída:

```json
{
  "quantity": 10,
  "observation": "Recebimento do fornecedor"
}
```

## Configuração local

1. Crie e ative um ambiente virtual:

   ```bash
   python -m venv venv
   # Windows PowerShell
   .\venv\Scripts\Activate.ps1
   ```

2. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

3. Copie `.env.example` para `.env` e preencha as variáveis:

   ```env
   DATABASE_URL=postgresql://postgres:sua_senha@localhost:5432/stock
   SECRET_KEY=uma_chave_secreta_forte
   ALGORITHM=HS256
   TOKEN_ACESS_EXPIRES_MINUTES=30
   ```

   > O nome `TOKEN_ACESS_EXPIRES_MINUTES` é mantido assim por compatibilidade com o código atual.

4. Aplique as migrations:

   ```bash
   alembic upgrade head
   ```

5. Inicie o servidor:

   ```bash
   uvicorn app.main:app --reload
   ```

A API estará disponível em `http://127.0.0.1:8000`, com documentação interativa em:

- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`

## Observação de manutenção

O endpoint de ajuste de inventário está exposto, mas sua implementação ainda precisa ser alinhada aos campos obrigatórios atuais de `StockMovement` (`movement_type`, `stock_before`, `stock_after` e `observation`). Os fluxos de entrada e saída já registram esses dados corretamente.
