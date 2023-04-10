from app import log
from app.utils.auth import decrypt_password
from app.errors import AuthenticationError

LOG = log.get_logger()

class AuthHandler(object):
    def process_request(self, request, response, resource=None):
        LOG.debug("Authorization: %s", request.auth)
        if request.auth is not None:
            token = decrypt_password(request.auth)
            if token is None:
                raise AuthenticationError("Invalid token %s" % request.auth)
            else:
                request.context["Authorization"] = token.decode("utf-8")
        else:
            request.context["Authorization"] = None
