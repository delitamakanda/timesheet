from sqlalchemy import Column, String, Integer, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from app.model import Base
from app.config import UUID_LENGTH
from app.utils import alchemy


class Task(Base):
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(1000), nullable=True)
    entry_id = Column(Integer, ForeignKey("timeentry.id"), nullable=False)
    entry = relationship("TimeEntry", back_populates="timeentry")


    def __repr__(self):
        return '<Task {}>'.format(self.title)
    
    @classmethod
    def get_id(cls):
        return Task.id
    
    FIELDS = { "title": str, "description": str }

    FIELDS.update(Base.FIELDS)

