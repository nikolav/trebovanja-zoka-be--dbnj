
from src.graphql.setup        import mutation
from src.utils                import Utils
from src.services.collections import Collections
from src.services.io          import IO
from src.config               import Config


# collectionsDocsDrop(topic: String!, ids: [ID!]!): JsonData!
@mutation.field('collectionsDocsDrop')
def resolve_collectionsDocsDrop(_obj, _info, topic, ids):
  r       = Utils.ResponseStatus()
  changes = 0

  try:
    if not topic or not ids:
      raise Exception('collections:docs:drop input invalid')
    
    changes  = Collections.rm(topic, ids = ids)
    r.status = changes

  except Exception as e:
    r.error = e

  else:
    if 0 < changes:
      IO.signal(f'{Config.COLLECTIONS_DOCS_UPDATED}{topic}')
  
  return r.dump()


  