from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session
from models import User
from security import bcrypt_context
from schemas import CreateAccountSchema

auth_router = APIRouter(prefix='/auth', tags=['auth'])

@auth_router.get('/')
async def home():
    return{
        "message": "Rota de autenticação"
    }


@auth_router.post('/create-account')
async def create_account(create_account: CreateAccountSchema, session=Depends(get_session)):
    user = session.query(User).filter(User.email == create_account.email).first()
    if user:
        raise HTTPException(status_code=400, detail='Email already exists')
    encrypted_password = bcrypt_context.hash(create_account.password)
    new_user = User(create_account.name, create_account.email, encrypted_password)
    session.add(new_user)
    session.commit()
    return{
        "message": f"User created {create_account.email}"
    }

