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
12) antiflatter_x : real
13) antiflatter_y : real
14) antiflatter_diam : real
15) antiflatter_length : real
15) wall_length : real
16) wall_angle : real
"""

from sqlalchemy import Column, String, Integer

from models.shell import ShellModel


class LangeronModel(ShellModel):
    """Default model of wing with longerone"""
    __tablename__ = 'Langeron'

    langeron_angles = Column('langeron_angles', String)
    langeron_wall_angles = Column('langeron_wall_angles', String)
    wall_length = Column('wall_length', String)
    wall_angle = Column('wall_angle', String)
    polymer_volume_coordinate = Column('polymer_volume_coordinate', Integer)
