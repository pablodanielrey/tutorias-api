
import logging
import datetime
from dateutil.parser import parse
import base64
import io

"""
    /////////////////////////
    inicializo warden para consultar los permisos
"""
import os
VERIFY_SSL = bool(int(os.environ.get('VERIFY_SSL',0)))
OIDC_URL = os.environ['OIDC_URL']

client_id = os.environ['OIDC_CLIENT_ID']
client_secret = os.environ['OIDC_CLIENT_SECRET']

from warden.sdk.warden import Warden
warden_url = os.environ['WARDEN_API_URL']
warden = Warden(OIDC_URL, warden_url, client_id, client_secret, verify=VERIFY_SSL)
"""
    //////////////////////
"""

TUTORIA_CREATE = 'urn:tutorias:tutoria:create'
TUTORIA_UPDATE = 'urn:tutorias:tutoria:update'
TUTORIA_DELETE = 'urn:tutorias:tutoria:delete'


from flask import Blueprint, request, jsonify, send_file

from tutorias.model import obtener_session
from tutorias.model.TutoriasModel import TutoriasModel

bp = Blueprint('tutorias', __name__, url_prefix='/tutorias/api/v1.0')

"""
    solo para chequear de forma intermedia los usuarios que permiten acceso a modificar
"""
def _chequear_usuarios_tutorias(uid):
    """
        por ahora chequeo los uids de los usuarios.
        89d88b81-fbc0-48fa-badb-d32854d3d93a - pablo rey
    """
    uids = [
        '89d88b81-fbc0-48fa-badb-d32854d3d93a'
    ]
    return uid in uids

@bp.route('/register', methods=['GET'])
def registrar_permisos():
    try:
        tk = ''
        datos = warden.register_system_perms(tk, 'tutorias-api', permisos=[
            TUTORIA_CREATE,
            TUTORIA_DELETE,
            TUTORIA_UPDATE
        ])
        if not datos:
            raise Exception('no se pudieron registrar los permisos')
        return jsonify({'status':200, 'data':datos})

    except Exception as e:
        return jsonify({'status':500, 'response': str(e)})    

@bp.route('/tutorias', methods=['GET'])
def obtener_tipos_de_normativas():
    (token,tkdata) = warden._require_valid_token()
    """
        !!!! TODO: esto se debe activar ni bien esté operativa la nueva version de warden

    if not warden.has_permissions(token, permisos=[NORMAS_CREATE]):
        return ('No tiene permisos para realizar esta acción', 403)
    """
    uid = tkdata['sub']
    if not _chequear_usuarios_tutorias(uid):
        return ('No tiene permisos para realizar esta acción', 403)

    try:
        with obtener_session() as session:
            tutorias = TutoriasModel.obtener_tutorias(session)
            resultado = [
                {
                    'id': t.id
                }
                for t in tutorias
            ]
            return jsonify({'status':200,'tutorias':resultado})

    except Exception as e:
        return jsonify({'status':500, 'response': str(e)})
