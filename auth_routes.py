from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session
from models import User

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.get('/')
async def home():
    return{
        "message": "Rota de autenticação"
    }


@auth_router.post('/create-account')
async def create_account(name, email, password, session=Depends(get_session)):
    user = session.query(User).filter(User.email == email).first()
    if user:
        raise HTTPException(status_code=400, detail='Email already exists')
    session.add(User(name, email, password))
    session.commit()
    return{
        "message": f"User created {email}"
    }