import falcon
import json

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict

from app import log
from app.utils.alchemy import new_alchemy_encoder
from app.config import API_NAME, POSTGRES
from app.database import engine
from app.errors import NotSupportedError

LOG = log.get_logger()

class BaseResource(object):
    HELLO_WORLD = {
        'server': '%s' % API_NAME,
        'database': '%s (%s)' % (engine.name, POSTGRES['host'])
    }

    def to_json(self, data):
        return json.dumps(data)

    def from_db_to_json(self, db):
        return json.dumps(db, cls=new_alchemy_encoder())

    def on_error(self, response, error=None):
        response.status = error["status"]
        meta = OrderedDict()
        meta["message"] = error["message"]
        meta["code"] = error["code"]

        obj = OrderedDict()
        obj["meta"] = meta
        response.body = self.to_json(obj)

    def on_success(self, response, data=None):
        response.status = falcon.HTTP_200
        meta = OrderedDict()
        meta["message"] = "Success"
        meta["code"] = 200
        obj = OrderedDict()
        obj["meta"] = meta
        obj["data"] = data
        response.body = self.to_json(data)

    def on_get(self,request,response):
        if request.path == '/':
            response.status = falcon.HTTP_200
            response.body = self.to_json(self.HELLO_WORLD)
        else:
            raise NotSupportedError(method="GET", url=request.path)

    def on_post(self,request,response):
        raise NotSupportedError(method="POST", url=request.path)

    def on_put(self,request,response):
        raise NotSupportedError(method="PUT", url=request.path)

    def on_delete(self,request,response):
        raise NotSupportedError(method="DELETE", url=request.path)

