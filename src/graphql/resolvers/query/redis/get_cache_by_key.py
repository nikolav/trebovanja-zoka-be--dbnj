
from src.graphql.setup  import query
from src.utils          import Utils
from src.services.cache import Cache


# cacheRedisGetCacheByKey(cache_key: String!): JsonData!
@query.field('cacheRedisGetCacheByKey')
def resolve_cacheRedisGetCacheByKey(_obj, _info, cache_key):  
  r     = Utils.ResponseStatus()
  cache = None

  try:
    cache = Cache.key(cache_key)
  
  except Exception as err:
    r.error = err

  else:
    r.status = { 'cache': { cache_key: cache } }


  return r.dump()

