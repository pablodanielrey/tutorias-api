
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
        for t in ts:
            u = self.users_model.obtener_usuario(t.tutor_id)
            t.tutor = u
            t.nro_alumnos = session.query(Asistencia).filter(Asistencia.tutoria_id == t.id).count()
        return ts

    def obtener_asistencia(self, session, tid):
        ts = session.query(Asistencia).filter(Asistencia.tutoria_id == tid).all()
        for a in ts:
            u = self.users_model.obtener_usuario(a.alumno_id)
            a.alumno = u
        return ts

    def obtener_situaciones(self, session):
        return session.query(Situacion).all()