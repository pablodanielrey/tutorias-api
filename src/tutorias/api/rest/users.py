
import logging
import datetime
from dateutil.parser import parse
import base64
import io

from flask import Blueprint, request, jsonify, send_file

from users.model.UsersModel import UsersModel
from users.model import open_session

from tutorias.model.Utils import map_user_from_model

bp = Blueprint('users', __name__, url_prefix='/tutorias/api/v1.0')

@bp.route('/usuarios/<list:uids>', methods=['GET'])
def obtener_usuarios_por_uids(uids=[]):
    try:
        with open_session() as s:
            usuarios = UsersModel.get_users(s, uids)
            musers = [map_user_from_model(u) for u in usuarios]
        return jsonify({'status': 200, 'response': musers})

    except Exception as e:
        return jsonify({'status': 500, 'response':str(e)})


@bp.route('/usuarios', methods=['GET'])
def obtener_usuarios_por_search():
    try:
        search = request.args.get('q', None)
        with open_session() as s:
            uids = UsersModel.search_user(s, search) 
            usuarios = UsersModel.get_users(s, uids)
            musers = [map_user_from_model(u) for u in usuarios]
        return jsonify({'status': 200, 'response': musers})

    except Exception as e:
        return jsonify({'status': 500, 'response':str(e)})    
    
    