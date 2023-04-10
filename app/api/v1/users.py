import re
import falcon

from sqlalchemy.orm.exc import NoResultFound
from cerberus import Validator
from cerberus.errors import ValidationError
from app import log
from app.api.common import BaseResource
from app.utils.hooks import auth_required
from app.utils.auth import encrypt_password, hash_password, verify_password, uuid
from app.model import User
from app.errors import AppError, InvalidRequest, NotFoundError, PasswordNotMatchError

LOG = log.get_logger()


FIELDS = {
    "username": {"type": "string", "required": True, "min_length": 3, "max_length": 20},
    "email": {"type": "string", "required": True, "min_length": 3, "max_length": 255, "regex": "[a-zA-Z0-9._-]+@(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,4}"},
    "password": {"type": "string", "required": True, "min_length": 6, "max_length": 64, "regex": "[0-9a-zA-Z]\w{3,14}"},
    "info": {"type": "string", "required": False }
}

def validate_user_create(request, response, resource, params):
    schema = {
        "username": FIELDS["username"],
        "email": FIELDS["email"],
        "password": FIELDS["password"],
        "info": FIELDS["info"]
    }
    validator = Validator(schema)
    if not validator.validate(request.context["data"]):
        raise InvalidRequest(validator.errors)

class Collection(BaseResource):
    @falcon.before(validate_user_create)
    def on_post(self, request, response):
        session = request.context["session"]
        data = request.context["data"]
        if data:
            user = User()
            user.username = data["username"]
            user.email = data["email"]
            user.password = hash_password(data["password"]).decode('utf-8')
            user.info = data["info"] if "info" in data else None
            sid = uuid()
            user.sid = sid
            user.token = encrypt_password(sid).decode('utf-8')
            session.add(user)
            self.on_success(response, None)
        else:
            raise InvalidRequest(request.context['data'])

    @falcon.before(auth_required)
    def on_get(self, request, response):
        session = request.context["session"]
        users = session.query(User).all()
        if users:
            obj = [user.to_dict() for user in users]
            self.on_success(response, obj)
        else:
            raise AppError()

    @falcon.before(auth_required)
    def on_put(self, request, response):
        pass

    @falcon.before(auth_required)
    def on_delete(self, request, response):
        pass


class Item(BaseResource):
    @falcon.before(auth_required)
    def on_get(self, request, response, user_id):
        session = request.context["session"]
        try:
            user = User.find_one(session, user_id)
            self.on_success(response, user.to_dict())
        except NoResultFound:
            raise NotFoundError("user {} not found".format(user_id))

class Self(BaseResource):
    LOGIN = 'login'
    RESET_PASSWORD = 'resetpassword'

    def on_get(self, request, response):
        cmd = re.split("\\W+", request.path)[-1:][0]
        if cmd == self.LOGIN:
            self.process_login(request, response)
        elif cmd == self.RESET_PASSWORD:
            self.process_reset_password(request, response)

    def process_login(self, request, response):
        data = request.context["data"]
        email = data["email"]
        password = data["password"]
        session = request.context["session"]
        try:
            user = User.find_by_email(session, email)
            if verify_password(password, user.password.encode('utf-8')):
                self.on_success(response, user.to_dict())
            else:
                raise PasswordNotMatchError()
        except NoResultFound:
            raise NotFoundError("user {} not found".format(email))

    @falcon.before(auth_required)
    def process_reset_password(self, request, response):
        pass