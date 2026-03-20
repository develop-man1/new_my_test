from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import timedelta, datetime, timezone
import jwt

from .config import settings


pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
        
    payload = {
        "sub": subject,
        "exp": expire,
    }
    
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    
    return token


def decode_access_token(token: str) -> dict:
    
    try:
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[settings.jwt_algorithm])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token invalid"
        )
        
    
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    
    payload = decode_access_token(token)
    user_id = str(payload.get("sub"))
    
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
        
    return user_id