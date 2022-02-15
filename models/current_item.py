"""
This module provides the interface to easy interaction with DB.
"""

from my_orm import BaseModel


class CurrentItemModel:
    """Default model of wing with current item"""
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
        'creation_time',
        'shell_integer_code',
        'langeron_integer_code',
        'bytestring'
    ]

    def __init__(self, row):
        for i, el in enumerate(row):
            setattr(self, self.initialization_list[i], el)

    @staticmethod
    def name_autoincrement(series, shell_angles):
        name = 'Series.' + series + ' Angles:' + shell_angles
        return name

    def decode_angles_to_list(self, value):
        list_of_angles = []
        value = getattr(self, value)
        for el in value.split(', '):
            if el != '':
                list_of_angles.append(el)
        return list_of_angles

    def encode_angles_from_list(self, angles_list, field):
        value = ''
        for el in angles_list:
            value = value + el + ', '
        value = value[:-2]
        setattr(self, field, value)

    def get_integer_code(self, field):
        value = getattr(self, field)
        if len(value) > 8:
            return value[0:8], value[8:]
        else:
            return value

    def update_values(self):
        data_to_update = {}
        for el in self.initialization_list:
            data_to_update[el] = getattr(self, el)
        tmp = BaseModel('current_item')
        tmp.update(new_data=data_to_update)
