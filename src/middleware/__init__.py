
from flask import request
from flask import abort
from flask import make_response


def handle_before_request():
  # @before_request

  # do not redirect `CORS` preflight `OPTIONS` requests, send success/2xx
  if 'OPTIONS' == request.method.upper():
    return abort(make_response('', 200))
