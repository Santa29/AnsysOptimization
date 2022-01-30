"""
This module provides the interface to easy interaction with DB.
"""

import datetime


class LangeronModel:
    """Default model of wing with longerone"""

    def __init__(self, **kwargs):
        self.series = kwargs['series']
        self.shell_angles = self.encode_angles_from_list(kwargs['shell_angles'])
        self.model_name = self.name_autoincrement(kwargs['series'], kwargs['shell_angles'])
        self.antiflatter_value = kwargs['antiflatter_value']
        self.antiflatter_diam = kwargs['antiflatter_diam']
        self.antiflatter_length = kwargs['antiflatter_length']
        self.creation_time = datetime.datetime.now()
        self.langeron_angles = self.encode_angles_from_list(kwargs['langeron_angles'])
        self.langeron_wall_angles = self.encode_angles_from_list(kwargs['langeron_wall_angles'])
        self.wall_length = kwargs['wall_length']
        self.wall_angle = kwargs['wall_angle']
        self.polymer_volume_coordinate = kwargs['polymer_volume_coordinate']
        self.value_vertical = 0.0
        self.value_horizontal = 0.0
        self.value_spectrum = []

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
