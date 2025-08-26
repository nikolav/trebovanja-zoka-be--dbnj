
from src.graphql.setup         import query
from src.services.collections  import Collections
from src.schemas.serialization import SchemaMongoDocData
from src.utils                 import Utils


# collectionsDocsByTopic(topic: String!, config: JsonData): JsonData!
@query.field('collectionsDocsByTopic')
def resolve_collectionsDocsByTopic(_obj, _info, topic, config = None):
  r = Utils.ResponseStatus()

  try:
    r.status = SchemaMongoDocData(many = True).dump(Collections.lsa(topic)) if topic else []

  except Exception as e:
    r.error = e
  
  return r.dump()

