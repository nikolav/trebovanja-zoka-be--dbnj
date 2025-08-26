
import firebase_admin
from firebase_admin import credentials

from src.config import Config


# service account key file
cert = credentials.Certificate(f'./{Config.CERTIFICATE_FIREBASEADMINSDK}')

# Initialize the Firebase app
firebase_admin.initialize_app(cert)

