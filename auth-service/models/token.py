import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String
from sqlalchemy.orm import Relationship

from ..database.database import Base


class Token(Base):
    __tablename__ = "token"

    id = Column(String, primary_key=True, unique=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    access_token = Column(String(450), primary_key=True)
    refresh_token = Column(String(450), nullable=False)
    status = Column(Boolean)
    created_date = Column(DateTime, default=datetime.datetime.now)

    user = Relationship("User", back_populates="tokens")
