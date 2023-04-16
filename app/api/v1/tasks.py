import re
import falcon

from sqlalchemy.orm.exc import NoResultFound
from cerberus import Validator
from cerberus.errors import ValidationError
from app import log
from app.model import Task
from app.api.common import BaseResource
from app.errors import AppError


LOG = log.get_logger()


class TaskResource(BaseResource):
    
    def on_get(self, req, resp, task_id):
        session = req.context['session']
        try:
            task = Task.find_one(session, id=task_id)
            self.on_success(resp, task.to_dict())
        except NoResultFound:
            raise AppError(falcon.HTTP_404, 'Task not found')

