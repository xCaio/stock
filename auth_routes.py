from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from dependencies import get_session, verify_token
from models import User
from security import bcrypt_context, TOKEN_ACESS_EXPIRES_MINUTES, SECRET_KEY, ALGORITHM
from schemas import CreateAccountSchema, LoginSchema
from datetime import timezone, timedelta, datetime
from jose import jwt

auth_router = APIRouter(prefix='/auth', tags=['auth'])

def authenticate_user(email,password,session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    else:
        return user

def create_access_token(id_user, duration= timedelta(minutes=TOKEN_ACESS_EXPIRES_MINUTES)):
    expiration_date = datetime.now(timezone.utc) + duration
    dict_info = {"sub": str(id_user), "exp": expiration_date}
    encode = jwt.encode(dict_info, SECRET_KEY, ALGORITHM)
    return encode
    
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
    access_token = create_access_token(user.id)
    refresh_token = create_access_token(user.id, duration=timedelta(days=7))
    return{
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type":"Bearer"
    }

@auth_router.post('/login-form')
async def login(login_form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(login_form.username, login_form.password, session)
    if not user:
        raise HTTPException(status_code=404, detail='Credenciais incorretas')
    access_token = create_access_token(user.id)
    return{
        "access_token": access_token,
        "token_type":"Bearer"
    }

@auth_router.get('/refresh')
async def refresh_token(user: User = Depends(verify_token)):
    access_token = create_access_token(user.id)

    return {
        "access_token" : access_token,
        "token_type": "Bearer"
    }

