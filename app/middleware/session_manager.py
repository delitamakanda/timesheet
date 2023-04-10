import falcon
import sqlalchemy.orm.scoping as scoping
from sqlalchemy.exc import SQLAlchemyError

from app import log
from app import config
from app.errors import DatabaseError, DATABASE_ERROR

LOG = log.get_logger()

class DatabaseSessionManager(object):
    def __init__(self, db_session):
        self._session_factory = db_session
        self._scoped = isinstance(db_session, scoping.ScopedSession)

    def process_request(self, request, response, resource=None):
        request.context['session'] = self._session_factory
    
    def process_response(self, request, response, resource=None, request_succeeded=None):
        session = request.context["session"]

        if config.DB_AUTOCOMMIT:
            try:
                session.commit()
            except SQLAlchemyError as e:
                session.rollback()
                raise DatabaseError(DATABASE_ERROR, e.args, e.params)
        if self._scoped:
            session.remove()
        else:
            session.close()
