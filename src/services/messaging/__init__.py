
from firebase_admin import messaging


def cm_notification_send(*, tokens, payload, image = None):
  return messaging.send_each(
    [messaging.Message(
        notification = messaging.Notification(
          title = payload['title'],
          body  = payload['body'],
          image = image,
        ),
        data  = payload.get('data'),
        token = token,
      ) for token in tokens])


def cm_send(*, tokens, payload):
  return messaging.send_each(
    [messaging.Message(
                data  = payload,
                token = token, 
              ) for token in tokens])

