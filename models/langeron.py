"""
This module provides the interface to easy interaction with DB.
"""

import datetime

from my_orm import BaseModel


class LangeronModel:
    """Default model of wing with longerone"""
    initialization_list = [
        'id',
        'langeron_angles',
        'langeron_wall_angles',
        'wall_length',
        'wall_angle',
        'polymer_volume_coordinate',
        'series',
        'model_name',
        'shell_angles',
        'value_vertical',
        'value_horizontal',
        'value_spectrum_modal',
        'antiflatter_value',
        'antiflatter_diam',
        'antiflatter_length',
        'creation_time'
    ]

    def __init__(self, row):
        self.series = ''
        self.shell_angles = ''
        self.data = []
        for i, el in enumerate(row):
            setattr(self, self.initialization_list[i], el)
        self.model_name = self.name_autoincrement(self.series, self.shell_angles)
        self.creation_time = datetime.datetime.now().strftime('%Y/%m/%d/%H:%M:%S')

    def __repr__(self):
        info = 'Langeron Series-{} Name-{}, Created-{}'.format(self.series, self.model_name, self.creation_time)
        return info

    @staticmethod
    def name_autoincrement(series, shell_angles):
        name = 'Series.' + series + ' Angles:' + shell_angles
        return name

    @staticmethod
    def decode_angles_to_list(value):
        list_of_angles = []
        for el in value.split(', '):
            if el != '':
                list_of_angles.append(el)
        return list_of_angles

    @staticmethod
    def encode_angles_from_list(angles_list):
        value = ''
        for el in angles_list:
            value = value + el + ', '
        value = value[:-2]
        return value

    def create_integer_code(self, field):
        angles_range = [-89.0]
        step = 180 / 64
        for i in range(1, 64):
            angles_range.append(angles_range[i - 1] + step)
        result = ''
        for angle in self.decode_angles_to_list(field):
            for i, el in enumerate(angles_range):
                if angle == el:
                    result += str(i + 11)
        if len(result) <= 8:
            return int(result)
        else:
            return int(result[0:8]), int(result[8:])

    def convert_to_bites(self):
        pass

    def read_from_bites(self):
        pass

    def update_values(self):
        data_to_update = {}
        for el in self.initialization_list:
            data_to_update[el] = getattr(self, el)
        tmp = BaseModel('langeron')
        tmp.update(new_data=data_to_update)
