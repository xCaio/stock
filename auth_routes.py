from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import get_session
from models import User
from security import bcrypt_context
from schemas import CreateAccountSchema, LoginSchema

auth_router = APIRouter(prefix='/auth', tags=['auth'])

def authenticate_user(email,password,session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    else:
        return user


@auth_router.get('/')
async def home():
    return{
        "message": "Rota de autenticação"
    }


@auth_router.post('/create-account')
async def create_account(create_account: CreateAccountSchema, session: Session = Depends(get_session)):
    user = session.query(User).filter(User.email == create_account.email).first()
    if user:
        raise HTTPException(status_code=400, detail='Email Ja existe')
    encrypted_password = bcrypt_context.hash(create_account.password)
    new_user = User(create_account.name, create_account.email, encrypted_password)
    session.add(new_user)
    session.commit()
    return{
        "message": f"Usuario criado {create_account.email}"
    }

@auth_router.post('/login')
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = authenticate_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=404, detail='Credenciais incorretas')
    return{
        "message": f"usuario logado com sucesso {login_schema.email}",
        "token_type":"Bearer"
    }