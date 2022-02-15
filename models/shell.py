"""
This module provides the interface to easy interaction with DB.
"""

import datetime

from my_orm import BaseModel


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
        self.data = []
        for i, el in enumerate(row):
            setattr(self, self.initialization_list[i], el)
        self.model_name = self.name_autoincrement(self.series, self.shell_angles)
        self.creation_time = datetime.datetime.now().strftime('%Y/%m/%d/%H:%M:%S')
        self.bytestring = ''
        self.shell_integer_code = self.create_integer_code('shell_angles')
        self._convert_to_bites()

    def __repr__(self):
        info = '[Shell Series-{} Name-{}, Created-{}]'.format(self.series, self.model_name, self.creation_time)
        return info

    @staticmethod
    def name_autoincrement(series, shell_angles):
        name = 'Series.' + series + ' Angles:' + shell_angles
        return name

    def decode_angles_to_list(self):
        list_of_angles = []
        value = self.shell_angles
        for el in value.split(', '):
            if el != '':
                list_of_angles.append(el)
        return list_of_angles

    def encode_angles_from_list(self, angles_list):
        value = ''
        for el in angles_list:
            value = value + el + ', '
        value = value[:-2]
        self.shell_angles = value

    def get_integer_code(self, field):
        value = getattr(self, field)
        if len(value) > 8:
            return value[0:8], value[8:]
        else:
            return value

    def _convert_to_bites(self):
        length_dict = {
            300: 3,
            400: 4,
            500: 5,
            600: 6,
            700: 7,
            800: 8
        }
        self.bytestring = ''
        argument = len(self.shell_angles)
        self.bytestring += format(argument, '03b')
        argument = []
        for i in range(len(self.shell_integer_code), 2):
            tmp = int(self.shell_integer_code[i: i + 2]) - 11
            argument.append(tmp)
        for el in argument:
            self.bytestring += format(el, '06b')
        self.bytestring += format(getattr(self, 'antiflatter_diam'), '02b')
        argument = length_dict[getattr(self, 'antiflatter_length')]
        self.bytestring += format(argument, '03b')
        self.bytestring += format(getattr(self, 'antiflatter_value'), '03b')

    def read_new_values_from_bitecode(self):
        pass

    def create_integer_code(self, field):
        angles_range = [-89.0]
        step = 180 / 64
        for i in range(1, 64):
            angles_range.append(angles_range[i - 1] + step)
        result = ''
        for angle in getattr(self, field).split(', '):
            for i, el in enumerate(angles_range):
                if float(angle) == el:
                    result += str(i + 11)
        if len(result) <= 8:
            return result
        else:
            return result[0:8], result[8:]

    def update_values(self):
        data_to_update = {}
        for el in self.initialization_list:
            data_to_update[el] = getattr(self, el)
        tmp = BaseModel('shell')
        tmp.update(new_data=data_to_update)
