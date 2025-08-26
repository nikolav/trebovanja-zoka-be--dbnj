
import json
from flask_app import redis_client

from src.utils.merge_strategies import dict_deepmerger_extend_lists as merger
from src.config                 import Config


class Cache:
  _err, client = redis_client

  @staticmethod
  def key(token):
    return {} if not Cache.client.exists(token) else json.loads(Cache.client.get(token).decode())
  
  @staticmethod
  def auth_profile(uid):
    return Cache.key(f'{Config.AUTH_PROFILE}{uid}')
  
  @staticmethod
  def cloud_messaging_tokens(uid):
    return Cache.auth_profile(uid).get(Config.CLOUD_MESSAGING_TOKENS)
  
  @staticmethod
  def commit(token, *, patch = None, merge = True):
    if patch:
      if merge:
        cache = Cache.key(token)
        merger.merge(cache, patch)

      else:
        cache = patch

      Cache.client.set(token, json.dumps(cache))

