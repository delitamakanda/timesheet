from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey

from app.model import Base
from app.config import UUID_LENGTH
from app.utils import alchemy
from app.model.user import User
from app.model.task import Task

from sqlalchemy.orm import relationship


class TimeEntry(Base):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.user_id'), nullable=False)
    user = relationship("User", backref="user")
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)

    def __repr__(self):
        return '<TimeEntry {}>'.format(self.id)
    
    @classmethod
    def get_id(cls):
        return TimeEntry.id
    
    FIELDS = { }

    FIELDS.update(Base.FIELDS)

