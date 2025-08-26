
if __name__ == '__main__':    
  # import os
  from flask_app  import app
  from flask_app  import io
  from src.config import Config
  
  err_, ioclient = io
  _port = Config.PORT

  ioclient.run(app, 
    debug = True,
    host  = '0.0.0.0',
    port  = _port if None != _port else 5000,
    allow_unsafe_werkzeug = True,
  )
  

# if __name__ == '__main__':    
#   from flask_app import app
#   from src.config import Config
  
#   _port = Config.PORT

#   app.run(
#     debug = True,
#     host  = '0.0.0.0',
#     port  = _port if None != _port else 5000,
#   )

