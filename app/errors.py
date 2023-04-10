import json
import falcon

try:
    from collections import OrderedDict
except ImportError:
    OrderedDict = dict


OK = { "status": falcon.HTTP_200, "code" : 200  }

UNKNOWN_ERROR = { "status": falcon.HTTP_500, "code": 500, "message": "An unknown error occurred." }

AUTH_ERROR = { "status": falcon.HTTP_401, "code": 401, "message": "Authentication failed." }

BAD_REQUEST = { "status": falcon.HTTP_400, "code": 400, "message": "Bad request." }

DATABASE_ERROR = { "status": falcon.HTTP_500, "code": 500, "message": "Database error." }


NOT_FOUND = { "status": falcon.HTTP_404, "code": 404, "message": "Not found." }

NOT_SUPPORTED = { "status": falcon.HTTP_405, "code": 405, "message": "Method not supported." }

class AppError(Exception):
    def __init__(self, error=UNKNOWN_ERROR, description=None):
        self.error = error
        self.error["description"] = description

    @property
    def status(self):
        return self.error["status"]

    @property
    def code(self):
        return self.error["code"]

    @property
    def message(self):
        return self.error["message"]
    
    @property
    def description(self):
        return self.error["description"]
    
    @staticmethod
    def handle(exception, request, response, error=None):
        response.status = exception.status
        meta = OrderedDict()
        meta["code"] = exception.code
        meta["message"] = exception.message
        if exception.description:
            meta["description"] = exception.description
        response.body = json.dumps({"meta": meta})

class InvalidRequest(AppError):
    def __init__(self, description=None):
        super().__init__(BAD_REQUEST)
        self.error["description"] = description

class DatabaseError(AppError):
    def __init__(self, error, args=None, params=None):
        super().__init__(error)
        obj = OrderedDict()
        obj["details"] = ", ".join(args)
        obj["params"] = str(params)
        self.error["description"] = obj

class NotSupportedError(AppError):
    def __init__(self, method=None, url=None):
        super().__init__(NOT_SUPPORTED)
        if method and url:
            self.error["description"] = "method: %s, url: %s" % (method, url)

class NotFoundError(AppError):
    def __init__(self, description=None):
        super().__init__(NOT_FOUND)
        self.error["description"] = description

class PasswordNotMatchError(AppError):
    def __init__(self, description=None):
        super().__init__(BAD_REQUEST)
        self.error["description"] = description


class AuthenticationError(AppError):
    def __init__(self, description=None):
        super().__init__(AUTH_ERROR)
        self.error["description"] = description

