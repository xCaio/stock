from fastapi import APIRouter, Depends, HTTPException
from dependencies import get_session, verify_token
from sqlalchemy.orm import Session
from models import User
from schemas import UserUpdateSchema, UserRoleSchema
from security import bcrypt_context


users_router = APIRouter(prefix='/users', tags=['users'], dependencies=[Depends(verify_token)])

@users_router.get('/')
async def get_users(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    query_users = session.query(User).all()
    if not query_users:
        raise HTTPException(404, "Nenhum usuário encontrado")
    if user.role != "admin":
        raise HTTPException(401, "Voce nao tem autorizacao para realizar essa operacao")
    return query_users

@users_router.get('/{id}')
async def get_user_id(id: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    users = session.query(User).filter(User.id == id).first()
    if not users:
        raise HTTPException(404, "Usuario nao encontrado")
    if user.role != "admin":
        raise HTTPException(401, "Voce nao tem autorizacao para realizar essa operacao")
    return users

@users_router.put('/{id}')
async def change_user_info(id: int, user_schema: UserUpdateSchema,session: Session = Depends(get_session), user: User = Depends(verify_token)):
    if user.role != "admin":
        raise HTTPException(401, "Voce nao tem autorizacao para realizar essa operacao")
    query_user = session.query(User).filter(User.id == id).first()
    if not query_user:
            raise HTTPException(404, "Usuário não encontrado")
    if user_schema.name is not None:
        query_user.name = user_schema.name
    if user_schema.email is not None:
        query_user.email = user_schema.email
    if user_schema.role is not None:
        query_user.role = user_schema.role
    if user_schema.password is not None:
        query_user.password = bcrypt_context.hash(user_schema.password)

    session.commit()
    session.refresh(query_user)
    return {
        "message": f"Dados do usuario id {query_user.id} alterado"
    }

@users_router.patch('/{id}/role')
async def change_role(id: int, user_schema: UserRoleSchema,session: Session = Depends(get_session), user: User = Depends(verify_token)):
    query_user = session.query(User).filter(User.id == id).first()
    if not query_user:
        raise HTTPException(404, "Usuario nao encontrado")
    if user.role != "admin":
        raise HTTPException(401, "Voce nao tem autorizacao para realizar essa operacao")
    query_user.role = user_schema.role
    session.commit()
    session.refresh(query_user)
    return {
        "message": f"Role do usuário {query_user.name} atualizado para {query_user.role}"
    }