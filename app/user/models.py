from passlib.context import CryptContext

from app.database import Base
from sqlalchemy import Column, Integer, String


class UserModel(Base):
    __tablename__ = 'user_db'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    hash_password = Column(String)


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hashed_password(password: str) -> str:
    return password_context.hash(password)


def verify_password(hash_password: str, planed_password: str) -> bool:
    return password_context.verify(hash_password, planed_password)
