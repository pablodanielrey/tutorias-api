
import logging
import datetime
from dateutil.parser import parse
import base64
import io
import json
import re


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

import pyqrcode
URL_FOR_QR = os.environ['URL_FOR_QR']

def _generar_qr_para_tutoria(tid):
    texto = f"{URL_FOR_QR}/{tid}"
    qr = pyqrcode.create(texto).png_as_base64_str(scale=3)
    return qr


from tutorias.model import obtener_session
from tutorias.api.rest.models import tutoriasModel

from flask import Blueprint, request, jsonify, send_file


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


@bp.route('/situaciones', methods=['GET'])
def obtener_situaciones():
    #(token,tkdata) = warden._require_valid_token()
    """
        !!!! TODO: esto se debe activar ni bien esté operativa la nueva version de warden

    if not warden.has_permissions(token, permisos=[NORMAS_CREATE]):
        return ('No tiene permisos para realizar esta acción', 403)
    """
    #uid = tkdata['sub']
    #if not _chequear_usuarios_tutorias(uid):
    #    return ('No tiene permisos para realizar esta acción', 403)

    try:
        with obtener_session() as session:
            situaciones = tutoriasModel.obtener_situaciones(session)
            resultado = [
                {
                    'id': t.id,
                    'situacion': t.situacion
                }
                for t in situaciones
            ]
            return jsonify({'status':200, 'response':resultado})

    except Exception as e:
        return jsonify({'status':500, 'response': str(e)})



@bp.route('/tutorias', methods=['GET'])
def obtener_tutorias():
    #(token,tkdata) = warden._require_valid_token()
    """
        !!!! TODO: esto se debe activar ni bien esté operativa la nueva version de warden

    if not warden.has_permissions(token, permisos=[NORMAS_CREATE]):
        return ('No tiene permisos para realizar esta acción', 403)
    """
    #uid = tkdata['sub']
    #if not _chequear_usuarios_tutorias(uid):
    #    return ('No tiene permisos para realizar esta acción', 403)

    params = request.json

    try:
        with obtener_session() as session:
            tutorias = tutoriasModel.obtener_tutorias(session)
            resultado = [
                {
                    'id': t.id,
                    'fecha': t.fecha,
                    'materia': t.materia,
                    'comision': t.comision,
                    'aula': t.aula,
                    'tutor': t.tutor,
                    'nro_alumnos': t.nro_alumnos,
                    'asistencia': None
                }
                for t in tutorias
            ]
            return jsonify({'status':200, 'response':resultado})

    except Exception as e:
        return jsonify({'status':500, 'response': str(e)})


@bp.route('/tutorias', methods=['POST'])
def crear_tutoria():
    (token,tkdata) = warden._require_valid_token()
    if not tkdata:
        return (401, 'Token expirado')

    """
        !!!! TODO: esto se debe activar ni bien esté operativa la nueva version de warden

    if not warden.has_permissions(token, permisos=[NORMAS_CREATE]):
        return ('No tiene permisos para realizar esta acción', 403)
    """
    #uid = tkdata['sub']
    #if not _chequear_usuarios_tutorias(uid):
    #    return ('No tiene permisos para realizar esta acción', 403)

    try:
        tutoria = request.json

        assert 'fecha' in tutoria
        assert 'hora_inicio' in tutoria
        assert 'materia' in tutoria
        assert 'comision' in tutoria
        assert 'aula' in tutoria

        tutoria['tutor_id'] = tkdata['sub']

        fecha = parse(tutoria['fecha'])
        tutoria['fecha'] = fecha

        ''' parseo la hora de inicio como segundos a partir de las 00 '''
        rhora = re.compile(r'(\d\d):(\d\d)')
        matchs = rhora.match(tutoria['hora_inicio'])
        if not matchs:
            raise Exception(f"formato incorrecto en la hora {tutoria['hora_inicio']}")
        _hora = matchs.group(1)
        _minutos = matchs.group(2)
        hora = int(_hora) * 60 * 60 + int(_minutos) * 60
        tutoria['hora_inicio'] = hora

        with obtener_session() as session:
            tid = tutoriasModel.crear_tutoria(session, tutoria)
            session.commit()
            return jsonify({'status':200, 'response':tid})

    except Exception as e:
        return jsonify({'status':500, 'response': str(e)})


