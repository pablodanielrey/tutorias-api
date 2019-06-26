
class UsersModel:

    def __init__(self, users_api):
        self.users_api = users_api

    def _get_headers(self):
        tk = self.users_api.get_token()
        return self.users_api.get_auth_headers(tk)

    def obtener_usuario_por_dni(self, dni, headers=None):
        if not headers:
            headers = self._get_headers()
        return self.users_api.obtener_usuario_por_dni(headers, dni)

    def obtener_usuarios(self, uids=[], headers=None):
        if not headers:
            headers = self._get_headers()
        return self.users_api.obtener_usuarios(headers, uids)

    def obtener_usuario(self, uid, headers=None):
        if not headers:
            headers = self._get_headers()
        usrs = self.obtener_usuarios([uid], headers)
        return usrs[0]

    def buscar_usuarios(self, search=None, headers=None):
        if not search:
            return []
        if not headers:
            headers = self._get_headers()
        return self.users_api.buscar_usuarios(headers, search)


class UsersMockModel:

    usuarios = [
        {
            'id': '1f23a93e-35a8-41c6-ac24-456bcccd23bf',
            'dni': '27234567',
            'nombre': 'Usuario',
            'apellido': 'Apellido',
            'legajo': '2806/4'
        },
        {
            'id': 'de479949-a75e-4aa4-81f5-e531b5e6d435',
            'dni': '27234568',
            'nombre': 'Usuario2',
            'apellido': 'Apellido2',
            'legajo': '2806/5'
        }
    ]

    def _get_headers(self):
        return None

    def obtener_usuario_por_dni(self, dni, headers=None):
        return self.usuarios[0]

    def obtener_usuarios(self, uids=[], headers=None):
        return [u for u in self.usuarios]

    def obtener_usuario(self, uid, headers=None):
        return self.usuarios[0]

    def buscar_usuarios(self, search=None, headers=None):
        return [u for u in self.usuarios]