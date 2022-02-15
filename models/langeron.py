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
        self.langeron_angles = ''
        self.data = []
        for i, el in enumerate(row):
            setattr(self, self.initialization_list[i], el)
        self.model_name = self.name_autoincrement(self.series, self.shell_angles)
        self.creation_time = datetime.datetime.now().strftime('%Y/%m/%d/%H:%M:%S')
        self.bytestring = ''
        self.shell_integer_code = self.create_integer_code('shell_angles')
        self.langeron_integer_code = self.create_integer_code('langeron_angles')
        self._convert_to_bites()

    def __repr__(self):
        info = 'Langeron Series-{} Name-{}, Created-{}'.format(self.series, self.model_name, self.creation_time)
        return info

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

    def create_integer_code(self, field):
        """
        Takes class field name, returns integer code in string, if there is up to 4 elements in field.
        This need to set the parameters in acp_pre.
        """
        angles_range = [-89.0]
        step = 180 / 64
        for i in range(1, 64):
            angles_range.append(angles_range[i - 1] + step)
        result = ''
        for angle in getattr(self, field).split(', '):
            for i, el in enumerate(angles_range):
                if float(angle) == el:
                    result += str(i + 11)
        return result

    def get_integer_code(self, field):
        value = getattr(self, field)
        if len(value) > 8:
            return value[0:8], value[8:]
        else:
            return value

    def _convert_to_bites(self):
        """
        Set the bytestring form of the class to interact with genetic algorithm.
        """
        length_dict = {
            300: 3,
            400: 4,
            500: 5,
            600: 6,
            700: 7,
            800: 8
        }
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
        argument = getattr(self, 'langeron_angles')
        self.bytestring += format(len(argument), '03b')
        argument = []
        for i in range(len(self.langeron_integer_code), 2):
            tmp = int(self.shell_integer_code[i: i + 2])
            argument.append(tmp)
        for el in argument:
            self.bytestring += format(el, '06b')
        self.bytestring += format(getattr(self, 'wall_length'), '05b')
        self.bytestring += format(getattr(self, 'wall_angle'), '06b')

    def read_from_bites(self):
        pass

    def update_values(self):
        data_to_update = {}
        for el in self.initialization_list:
            data_to_update[el] = getattr(self, el)
        tmp = BaseModel('langeron')
        tmp.update(new_data=data_to_update)
