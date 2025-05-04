import datetime

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import Relationship

from ..database.database import Base
from ..utils.roles import Role


class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, unique=True)
    username = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(ENUM(Role), default=Role.USER, nullable=True)
    first_name = Column(String(50), nullable=True)
    last_name = Column(String(50), nullable=True)
    created_date = Column(DateTime, default=datetime.datetime.now)
    updated_date = Column(DateTime, default=datetime.datetime.now)

    tokens = Relationship("Token", back_populates="user")
