from fastapi import APIRouter, Depends, HTTPException
from dependencies import verify_token, get_session
from sqlalchemy.orm import Session
from models import Product, User
from schemas import SuppliesSchema, ProductResponseSchema
from typing import List


supplies_router = APIRouter(prefix='/supplies', tags=['supplies'], dependencies=[Depends(verify_token)])

@supplies_router.get('/')
async def home():
    return {
        "message": "Rota inicial dos insumos"
    }

@supplies_router.get('/products', response_model=List[ProductResponseSchema])
async def show_products(session: Session = Depends(get_session)):

    """
        GET /products    -- listar todos
    """

    products = session.query(Product).all()
    return products


@supplies_router.post('/products')
async def create_product(supplies_schema: SuppliesSchema, session: Session = Depends(get_session), user: User = Depends(verify_token)):

    """
        ## Criar produto (Admin)
        POST /products
    """

    product = session.query(Product).filter(Product.code == supplies_schema.code).first()
    if product:
        raise HTTPException(status_code=400, detail='O codigo do produto já existe')
    if user.role != "admin":
        raise HTTPException(status_code=401, detail='Voce nao tem autorizacao para realizar essa operacao.')
    new_product =  Product(supplies_schema.code, supplies_schema.product_type, supplies_schema.stock, supplies_schema.stock_minimum)
    session.add(new_product)
    session.commit()
    return {
        "message": f"Produto {new_product.code} adicionado com sucesso ",
        "product": new_product
    }

@supplies_router.get('/products/{code}')
async def search_product(code: str, session: Session = Depends(get_session)):
    """
        ## Buscar um produto
        GET /products/{id}  -- busca um insumo a partir do ID
    """
    product = session.query(Product).filter(Product.code == code).first()
    if not product:
        raise HTTPException(status_code=404, detail='Codigo da etiqueta nao encontrada')
    return{
        "product": product
    }

@supplies_router.put('/products/{code}')
async def edit_product(code: str, session: Session = Depends(get_session)):
    """
        ## Editar um produto
        PUT /products/{id}
    """
    product = session.query(Product).filter(Product.code == code).first()
    ## ainda vou continuar, calma ae q vou almoçar