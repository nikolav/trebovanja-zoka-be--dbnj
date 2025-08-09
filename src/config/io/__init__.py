
# https://github.com/miguelgrinberg/flask-socketio/issues/40#issuecomment-48268526
from flask_socketio import SocketIO

from src.config import Config


initialized = False
error       = None
io          = None

def socketio_setup(app):
  global initialized
  global error
  global io

  if not initialized:  
    try:
      io = SocketIO(app, 
              cors_allowed_origins      = Config.IO_CORS_ALLOW_ORIGINS if Config.PRODUCTION else '*', 
              cors_supports_credentials = True,
          )
          
    except Exception as e:
      error = e

    else:
      io.init_app(app)
      # io status check
      @io.on('connect')
      def io_connected():
        print('@connection:io')
    
    initialized = True
  
  return error, io


