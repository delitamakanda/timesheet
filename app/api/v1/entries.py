import re
import falcon

from sqlalchemy.orm.exc import NoResultFound
from cerberus import Validator
from cerberus.errors import ValidationError
from app import log
from app.model import TimeEntry
from app.api.common import BaseResource
from app.errors import AppError


LOG = log.get_logger()

class TimeEntryResource(BaseResource):

    def on_get(self, request, response, time_entry_id):
        session = request.context['session']
        try:
            time_entry = TimeEntry.find_one(session, id=time_entry_id)
            self.on_success(response, time_entry.to_dict())
        except NoResultFound:
            raise AppError(falcon.HTTP_404, 'Time entry not found')
