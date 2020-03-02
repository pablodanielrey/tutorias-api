
import os

from tutorias.model.API import API
from tutorias.model.UsersAPI import UsersAPI
#from tutorias.model.UserCache import UserCache
from tutorias.model.TutoriasModel import TutoriasModel
from tutorias.model.UsersModel import UsersModel, UsersMockModel

VERIFY_SSL = bool(int(os.environ.get('VERIFY_SSL',1)))
OIDC_URL = os.environ['OIDC_URL']
client_id = os.environ['OIDC_CLIENT_ID']
client_secret = os.environ['OIDC_CLIENT_SECRET']
USERS_API_URL = os.environ['USERS_API_URL']
MONGO_URL = os.environ['MONGO_URL']

_API = API(url=OIDC_URL, 
              client_id=client_id, 
              client_secret=client_secret, 
              verify_ssl=VERIFY_SSL)

usersApi = UsersAPI(USERS_API_URL, _API)
#usersCacheApi = UserCache(MONGO_URL, usersApi, timeout=60*60*24)
usersModel = UsersModel(usersApi)
#usersModel = UsersMockModel()
tutoriasModel = TutoriasModel(usersModel)

