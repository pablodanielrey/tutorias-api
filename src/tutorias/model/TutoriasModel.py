
from .UsersModel import UsersModel
from .entities.Tutorias import Situacion, Tutoria, Asistencia

class TutoriasModel:

    @classmethod
    def obtener_tutoria(cls, session, tid):
        asistencia = cls.obtener_asistencia(session, tid)
        t = session.query(Tutoria).filter(Tutoria.id == tid).one()
        u = UsersModel.obtener_usuario(t.tutor_id)
        t.tutor = u
        t.nro_alumnos = len(asistencia)
        t.asistencia = asistencia
        return t

    @classmethod
    def obtener_tutorias(cls, session):
        ts = session.query(Tutoria).limit(10).all()
        for t in ts:
            u = UsersModel.obtener_usuario(t.tutor_id)
            t.tutor = u
            t.nro_alumnos = session.query(Asistencia).filter(Asistencia.tutoria_id == t.id).count()
        return ts

    @classmethod
    def obtener_asistencia(cls, session, tid):
        ts = session.query(Asistencia).filter(Asistencia.tutoria_id == tid).all()
        for a in ts:
            u = UsersModel.obtener_usuario(a.alumno_id)
            a.alumno = u
        return ts

    @classmethod
    def obtener_situaciones(cls, session):
        return session.query(Situacion).all()