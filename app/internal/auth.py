"""Module defining authentication utilities"""

# System imports
from passlib.context import CryptContext
from datetime import datetime, timedelta

# Libs imports
from jose import JWTError, jwt

# Initialize password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Define constants
SECRET_KEY = "OKLM1234567890"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def verify_password(plain_password: str, hashed_password: str):
    """Verify the provided password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    """Hash the provided password"""
    return pwd_context.hash(password)

def create_access_token(*, data: dict, expires_delta: timedelta = None):
    """Create an access token with the provided data"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def authenticate_user(email: str, password: str, db):
    """Authenticate a user with the provided credentials"""
    user = db.get_user_by_email(email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
