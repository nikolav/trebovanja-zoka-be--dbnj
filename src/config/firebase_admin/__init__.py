
import firebase_admin
from firebase_admin import credentials

from src.config import Config


initialized = False
cert        = None

if not initialized:

  # service account key file
  cert = credentials.Certificate(f'./{Config.CERTIFICATE_FIREBASEADMINSDK}')

  # Initialize the Firebase app
  firebase_admin.initialize_app(cert)

  initialized = True


