import sys

from fastapi import HTTPException, status
from jose import jwt
from jwt import InvalidTokenError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..config.config import FastAPIConfig
from ..models.token import Token

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(password: str, hashed_pass: str) -> bool:
    return password_context.verify(password, hashed_pass)


def verify_token(token: str, db: Session):
    token_record = db.query(Token).filter(Token.access_token == token).first()
    if not token_record or not token_record.status:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token"
        )
    return token_record


def decodeJWT(jwtoken: str):
    try:
        payload = jwt.decode(
            jwtoken, FastAPIConfig.JWT_SECRET_KEY, FastAPIConfig.ALGORITHM
        )
        return payload
    except InvalidTokenError:
        return None
