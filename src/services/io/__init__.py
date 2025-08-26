
from flask_app import io


class IO:
  _err, client = io

  @staticmethod
  def signal(sig_token):
    IO.client.emit(sig_token)

