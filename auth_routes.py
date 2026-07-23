from fastapi import APIRouter

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.get('/')
async def home():
    return{
        "message": "Rota de autenticação"
    }