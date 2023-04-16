import falcon
import json
import yaml
from app import log

from apispec.ext.marshmallow import MarshmallowPlugin
from apispec import APISpec

from falcon_apispec import FalconPlugin

from app.schema import UserSchema, TaskSchema


from app.middleware import AuthHandler, JSONTranslator, DatabaseSessionManager
from app.database import db_session, init_session

from app.api.common import base
from app.api.v1 import users, tasks, entries
from app.errors import AppError

LOG = log.get_logger()


application = falcon.API(middleware=[JSONTranslator(), AuthHandler(), DatabaseSessionManager(db_session)])

LOG.info('App initialized')

application.add_route('/', base.BaseResource())
application.add_route('/v1/users', users.Collection())
application.add_route('/v1/users/{user_id}', users.Item())
application.add_route('/v1/users/self/login', users.Self())
application.add_route('/v1/users/self/resetpassword', users.Self())

application.add_route('/v1/tasks/{task_id}', tasks.TaskResource())
application.add_route('/v1/timeentries/{time_entry_id}', entries.TimeEntryResource())

application.add_error_handler(AppError, AppError.handle)

init_session()

spec = APISpec(
    title='Timesheet API',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FalconPlugin(application),
        MarshmallowPlugin(),
    ],
    info=dict(description='minimal api for timesheet')
)

# Open API spec

spec.components.schema('User', schema=UserSchema)
spec.components.schema('Task', schema=TaskSchema)


spec.path(path='/', resource=application.add_route('/', base.BaseResource()), operations=dict(get=(dict(description='hello world', responses={"200": {"description": "hello world"}}))), tags=['users'])

spec.path(path='/v1/users', resource=application.add_route('/v1/users', users.Collection()), operations=dict(get=dict(summary='get all users', responses={"200": {"description": "get all users"}}), post=dict(summary='create user', responses={"201": {"description": "create user"}})))


spec.path(path='/v1/users/:user_id', resource=application.add_route('/v1/users/{user_id}', users.Item()), operations=dict(get=dict(summary='get user by id', responses={"200": {"description": "get user by id"}, "404": {"description": "user not found"}})))

spec.path(path='/v1/tasks/:task_id', resource=application.add_route('/v1/tasks/{task_id}', tasks.TaskResource()), operations=dict(get=dict(summary='get task by id', responses={"200": {"description": "get task by id"}, "404": {"description": "task not found"}})))

spec.path(path='/v1/timeentries/:time_entry_id', resource=application.add_route('/v1/timeentries/{time_entry_id}', entries.TimeEntryResource()), operations=dict(get=dict(summary='get time entry by id', responses={"200": {"description": "get time entry by id"}, "404": {"description": "time entry not found"}})))

spec.path(path='/v1/users/self/login', resource=application.add_route('/v1/users/self/login', users.Self()), operations=dict(get=dict(summary='login user', responses={"200": {"description": "login user"}})))

spec.path(path='/v1/users/self/resetpassword', resource=application.add_route('/v1/users/self/resetpassword', users.Self()), operations=dict(get=dict(summary='reset password', responses={"200": {"description": "reset password"}})))


print(spec.to_yaml())

if __name__ == '__main__':
    from wsgiref import simple_server
    httpd = simple_server.make_server("127.0.0.1", 5000, application)
    httpd.serve_forever()
