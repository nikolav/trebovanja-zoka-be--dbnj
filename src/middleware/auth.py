
import re
from flask import request
from flask import abort
from flask import make_response
from flask import g

from firebase_admin import auth

from src.config       import Config
from src.services.jwt import JWT


def authenticate():
  # @before_request
  
  error   = '@error:authenticate:mw'
  payload = None
  token   = None
  uid     = None
  user    = None

  # do not redirect `CORS` preflight `OPTIONS` requests, send success/2xx
  if 'OPTIONS' == request.method.upper():
    return abort(make_response('', 200))
  
  # allow open routes
  if any(re.match(p, request.path) for p in Config.PATHS_SKIP_AUTH):
    return
  
  # @auth
  try:
    token = JWT.token_from_request()

    if JWT.expired(token):
      raise Exception('access denied')
    
    if not JWT.is_valid(token):
      raise Exception('access denied')
    
    payload = JWT.decode(token)
    uid     = payload['uid']
    
    user = auth.get_user(uid)
  
  except Exception as e:
    error = e
  
  else:
    if user:
      g.user = user
      return

  # 401/unauthenticated otherwise
  return abort(make_response({ 'error': str(error) }, 401))

