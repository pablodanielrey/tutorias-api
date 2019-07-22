

if __name__ == '__main__':
    import datetime
    from tutorias.model import obtener_session
    from tutorias.model.entities.Tutorias import Tutoria, Coordinador
    import uuid
    import sys

    coordinador_id = sys.argv[1]

    with obtener_session() as session:

        coordinados = [c.tutor_id for c in session.query(Coordinador).filter(Coordinador.coordinador_id == coordinador_id).all()]
        tutores = [t.tutor_id for t in session.query(Tutoria).distinct(Tutoria.tutor_id).all()]
        agregar = list(filter(lambda t: t not in coordinados, tutores))

        for a in agregar:
            c = Coordinador()
            c.id = str(uuid.uuid4())
            c.created = datetime.datetime.utcnow()
            c.tutor_id = a
            c.coordinador_id = coordinador_id
            session.add(c)
        session.commit()
