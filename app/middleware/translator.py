import json
import falcon

from app.errors import InvalidRequest

class JSONTranslator(object):
    def process_request(self, request, response):
        if request.content_type == 'application/json':
            try:
                request_body = request.stream.read()
            except Exception:
                message = 'Could not read request body'
                raise falcon('Bad Request', message)
            try:
                request.context['data'] = json.loads(request_body.decode('utf-8'))
            except ValueError:
                raise InvalidRequest('No JSON object could be decoded or malformed')
            except UnicodeDecodeError:
                raise InvalidRequest('JSON object could not be decoded')
        else:
            request.context['data'] = None
