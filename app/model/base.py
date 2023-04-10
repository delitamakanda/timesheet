from sqlalchemy import Column, Integer, String, PrimaryKeyConstraint, DateTime, func, Table
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.ext.declarative import as_declarative

from app import log
from app.utils import alchemy

LOG = log.get_logger()

@as_declarative()
class BaseModel(object):
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @classmethod
    def __table_cls__(cls, *args, **kwargs):
        for obj in args[1:]:
            if (isinstance(obj, Column) and obj.primary_key) or isinstance(obj, PrimaryKeyConstraint):
                return Table(*args, **kwargs)
        return None

    @classmethod
    def find_one(cls, session, id):
        return session.query(cls).filter(cls.get_id() == id).one()

    @classmethod
    def find_all(cls, session):
        return session.query(cls).all()

    @classmethod
    def find_update(cls, session, id, args):
        return session.query(cls).filter(cls.get_id() == id).update(args, synchronize_session=False)

    @classmethod
    def get_id(cls):
        pass

    def to_dict(self):
        intersection = set(self.__table__.columns.keys()) & set(self.FIELDS)
        return dict(
            map(
                lambda key: (
                    key,
                    (lambda value: self.FIELDS[key](value) if value else None)(getattr(self, key)
                    )
                ),
                intersection
            )
        )
    FIELDS = {
        "created_at": alchemy.datetime_to_timestamp,
        "updated_at": alchemy.datetime_to_timestamp
    }

Base = declarative_base(cls=BaseModel)
