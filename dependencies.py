from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from security import oauth2_schema, ALGORITHM, SECRET_KEY
from models import User
from database import engine
from jose import jwt, JWTError

def get_session():
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_token(token: str = Depends(oauth2_schema), session:Session = Depends(get_session)):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_user = dict_info.get("sub")
    except JWTError:
        raise HTTPException(status_code=400, detail='Erro, verifique a validade do token e tente novamente')
    user = session.query(User).filter(User.id == id_user).first()
    return user
