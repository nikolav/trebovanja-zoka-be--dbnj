
from flask      import Blueprint
from flask_cors import CORS


bp_testing = Blueprint('testing', __name__, url_prefix = '/testing')

# cors blueprints for cross-domain
CORS(bp_testing)

@bp_testing.route('/', methods = ('POST',))
def resolve_route_testing():
  from src.services.collections  import Collections
  from src.schemas.serialization import SchemaMongoDocData
  
  return SchemaMongoDocData(many = True).dump(Collections.lsa('main'))

