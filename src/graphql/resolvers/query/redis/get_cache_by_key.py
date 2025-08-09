
import json

from src.graphql.setup import query
from src.utils         import Utils


# cacheRedisGetCacheByKey(cache_key: String!): JsonData!
@query.field('cacheRedisGetCacheByKey')
def resolve_cacheRedisGetCacheByKey(_obj, _info, cache_key):
  
  r     = Utils.ResponseStatus()
  cache = None

  try:
    from flask_app import redis_client
    _err, client = redis_client

    cache = {} if not client.exists(cache_key) else json.loads(client.get(cache_key).decode())
  
  except Exception as err:
    r.error = err

  else:
    r.status = { 'cache': { cache_key: cache } }


  return r.dump()

