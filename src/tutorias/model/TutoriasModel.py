
import uuid
import datetime

import pyqrcode
#from pyqrcode import QRCode

from .UsersModel import UsersModel
from .entities.Tutorias import Situacion, Tutoria, Asistencia

class TutoriasModel:

    def __init__(self, users_model):
        self.users_model = users_model

    def obtener_tutoria(self, session, tid):
        asistencia = self.obtener_asistencia(session, tid)
        t = session.query(Tutoria).filter(Tutoria.id == tid).one()
        u = self.users_model.obtener_usuario(t.tutor_id)
        t.tutor = u
        t.nro_alumnos = len(asistencia)
        t.asistencia = asistencia
        return t

    def obtener_tutorias(self, session):
        ts = session.query(Tutoria).all()
        
        """ es mas rápido una sola llamada a la api de usuarios """
        tuids = [t.tutor_id for t in ts]
        """ separo la lista en listas de a 10 elementos para que no se haga tan largo el get """
        tamano = 20
        sub_tuids = [tuids[i:i+tamano] for i in range(0,len(tuids),tamano)]
        headers = self.users_model._get_headers()
        users = []
        for tids in sub_tuids:
            users.extend(self.users_model.obtener_usuarios(tids, headers))

        for t in ts:
            #u = self.users_model.obtener_usuario(t.tutor_id)
            for u in users:
                if t.tutor_id in u['id']:
                    t.tutor = u
            #t.tutor = u
            t.nro_alumnos = session.query(Asistencia).filter(Asistencia.tutoria_id == t.id).count()
        return ts

    def crear_tutoria(self, session, tutoria):
        fecha = tutoria['fecha']
        tutor = tutoria['tutor_id']
        materia = tutoria['materia']
        comision = tutoria['comision']
        aula = tutoria['aula']

        t = session.query(Tutoria).filter(Tutoria.tutor_id == tutor, Tutoria.fecha == fecha).one_or_none()
        if t:
            return t.id

        tid = str(uuid.uuid4())
        t = Tutoria()
        t.id = tid
        t.created = datetime.datetime.utcnow()
        t.fecha = fecha
        t.tutor_id = tutor
        t.materia = materia
        t.comision = comision
        t.aula = aula
        session.add(t)

        return tid



    def obtener_asistencia(self, session, tid):
        ts = session.query(Asistencia).filter(Asistencia.tutoria_id == tid).all()
        for a in ts:
            u = self.users_model.obtener_usuario(a.alumno_id)
            a.alumno = u
        return ts

    def obtener_situaciones(self, session):
        return session.query(Situacion).all()