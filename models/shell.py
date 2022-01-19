"""
This module provides the interface to easy interaction with DB.
Model for all DB:
1) ID : int
2) model_name : text
3) shell_angles : json (text)
4) langeron_angles : json (text)
5) langeron_wall_angles : json(text)
6) value_vertical : real
7) value_horizontal : real
8) value_neutral : real
9) value_spectrum_tang : json (text)
10) value_spectrum_attack : json (text)
11) value_spectrum_roll : json (text)
12) antiflatter_value : integer
13) antiflatter_diam : real
14) antiflatter_length : real
15) wall_length : real
16) wall_angle : real
17) creation_time: datetime
"""

from sqlalchemy import Column, Integer, String, Float, DateTime

from models.database import Base

import datetime


class ShellModel(Base):
    """Default model of wing without longerone"""
    __tablename__ = 'Shell'

    id = Column(Integer, primary_key=True, autoincrement=True)
    series = Column('series', String)
    model_name = Column('model_name', String)
    shell_angles = Column('shell_angles', String)
    value_vertical = Column('value_vertical', Float)
    value_horizontal = Column('value_horizontal', Float)
    value_neutral = Column('value_neutral', Float)
    value_spectrum_tang = Column('value_spectrum_tang', Float)
    value_spectrum_attack = Column('value_spectrum_attack', Float)
    value_spectrum_roll = Column('value_spectrum_roll', Float)
    antiflatter_value = Column('antiflatter_value', Integer)
    antiflatter_diam = Column('antiflatter_diam', Float)
    antiflatter_length = Column('antiflatter_length', Float)
    creation_time = Column('creation_time', DateTime)

    def __init__(self, series: str, shell_angles: list, antiflatter_value: int, antiflatter_diam: float,
                 antiflatter_length: float):
        self.series = series
        self.shell_angles = self.encode_angles_from_list(shell_angles)
        self.model_name = self.name_autoincrement(series, shell_angles)
        self.antiflatter_value = antiflatter_value
        self.antiflatter_diam = antiflatter_diam
        self.antiflatter_length = antiflatter_length
        self.creation_time = datetime.datetime.now()

    def __repr__(self):
        info: str = f'Оболочка [Серия - {self.series} Имя - {self.model_name}]'
        return info

    @staticmethod
    def name_autoincrement(series, shell_angles):
        angles_string = ''
        for el in shell_angles:
            angles_string = angles_string + ', ' + el
        name = 'Series.' + series + ' Angles:' + angles_string
        return name

    @staticmethod
    def decode_angles_to_list(value):
        list_of_angles = []
        for el in value.split('\n'):
            if el != '':
                list_of_angles.append(el)
        return list_of_angles

    @staticmethod
    def encode_angles_from_list(angles_list):
        value = ''
        for el in angles_list:
            value = value + el + '\n'
        return value
