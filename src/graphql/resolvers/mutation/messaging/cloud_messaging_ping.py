
from flask       import g
from marshmallow import EXCLUDE

from src.graphql.setup      import mutation
from src.services.messaging import cm_notification_send
from src.schemas.validation import SchemaValidateCloudMessagingMessage
from src.utils              import Utils
from src.services.cache     import Cache


@mutation.field('cloudMessagingPing')
def resolve_cloudMessagingPing(_obj, _info, 
                               payload = {
                                 'title' : 'title --ping', 
                                 'body'  : 'body --ping',
                                }):
  r   = Utils.ResponseStatus()
  res = None

  try:
    res = cm_notification_send(
      tokens  = [tok for tok, val in Cache.cloud_messaging_tokens(g.user.uid).items() if True == val],
      payload = SchemaValidateCloudMessagingMessage(unknown = EXCLUDE).load(payload))

  except Exception as e:
    r.error = e
  
  else:
    r.status = str(res)

  return r.dump()

