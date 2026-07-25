from fastapi import APIRouter, Depends, HTTPException
from dependencies import verify_token, get_session
from sqlalchemy.orm import Session
from models import Product, User
from schemas import SuppliesSchema, ProductResponseSchema, ProductUpdateSchema
from typing import List


supplies_router = APIRouter(prefix='/supplies', tags=['supplies'], dependencies=[Depends(verify_token)])

@supplies_router.get('/')
async def home():
    return {
        "message": "Rota inicial dos insumos"
    }

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
async def edit_product(code: str, product_update: ProductUpdateSchema ,session: Session = Depends(get_session)):
    """
        ## Editar um produto
        PUT /products/{id}
    """
    product = session.query(Product).filter(Product.code == code).first()
    if not product:
        raise HTTPException(status_code=404, detail='Produto nao encontrado')
    
    code_exists = session.query(Product).filter(Product.code == product_update.code).first()
    if code_exists:
        raise HTTPException(status_code=400, detail='O codigo já está cadastrado')
    
    product.code = product_update.code
    product.product_type = product_update.product_type
    product.stock = product_update.stock
    session.commit()
    session.refresh(product)

    return {
        "message": "Produto atualizado com sucesso",
        "code": product.code, 
        "product_type": product.product_type, 
        "stock": product.stock, 
    }

@supplies_router.get('/products')
async def get_products(
    type: str | None = None, 
    active: bool | None = None, 
    search: str | None = None, 
    session: Session = Depends(get_session)
):
    query = session.query(Product)
    if type:
        query = query.filter(Product.product_type == type)
    if active is not None:
        query = query.filter(Product.active == active)
    if search:
        query = query.filter(Product.code.ilike(f"%{search.strip()}%"))
    return query.all()

@supplies_router.patch('/products/{code}/inactive')
async def inactive_product(code:str, session:Session = Depends(get_session)):
    product = session.query(Product).filter(Product.code == code).first()
    if not product:
        raise HTTPException(status_code=404, detail='Produto nao encontrado')
    product.active=False
    session.commit()
    session.refresh(product)
    return{
        "message": f"Produto {product.code} Desativado"
    }

@supplies_router.patch('/products/{code}/active')
async def active_product(code:str, session:Session = Depends(get_session)):
    product = session.query(Product).filter(Product.code == code).first()
    if not product:
        raise HTTPException(status_code=404, detail='Produto nao encontrado')
    product.active=True
    session.commit()
    session.refresh(product)
    return{
        "message": f"Produto {product.code} Ativado"
    }