@bp.route('/tutoria/<tid>', methods=['GET'])
def obtener_tutoria(tid):
    #(token,tkdata) = warden._require_valid_token()
    """
        !!!! TODO: esto se debe activar ni bien esté operativa la nueva version de warden

    if not warden.has_permissions(token, permisos=[NORMAS_CREATE]):
        return ('No tiene permisos para realizar esta acción', 403)
    """
    #uid = tkdata['sub']
    #if not _chequear_usuarios_tutorias(uid):
    #    return ('No tiene permisos para realizar esta acción', 403)

    assert tid is not None

    try:
        with obtener_session() as session:
            t = tutoriasModel.obtener_tutoria(session, tid)
            resultado = {
                'id': t.id,
                'fecha': t.fecha,
                'materia': t.materia,
                'comision': t.comision,
                'aula': t.aula,
                'tutor': t.tutor,
                'nro_alumnos': t.nro_alumnos,
                'asistencia': [ 
                    {
                        'id': a.id,
                        'alumno': a.alumno,
                        'situacion': a.situacion.situacion
                    } 
                    for a in t.asistencia
                ],
                'qr': _generar_qr_para_tutoria(tid)
            }
            return jsonify({'status':200, 'response':resultado})

    except Exception as e:
        return jsonify({'status':500, 'response': str(e)})


@bp.route('/asistencias/<tid>', methods=['GET'])
def obtener_asistencia_a_tutoria(tid):
    #(token,tkdata) = warden._require_valid_token()
    """
        !!!! TODO: esto se debe activar ni bien esté operativa la nueva version de warden

    if not warden.has_permissions(token, permisos=[NORMAS_CREATE]):
        return ('No tiene permisos para realizar esta acción', 403)
    """
    #uid = tkdata['sub']
    #if not _chequear_usuarios_tutorias(uid):
    #    return ('No tiene permisos para realizar esta acción', 403)

    assert tid is not None

    try:
        with obtener_session() as session:
            asistencias = tutoriasModel.obtener_asistencia(session, tid)
            resultado = [
                {
                    'id': a.id, 
                    'alumno': a.alumno, 
                    'situacion': a.situacion.situacion
                } 
                for a in asistencias
            ]
            return jsonify({'status':200, 'response':resultado})

    except Exception as e:
        return jsonify({'status':500, 'response': str(e)})


@bp.route('/qrcode/<tid>', methods=['GET'])
def obtener_qrcode(tid):
    #(token,tkdata) = warden._require_valid_token()
    """
        !!!! TODO: esto se debe activar ni bien esté operativa la nueva version de warden

    if not warden.has_permissions(token, permisos=[NORMAS_CREATE]):
        return ('No tiene permisos para realizar esta acción', 403)
    """
    #uid = tkdata['sub']
    #if not _chequear_usuarios_tutorias(uid):
    #    return ('No tiene permisos para realizar esta acción', 403)

    """ obtengo en que formato se quiere el qr """  
    mime_type = request.headers.get('content-type')
    if not mime_type:
        mime_type = 'text/html'

    qr = _generar_qr_para_tutoria(tid)

    if 'text/html' in mime_type:
        datauri = f"<img src='data:image/png;base64,{qr}'>"
        return (datauri, 200)

    if 'image/png' in mime_type:
        bs = base64.b64decode(qr.encode())
        return send_file(io.BytesIO(bs), attachment_filename=f'{tid}.png', mimetype='image/png')

    if 'application/json' in mime_type:
        data = {
            'qr': qr,
            'encoding': 'base64',
            'tutoria_id': tid,
            'date': str(datetime.datetime.utcnow())
        }
        return (json.dumps(data), 200)

    return ('Malformed', 401)

    """
    assert qid is not None
    try:

        return jsonify({'status':200, 'response':resultado})

    except Exception as e:
        return jsonify({'status':500, 'response': str(e)})
    """