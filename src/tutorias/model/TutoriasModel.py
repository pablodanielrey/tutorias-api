
import uuid
import datetime

import pyqrcode
#from pyqrcode import QRCode

from .UsersModel import UsersModel
from .entities.Tutorias import Situacion, Tutoria, Asistencia, Coordinador

class TutoriasModel:

    def __init__(self, users_model):
        self.users_model = users_model


    def _chequear_acceso(self, session, tid, uid):
        ''' chequea si tiene acceso a los datos de la tutoría '''
        t = session.query(Tutoria).filter(Tutoria.id == tid).one()
        if t.tutor_id != uid:
            if session.queyr(Coordinador).filter(Coordinador.coordinador_id == uid, Coordinador.tutor_id == t.tutor_id).count() <= 0:
                raise Exception(f'{uid} no tiene permisos para acceder a la tutoria {tid}')
        return t

    def obtener_tutoria(self, session, tid, uid):
        t = self._chequear_acceso(session, tid, uid)
        asistencia = self.obtener_asistencia(session, tid)
        u = self.users_model.obtener_usuario(t.tutor_id)
        t.tutor = u
        t.nro_alumnos = len(asistencia)
        t.asistencia = asistencia
        return t

    def obtener_tutorias(self, session, uid):
        tutores_id = [c.tutor_id for c in session.query(Coordinador).filter(Coordinador.coordinador_id == uid).all()]
        tutores_id.append(uid)

        ts = session.query(Tutoria).filter(Tutoria.deleted == False, Tutoria.tutor_id.in_(tutores_id)).all()

        """ es mas rápido una sola llamada a la api de usuarios """
        tuids = [t.tutor_id for t in ts]
        users = self.users_model.obtener_usuarios(tuids)

        iusers = {}
        for u in users:
            iusers[u['id']] = u

        for t in ts:
            if t.tutor_id in iusers:
                t.tutor = iusers[t.tutor_id]
            t.nro_alumnos = session.query(Asistencia).filter(Asistencia.tutoria_id == t.id, Asistencia.deleted == False).count()
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

    def eliminar_tutoria(self, session, tutoria_id, uid=None):
        t = session.query(Tutoria).filter(Tutoria.id == tutoria_id).one()
        t.deleted = True
        t.deleter_id = uid

        asis = session.query(Asistencia).filter(Asistencia.tutoria_id == tutoria_id, Asistencia.deleted == False).all()
        for a in asis:
            a.deleted = True
            a.deleter_id = uid

        return tutoria_id

    def obtener_asistencia(self, session, tid):
        ts = session.query(Asistencia).filter(Asistencia.tutoria_id == tid, Asistencia.deleted == False).all()

        uids = [a.alumno_id for a in ts]
        alumnos = self.users_model.obtener_usuarios(uids)

        ''' genero un indice '''
        ialumnos = {}
        for a in alumnos:
            ialumnos[a['id']] = a

        for a in ts:
            if a.alumno_id in ialumnos:
                a.alumno = ialumnos[a.alumno_id]
        return ts


    def crear_asistencia(self, session, tutoria_id, alumno_id, situacion_id):
        a = Asistencia()
        a.id = str(uuid.uuid4())
        a.created = datetime.datetime.utcnow()
        a.alumno_id = alumno_id
        a.situacion_id = situacion_id
        a.tutoria_id = tutoria_id
        session.add(a)
        return a.id

    def eliminar_asistencia(self, session, asistencia_id, uid=None):
        a = session.query(Asistencia).filter(Asistencia.id == asistencia_id).one()
        a.deleted = True
        a.deleter_id = uid
        return a.id
        

    def obtener_situaciones(self, session):
        return session.query(Situacion).all()