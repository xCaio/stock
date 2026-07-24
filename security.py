from passlib.context import CryptContext
from dotenv import load_dotenv
import os
load_dotenv()
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
TOKEN_ACESS_EXPIRES_MINUTES = int(os.getenv('TOKEN_ACESS_EXPIRES_MINUTES'))
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')