
import logging
import os
import json
import uuid
import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Date, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from tutorias.model.entities import Base

    

class Tutoria(Base):
    __tablename__ = 'tutorias'

    id = Column(String(), primary_key=True, default=None)
    created = Column(DateTime())
    modified = Column(DateTime())

    materia = Column(String())
    comision = Column(String())
    aula = Column(String())

    fecha = Column(DateTime())
    tutor_id = Column(String())


class Situacion(Base):
    __tablename__ = 'situaciones'

    id = Column(String(), primary_key=True, default=None)
    created = Column(DateTime())

    situacion = Column(String())


class Asistencia(Base):
    __tablename__ = 'asistencia'

    id = Column(String(), primary_key=True, default=None)
    created = Column(DateTime())
    modified = Column(DateTime())

    alumno_id = Column(String())

    situacion_id = Column(String(), ForeignKey('situaciones.id'))
    situacion = relationship('Situacion')

    tutoria_id = Column(String(), ForeignKey('tutorias.id'))
    tutoria = relationship('Tutoria')
