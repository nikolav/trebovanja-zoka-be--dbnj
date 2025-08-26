
from src.graphql.setup        import mutation
from src.services.collections import Collections
from src.utils                import Utils
from src.services.io          import IO
from src.config               import Config


# collectionsDocsUpsert(topic: String!, patches: [JsonData!]!): JsonData!
@mutation.field('collectionsDocsUpsert')
def resolve_collectionsDocsUpsert(_obj, _info, topic, patches):
  r       = Utils.ResponseStatus()
  changes = 0

  try:
    if not topic:
      raise Exception('collection name invalid')
    
    changes  = Collections.commit(topic, patches = patches)
    r.status = changes
  
  except Exception as e:
    r.error = e

  else:
    if 0 < changes:
      IO.signal(f'{Config.COLLECTIONS_DOCS_UPDATED}{topic}')

  return r.dump()


