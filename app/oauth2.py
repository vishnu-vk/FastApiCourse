from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from . import schemas, database, models
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "login")


#SECRET KEY
SECRET_KEY = settings.secret_key

#ALGORITHM
ALGORITHM = settings.algorithm

ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes



def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm= ALGORITHM)

    return encoded_jwt



def verity_access_token(token: str, credentails_exceptions):

    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])

        id: str = payload.get("user_id")

        if id is None:
            raise credentails_exceptions

        token_data = schemas.Token(id= id)
    
    except JWTError:
        raise credentails_exceptions

    return token_data



def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    
    credentails_exceptions = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= f"Could not validate the credentials", headers= {"WWW-Authenticate": "Bearer"})

    token: schemas.Token = verity_access_token(token, credentails_exceptions)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user 

