## Modulo de autenticação (feito)
GET /auth/          -- rota padrão
POST /auth/login    -- login de usuario
POST /auth/register -- registro de usuario
GET  /auth/refresh  -- refresh token


## Módulo de insumos (feito)

GET /products       -- listar todos

Exemplo de resposta:

[
  {
    "id": 1,
    "code": "PA12345",
    "type": "etiqueta",
    "stock": 20
  }
]

Pode aceitar filtros futuramente:

GET /products?type=etiqueta
GET /products?active=true
GET /products?search=PA123

## Buscar um produto (feito)

GET /products/{id}  -- busca um insumo a partir do ID


## Criar produto (Admin) (feito)

POST /products

## Editar produto (feito)

PUT /products/{id}

## Inativar produto (ao invés de excluir) (feito)

PATCH /products/{id}/inactive
Só altera:
active = False

# Reativar (feito)
PATCH /products/{id}/active
Só altera:
active = True


## Movimentações - Essa é a parte principal do sistema. (feito)
- Entrada

POST /products/{id}/entry

{
    "quantity": 20,
    "observation": "Compra fornecedor X"
}

+ aumenta estoque
+ cria movimentação
+ salva usuário
+ salva data

- Saída

POST /products/{id}/exit

{
    "quantity": 5,
    "observation": "Produção"
}

+ verifica estoque
+ diminui estoque
+ cria movimentação


# Histórico

Listar tudo

GET /movements

GET /movements?products=1

GET /movements?user=5

GET /movements?type=entry

GET /movements?start=2026-07-01&end=2026-07-31

# Dashboard

GET /dashboard

{
    "products": 32,
    "entries_today": 8,
    "exits_today": 6,
    "low_stock": 4
}

# Usuários (Admin)

GET /users
GET /users/{id}
PUT /users/{id}
PATCH /users/{id}/role
PATCH /users/{id}/inactive



## Obrigar toda alteração de estoque a passar por uma movimentação.

Entrada:
POST /products/{id}/entry

Saída:
POST /products/{id}/exit

A única exceção seria um ajuste de inventário:

POST /products/{id}/adjustment

Body:

{
    "new_stock": 48,
    "reason": "Inventário mensal"
}

O backend calcula a diferença automaticamente:

Antes: 55
Depois: 48

↓

Movimentação:

AJUSTE
-7

## Estoque baixo

GET /products/low-stock

Retorna apenas produtos com:

stock <= stock_minimum

## Historico de um produto
GET /products/{id}/movements