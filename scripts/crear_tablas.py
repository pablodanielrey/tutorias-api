

if __name__ == '__main__':
    import datetime
    from tutorias.model.entities import crear_tablas
    crear_tablas()

    from tutorias.model import obtener_session
    from tutorias.model.entities.Tutorias import Tutoria, Situacion, Asistencia
    import uuid

    with obtener_session() as session:

        situaciones = [ 
            {
                'id':'e97e3aa8-2c8a-4f2d-8fad-bb2ca1d5d764',
                'situacion':'Situación económica'
            },
            {
                'id':'a89df5d8-9b0e-4616-969d-8d8e1a7853b7',
                'situacion':'Situación personal'
            },
            {
                'id':'8fcc979f-118f-481a-bc68-ed5ed5a39146',
                'situacion':'Situación académica'
            }
        ]

        for t in situaciones:
            if session.query(Situacion).filter(Situacion.situacion == t['id']).count() <= 0:
                tn = Situacion()
                tn.id = t['id']
                tn.created = datetime.datetime.utcnow()
                tn.situacion = t['situacion']
                session.add(tn)
                session.commit()

