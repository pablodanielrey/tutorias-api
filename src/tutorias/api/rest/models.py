
import os

from users.sdk.UsersApi import UsersApi
from tutorias.model.TutoriasModel import TutoriasModel
from tutorias.model.UsersModel import UsersModel, UsersMockModel

VERIFY_SSL = bool(int(os.environ.get('VERIFY_SSL',0)))
OIDC_URL = os.environ['OIDC_URL']
client_id = os.environ['OIDC_CLIENT_ID']
client_secret = os.environ['OIDC_CLIENT_SECRET']
USERS_API_URL = os.environ['USERS_API_URL']

usersApi = UsersApi(OIDC_URL, client_id, client_secret, USERS_API_URL)
#usersModel = UsersModel(usersApi)
usersModel = UsersMockModel()
tutoriasModel = TutoriasModel(usersModel)

