

from flask      import g
from flask      import Blueprint
from flask_cors import CORS

from firebase_admin import auth

from src.middleware.arguments_schema import arguments_schema
from src.schemas.validation          import SchemaAuthArguments
from src.services.jwt                import JWT


def _user_to_dict(user):
  return {
    'uid': user.uid,
    'email': user.email,
    'phone_number': user.phone_number,
    'display_name': user.display_name,
    'photo_url': user.photo_url,
    'email_verified': user.email_verified,
    'disabled': user.disabled,
    'custom_claims': user.custom_claims,
    'provider_data': [p.__dict__ for p in user.provider_data],
    'tokens_valid_after_time': str(user.tokens_valid_after_timestamp),
  }

bp_auth = Blueprint('auth', __name__, url_prefix = '/auth')

# cors blueprints for cross-domain
CORS(bp_auth)

@bp_auth.route('/authenticate', methods = ('POST',))
@arguments_schema(SchemaAuthArguments())
def resolve_route_authenticate():
  error = '@error:authenticate:access_token'
  token = None
  user  = None
  uid   = g.arguments['uid']

  try:
    user = auth.get_user(uid)
    if not user:
      raise Exception('access denied')
    
    token = JWT.encode({ 'uid': user.uid })

  except Exception as e:
    error = e

  else:
    if token:
      return { 'token': token }, 200
  
  return { 'error': str(error) }, 401


@bp_auth.route('/who', methods = ('GET',))
def auth_who():
  error = '@error/auth:who'
  try:
    # send user data
    return _user_to_dict(g.user), 200
  
  except Exception as err:
    error = err
  
  return { 'error': str(error) }, 500


