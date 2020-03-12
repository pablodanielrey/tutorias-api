import sys
import json
import uuid
import datetime

from users.model import open_session as open_user_session
from users.model.UsersModel import UsersModel

from tutorias.model import obtener_session as open_tutorias_session
from tutorias.model.entities.Tutorias import Coordinador


if __name__ == '__main__':
    archivo = sys.argv[1]
    with open(archivo, 'r') as f:
        fs = f.readlines()

    catedras = {}
    for l in fs:
        catedra, nombre, dni, cargo = l.split(";")
        print(catedra)
        print(dni)
        print(cargo)

        if catedra not in catedras:
            catedras[catedra] = {'tutores':[], 'coordinadores':[]}

        if 'TUTOR' in cargo:
            catedras[catedra]['tutores'].append(dni)
        if 'COORDINADOR' in cargo:
            catedras[catedra]['coordinadores'].append(dni)

    usersModel = UsersModel

    with open_tutorias_session() as stutorias:
        with open_user_session() as susers:
            for c in catedras:
                for coordinador in catedras[c]['coordinadores']:
                    cuid = usersModel.get_uid_person_number(susers, coordinador)
                    assert cuid is not None

                    for tutor in catedras[c]['tutores']:
                        tuid = usersModel.get_uid_person_number(susers, tutor)
                        assert tuid is not None

                        if stutorias.query(Coordinador).filter(Coordinador.coordinador_id == cuid, Coordinador.tutor_id == tuid).count() > 0:
                            print(f'{coordinador};{tutor};ya existe')
                            continue

                        coord = Coordinador()
                        coord.id = str(uuid.uuid4())
                        coord.created = datetime.datetime.utcnow()
                        coord.tutor_id = tuid
                        coord.coordinador_id = cuid
                        stutorias.add(coord)
                        stutorias.commit()

                        print(f'{coordinador};{tutor};agregado')