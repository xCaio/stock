from fastapi import APIRouter

supplies_router = APIRouter(prefix='/supplies', tags=['supplies'])

@supplies_router.get('/')
async def home():
    return {
        "message": "Rota inicial dos insumos"
    }