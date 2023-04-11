import falcon
import json
from app import log

from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec

from falcon_apispec import FalconPlugin

from app.schema import UserSchema, TaskSchema


from app.middleware import AuthHandler, JSONTranslator, DatabaseSessionManager
from app.database import db_session, init_session

from app.api.common import base
from app.api.v1 import users
from app.errors import AppError

LOG = log.get_logger()


application = falcon.API(middleware=[JSONTranslator(), AuthHandler(), DatabaseSessionManager(db_session)])

LOG.info('App initialized')

application.add_route('/', base.BaseResource())
application.add_route('/v1/users', users.Collection())
application.add_route('/v1/users/{user_id}', users.Item())
application.add_route('/v1/users/self/login', users.Self())
application.add_route('/v1/users/self/resetpassword', users.Self())

application.add_error_handler(AppError, AppError.handle)

init_session()

spec = APISpec(
    title='Timesheet API',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FalconPlugin(application),
        MarshmallowPlugin(),
    ]
)

# Open API spec

spec.components.schema('User', schema=UserSchema)
spec.components.schema('Task', schema=TaskSchema)


spec.path(path='/', resource=application.add_route('/', base.BaseResource()))
spec.path(path='/v1/users', resource=application.add_route('/v1/users', users.Collection()))
spec.path(path='/v1/users/:user_id', resource=application.add_route('/v1/users/{user_id}', users.Item()))
spec.path(path='/v1/users/self/login', resource=application.add_route('/v1/users/self/login', users.Self()))
spec.path(path='/v1/users/self/resetpassword', resource=application.add_route('/v1/users/self/resetpassword', users.Self()))


print(json.dumps(spec.to_dict(), indent=4))

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server("127.0.0.1", 5000, application)
    httpd.serve_forever()
