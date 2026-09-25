# project/starter/app/auth.py
# Module 5 Project — JWT and password utilities
#
# TODO: Implement password hashing and JWT functions

from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.database import get_db
import os
from app.models.user import User

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# TODO: Create pwd_context with bcrypt
pwd_context = None  # TODO
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)
http_bearer = HTTPBearer()



def hash_password(password: str) -> str:
    """Hash a plain-text password using pwd_context."""
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    """TODO: verify with pwd_context"""
    
    return pwd_context.verify(plain, hashed)



def create_access_token(data: dict) -> str:
    """TODO: create JWT with expiry"""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta( 
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode["exp"] = expire
    
    return jwt.encode(
        to_encode, SECRET_KEY, algorithm=ALGORITHM)



def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(http_bearer),
    db: Session = Depends(get_db),
):
    """TODO: extract token from credentials.credentials, decode JWT, and return current user"""
    token = credentials.credentials 
    try: 
        payload = jwt.decode(
            token, 
            SECRET_KEY, 
            algorithms=[ALGORITHM])
        username = payload.get("sub")

        if username is None:
            raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid authentication credentials",
        )

    except JWTError: 
        raise HTTPException( 
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials", ) 
            
    user = db.query(User).filter(
        User.username == username).first()    

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )
    
    return user

