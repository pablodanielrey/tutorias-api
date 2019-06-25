
import os
import psycopg2
import logging
logging.getLogger().setLevel(logging.INFO)

user = os.environ['OLD_DB_USER']
passw = os.environ['OLD_DB_PASSWORD']
host = os.environ['OLD_DB_HOST']
port = os.environ['OLD_DB_PORT']
db = os.environ['OLD_DB']

tutorias = {}

con = psycopg2.connect(f"dbname='{db}' user='{user}' password='{passw}' host='{host}' port='{port}'")
try:
    cur = con.cursor()
    try:
        cur.execute('select t.id, t.date, t.created, u.dni as tutor from tutoring.tutorings t inner join profile.users u on (t.tutor_id = u.id)')
        for t in cur:
            tid = t[0]
            tutorias[tid] = {
                'id': tid,
                'fecha': t[1],
                'creada': t[2],
                'tutor_dni': t[3],
                'alumnos': []
            }

        cur.execute('select s.tutoring_id, u.dni, s.situation from tutoring.situations s inner join profile.users u on (u.id = s.user_id)')
        for a in cur:
            tid = a[0]
            tutorias[tid]['alumnos'].append({
                'alumno_dni': a[1],
                'situacion': a[2]
            })

    finally:
        cur.close()

finally:
    con.close()


"""
    comienza la parte de ejecución sobre los sistemas actuales
"""

import requests

oidc_url = os.environ['OIDC_URL']
client_id = os.environ['OIDC_CLIENT_ID']
client_secret = os.environ['OIDC_CLIENT_SECRET']
verify = False
users_api_url = os.environ['USERS_API_URL']

from oidc.oidc import ClientCredentialsGrant
cc = ClientCredentialsGrant(oidc_url, client_id, client_secret, verify)

def _get_token(cc):
    r = cc.access_token()
    tk = cc.get_token(r)
    return tk

def _get_auth_headers(tk):
    headers = {
        'Authorization': 'Bearer {}'.format(tk),
        'Accept':'application/json'
    }
    return headers

def obtener_usuario_por_dni(headers, dni):
    r = requests.get(users_api_url + f'/usuario_por_dni/{dni}', verify=verify, allow_redirects=False, headers=headers)
    return r.json()

tk = _get_token(cc)
headers = _get_auth_headers(tk)

"""
    obtengo los ids para los tutores y los alumnos
    de paso los cacheo para no preguntarlos nuevamente
"""
import json
with open('errores.log','w') as f:
    usuarios = {}

    for tid in tutorias:
        try:
            tutoria = tutorias[tid]

            dni = tutoria['tutor_dni']
            uid = None
            if dni not in usuarios:
                usr = obtener_usuario_por_dni(headers, dni)
                uid = usr['id']
                usuarios[dni] = uid
            uid = usuarios[dni]
            tutoria['tutor_id'] = uid

            for alumno in tutoria['alumnos']:
                try:
                    dni = alumno['alumno_dni']
                    if dni not in usuarios:
                        usr = obtener_usuario_por_dni(headers, dni)
                        uid = usr['id']
                        usuarios[dni] = uid
                    uid = usuarios[dni]
                    alumno['id'] = uid

                except Exception as e2:
                    f.write('error agregando alumno :')
                    f.write(json.dumps(alumno))
                    logging.exception(e2)

        except Exception as e:
            f.write('error agregando tutoria:')
            f.write(json.dumps(tutoria))
            logging.exception(e)

import uuid
from tutorias.model import obtener_session
from tutorias.model.entities import Tutoria, Situacion, Asistencia

with obtener_session() as session:

    situaciones = {}
    for s in session.query(Situacion).all():
        situaciones[s.situacion] = s.id

    for tid in tutorias:
        try:
            logging.info(f'Agregando tutoria {tid}')
            tutoria = tutorias[tid]
            if 'tutor_dni' not in tutoria:
                continue

            if session.query(Tutoria).filter(Tutoria.id == tid).count() <= 0:
                t = Tutoria()
                t.id = tid
                t.ceated = datetime.datetime.utcnow()
                t.fecha = tutoria['fecha']
                t.tutor_id = tutoria['tutor_id']
                session.add(t)

            for alumno in tutoria['alumnos']:
                if 'id' not in alumno:
                    continue

                aid = alumno['id']
                if session.query(Asistencia).filter(Asistencia.alumno_id == aid, Asistencia.tutoria_id == tid).count() <= 0:
                    a = Asistencia()
                    a.alumno_id = aid
                    a.tutoria_id = tid
                    a.created = datetime.datetime.utcnow()
                    a.id = str(uuid.uuid4())
                    a.situacion_id = situaciones[alumno['situacion']]
                    session.add(a)

            logging.info(f'Agregado tutoria {tid}')
            session.commit()
            
        except Exception as e:
            logging.exception(e)