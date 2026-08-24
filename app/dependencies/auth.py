from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from sqlalchemy.orm import Session, sessionmaker

from app.core.database import engine
from app.core.security import ALGORITHM, SECRET_KEY, oauth2_schema
from app.models import User


def get_session():
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()


def verify_token(
    token: str = Depends(oauth2_schema),
    session: Session = Depends(get_session),
):
    try:
        dict_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        id_user = dict_info.get("sub")
    except JWTError:
        raise HTTPException(
            status_code=400,
            detail="Erro, verifique a validade do token e tente novamente",
        )

    user = session.query(User).filter(User.id == id_user).first()

    return user