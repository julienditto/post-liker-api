from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from . import database
from sqlalchemy.orm import Session
from . import models
from os import environ


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY=environ.get('SECRET_KEY')
ALGOIRTHM=environ.get('ALGOIRTHM')
ACCESS_TOKEN_EXPIRE_MINUTES=environ.get('ACCESS_TOKEN_EXPIRE_MINUTES')

def create_access_token(data: dict):
    float_expire = float(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=float_expire)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGOIRTHM)
    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGOIRTHM])
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                                          detail="could not validate credentials", 
                                          headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user