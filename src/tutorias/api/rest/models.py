
import os

from users.sdk.UsersApi import UsersApi
from users.sdk.UsersCache import UsersCache
from tutorias.model.TutoriasModel import TutoriasModel
from tutorias.model.UsersModel import UsersModel, UsersMockModel

VERIFY_SSL = bool(int(os.environ.get('VERIFY_SSL',0)))
OIDC_URL = os.environ['OIDC_URL']
client_id = os.environ['OIDC_CLIENT_ID']
client_secret = os.environ['OIDC_CLIENT_SECRET']
USERS_API_URL = os.environ['USERS_API_URL']
MONGO_URL = os.environ['MONGO_URL']

usersApi = UsersApi(OIDC_URL, client_id, client_secret, USERS_API_URL)
usersCacheApi = UsersCache(MONGO_URL, usersApi, timeout=60*60*24)
usersModel = UsersModel(usersCacheApi)
#usersModel = UsersMockModel()
tutoriasModel = TutoriasModel(usersModel)

