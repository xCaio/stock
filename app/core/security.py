from passlib.context import CryptContext
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
load_dotenv()

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
TOKEN_ACESS_EXPIRES_MINUTES = int(os.getenv('TOKEN_ACESS_EXPIRES_MINUTES'))
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")