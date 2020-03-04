
import os

from tutorias.model.TutoriasModel import TutoriasModel

VERIFY_SSL = bool(int(os.environ.get('VERIFY_SSL',1)))
OIDC_URL = os.environ['OIDC_URL']
client_id = os.environ['OIDC_CLIENT_ID']
client_secret = os.environ['OIDC_CLIENT_SECRET']
USERS_API_URL = os.environ['USERS_API_URL']
MONGO_URL = os.environ['MONGO_URL']

tutoriasModel = TutoriasModel()

