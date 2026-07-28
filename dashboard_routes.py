from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session
from dependencies import get_session
from models import Product, StockMovement
from datetime import datetime, timedelta

today = datetime.now().date()
start = datetime.combine(today, datetime.min.time())
end = start + timedelta(days=1)

dashboard_router = APIRouter(prefix='/dashboard', tags=['dashboard'])

@dashboard_router.get('/')
async def dashboard(session: Session = Depends(get_session)):
    total_products = session.query(func.sum(Product.stock)).scalar()
    entryies_today = session.query(StockMovement).filter(
        StockMovement.movement_type == "entrada",
        StockMovement.created_at >= start,
        StockMovement.created_at < end
        ).count()
    outputs_today = session.query(StockMovement).filter(
        StockMovement.movement_type == "saida",
        StockMovement.created_at >= start,
        StockMovement.created_at < end
    ).count()
    low_stock = session.query(Product).filter(Product.stock <= Product.stock_minimum).count()
    low_stock_products = session.query(Product).filter(Product.stock <= Product.stock_minimum).all()
    out_of_stock = session.query(Product).filter(Product.stock == 0).count()
    last_movements = session.query(StockMovement).order_by(StockMovement.created_at.desc()).limit(10).all()
    busiest = session.query(StockMovement.product_id,func.sum(StockMovement.quantity)).group_by(StockMovement.product_id)

    return{
        "cards":{
            "total_produtos": total_products,
            "entradas_hoje": entryies_today,
            "saidas_hoje": outputs_today,
            "sem_estoque": out_of_stock,
            "estoque_baixo": {
                "total": low_stock,
                "produtos": [
                    {
                        "code": p.code,
                        "stock": p.stock,
                        "stock_minimum": p.stock_minimum
                    }
                    for p in low_stock_products
                ]
            },
            "ultimas_movimentacoes": last_movements,
            "mais_movimentado": busiest
        }
    }