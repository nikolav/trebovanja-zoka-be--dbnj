# import os
import re
from datetime import datetime, timezone

import jwt
from flask import request

from src.config   import Config
from src.utils.re import RE_MATCH_AUTH_HEADER


def with_created_at(payload):
  payload[Config.KEY_TOKEN_CREATED_AT] = str(datetime.now(timezone.utc))
  return payload


class JWT:
  
  @staticmethod
  def encode(jsonPayload):
    return JWT.encode_secret(jsonPayload, Config.JWT_SECRET_ACCESS_TOKEN)
  
  @staticmethod
  def encode_secret(jsonPayload, secret):
    return jwt.encode(with_created_at(jsonPayload),
      secret, algorithm = 'HS256')
  
  @staticmethod
  def decode(sToken):
    return JWT.decode_secret(sToken, Config.JWT_SECRET_ACCESS_TOKEN)

  @staticmethod
  def decode_secret(sToken, secret):
    return jwt.decode(sToken, secret, algorithms = ('HS256',))
    
  @staticmethod
  def expired(token):
    jsonTokenPayload = token if isinstance(token, dict) else JWT.decode(token)
    ddif = datetime.now(timezone.utc) - datetime.fromisoformat(jsonTokenPayload[Config.KEY_TOKEN_CREATED_AT])
    return Config.JWT_EXPIRE_SECONDS < ddif.total_seconds()
  
  @staticmethod
  def token_from_request():
    return re.match(RE_MATCH_AUTH_HEADER, 
                    request.headers.get('Authorization')).groups()[0]

  @staticmethod
  def is_valid(token, *, 
                   secret           = Config.JWT_SECRET_ACCESS_TOKEN, 
                   verify_signature = True,
                  ):

    try:
      jwt.decode(
        token,
        secret if verify_signature else None,
        algorithms = ('HS256',),
        options    = { 'verify_signature': verify_signature },
      )
    
    except (jwt.DecodeError, jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False
    
    return True
  

