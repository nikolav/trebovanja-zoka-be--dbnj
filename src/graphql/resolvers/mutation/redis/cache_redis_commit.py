
import json

from src.graphql.setup          import mutation
from src.utils.merge_strategies import dict_deepmerger_extend_lists as merger
from src.utils                  import Utils
from src.config                 import Config

from flask_app import io


# cacheRedisCommit(cache_key: String!, patch: JsonData, merge: Boolean ): JsonData!
@mutation.field('cacheRedisCommit')
def resolve_cacheRedisCommit(_obj, _info, cache_key, patch = None, merge = True):
  r       = Utils.ResponseStatus()
  cache   = None
  changes = 0

  try:
    if patch:
      from flask_app import redis_client
      _err, client = redis_client
      
      if merge:
        cache = {} if not client.exists(cache_key) else json.loads(client.get(cache_key).decode())
        merger.merge(cache, patch)

      else:
        cache = patch

      client.set(cache_key, json.dumps(cache))

      changes += 1

  except Exception as err:
    r.error = err

  else:
    r.status = 'ok'
    if 0 < changes:
      err_, ioclient = io
      ioclient.emit(f'{Config.IOEVENT_REDIS_CACHE_KEY_UPDATED_prefix}{cache_key}')

  return r.dump()


