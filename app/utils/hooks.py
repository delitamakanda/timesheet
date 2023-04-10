import falcon
from app.errors import AuthenticationError

def auth_required(request, response, resource, params):
    if request.context['Authorization'] is None:
        raise AuthenticationError()
