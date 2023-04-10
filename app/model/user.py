from sqlalchemy import Column, String, Integer, LargeBinary
from sqlalchemy.orm import relationship

from app.model import Base
from app.config import UUID_LENGTH
from app.utils import alchemy


class User(Base):
    user_id = Column(Integer, primary_key=True)
    username = Column(String(20), nullable=False, unique=True)
    email = Column(String(120), nullable=False, unique=True)
    password = Column(String(120), nullable=False)
    info = Column(String(), nullable=True)
    token = Column(String(255), nullable=False)
    sid = Column(String(UUID_LENGTH), nullable=False)

    def __repr__(self):
        return '<User {}>'.format(self.username)


    @classmethod
    def find_by_email(cls, session, email):
        return session.query(User).filter(User.email == email).one()
    
    @classmethod
    def get_id(cls):
        return User.user_id
    
    FIELDS = { "username": str, "email": str, "info": alchemy.passby, "token": str }

    FIELDS.update(Base.FIELDS)

