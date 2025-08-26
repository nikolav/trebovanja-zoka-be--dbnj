
from src.graphql.setup          import mutation
from src.utils                  import Utils
from src.config                 import Config
from src.services.cache         import Cache
from src.services.io            import IO


# cacheRedisCommit(cache_key: String!, patch: JsonData, merge: Boolean ): JsonData!
@mutation.field('cacheRedisCommit')
def resolve_cacheRedisCommit(_obj, _info, cache_key, patch = None, merge = True):
  r       = Utils.ResponseStatus()
  changes = 0

  try:
    Cache.commit(cache_key, patch = patch, merge = merge)
    changes += 1

  except Exception as e:
    r.error = e

  else:
    r.status = 'ok'
    if 0 < changes:
      IO.signal(f'{Config.IOEVENT_REDIS_CACHE_KEY_UPDATED_prefix}{cache_key}')

  return r.dump()


