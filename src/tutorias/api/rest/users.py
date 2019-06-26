
import logging
import datetime
from dateutil.parser import parse
import base64
import io

from flask import Blueprint, request, jsonify, send_file

from tutorias.api.rest.models import usersModel

bp = Blueprint('users', __name__, url_prefix='/tutorias/api/v1.0')

@bp.route('/usuarios/<list:uids>', methods=['GET'])
def obtener_usuarios_por_uids(uids=[]):
    try:
        usuarios = usersModel.obtener_usuarios(uids)
        return jsonify({'status': 200, 'response': usuarios})

    except Exception as e:
        return jsonify({'status': 500, 'response':str(e)})


@bp.route('/usuarios', methods=['GET'])
def obtener_usuarios_por_search():
    try:
        search = request.args.get('q', None)
        usuarios = usersModel.buscar_usuarios(search)
        return jsonify({'status': 200, 'response': usuarios})

    except Exception as e:
        return jsonify({'status': 500, 'response':str(e)})    
    
    