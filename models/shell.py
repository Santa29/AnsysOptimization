"""
This module provides the interface to easy interaction with DB.
"""

import datetime

from models.my_orm import ShellTable


class ShellModel:
    """Default model of wing with longerone"""
    initialization_list = [
        'id',
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
        for i, el in enumerate(row):
            setattr(self, self.initialization_list[i], el)
        self.model_name = self.name_autoincrement(self.series, self.shell_angles)
        self.creation_time = datetime.datetime.now().strftime('%Y/%m/%d/%H:%M:%S')

    def __repr__(self):
        info: str = f'Оболочка [Оболочка Серия - {self.series} Имя - {self.model_name}, Создан - {self.creation_time}]'
        return info

    @staticmethod
    def name_autoincrement(series, shell_angles):
        name = 'Series.' + series + ' Angles:' + shell_angles
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

    def convert_to_bites(self):
        pass

    def read_from_bites(self):
        pass

    def update_values(self):
        data_to_update = {}
        for el in self.initialization_list:
            data_to_update[el] = getattr(self, el)
        ShellTable.objects.update(data_to_update)