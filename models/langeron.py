"""
This module provides the interface to easy interaction with DB.
"""

import datetime

from .my_orm import BaseModel


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
        'bytestring',
        'creation_time',
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
        self.shell_integer_code = ''
        self.langeron_integer_code = ''
        self.angles_range = []
        self.create_angles_range()

    def __repr__(self):
        info = 'Langeron Series-{} Name-{}, Created-{}'.format(self.series, self.model_name, self.creation_time)
        return info

    def prepare_to_wb(self):
        """This function prepare the LangeronModel object to introduce with Ansys WB and optimization script by
        create specific values: shell and langeron integer codes will provide information about shell angles to
        acp-pre, bytestring will introduce with parametric optimization script """
        self.shell_integer_code = self.create_integer_code('shell_angles')
        self.langeron_integer_code = self.create_integer_code('langeron_angles')
        self._convert_to_bites()

    @staticmethod
    def name_autoincrement(series, shell_angles):
        name = 'Series.' + series + ' Angles:' + shell_angles
        return name

    def create_angles_range(self):
        self.angles_range = [-89.0]
        step = 180 / 64
        for i in range(1, 64):
            self.angles_range.append(self.angles_range[i - 1] + step)

    def decode_angles_to_list(self, value):
        """
        string -> ['value1', 'value2', ... ]
        """
        list_of_angles = []
        value = getattr(self, value)
        for el in value.split(', '):
            if el != '':
                list_of_angles.append(el)
        return list_of_angles

    def create_integer_code(self, field):
        """
        Takes class field name, returns integer code in string, if there is up to 4 elements in field.
        This need to set the parameters in acp_pre.
        """
        result = ''
        for angle in getattr(self, field).split(', '):
            for i, el in enumerate(self.angles_range):
                if float(angle) == el:
                    result += str(i + 10)
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
        self.bytestring += format(int(len(self.shell_integer_code) / 2), '04b')
        self.bytestring += format(int(len(self.langeron_integer_code) / 2), '04b')
        argument = []
        for i in range(0, int(len(self.shell_integer_code) / 2)):
            tmp = int(self.shell_integer_code[2 * i: 2 * i + 2]) - 10
            argument.append(tmp)
        for el in argument:
            self.bytestring += format(el, '06b')
        self.bytestring += format(getattr(self, 'antiflatter_diam'), '03b')
        argument = length_dict[getattr(self, 'antiflatter_length')]
        self.bytestring += format(argument, '04b')
        self.bytestring += format(getattr(self, 'antiflatter_value'), '03b')
        argument = []
        for i in range(0, len(self.langeron_integer_code), 2):
            tmp = int(self.langeron_integer_code[i: i + 2]) - 10
            argument.append(tmp)
        for el in argument:
            self.bytestring += format(el, '06b')
        self.bytestring += format(getattr(self, 'wall_length') - 15, '05b')
        self.bytestring += format(getattr(self, 'wall_angle'), '06b')

    def read_from_bites(self, income_bytestring):
        # Read the number of shell layers
        number_of_shell_layers = int(income_bytestring[:4], 2)
        # Read the number of langeron layers
        number_of_langeron_layers = int(income_bytestring[4:8], 2)
        # Read the values of shell angles
        temporary_list = []
        result_dict = {
            'shell_integer_code': '',
            'langeron_integer_code': '',
            'antiflatter_diam': '',
            'antiflatter_length': '',
            'antiflatter_value': '',
            'wall_length': '',
            'wall_angle': ''
        }
        temporary_value = 8
        for i in range(number_of_shell_layers):
            temporary_list.append(int(income_bytestring[temporary_value + i: temporary_value + i + 6], 2) + 10)
            temporary_value += 6
        for el in temporary_list:
            result_dict['shell_integer_code'] += str(el)
        # Read antiflatter_diam
        result_dict['antiflatter_diam'] = int(income_bytestring[temporary_value:temporary_value + 3], 2)
        temporary_value += 3
        # Read antiflatter_length
        result_dict['antiflatter_length'] = int(income_bytestring[temporary_value: temporary_value + 4], 2) * 100
        temporary_value += 4
        # Read antiflatter value
        result_dict['antiflatter_value'] = int(income_bytestring[temporary_value: temporary_value + 3], 2)
        temporary_value += 3
        # Read the values of langeron angles
        temporary_list = []
        for i in range(number_of_langeron_layers):
            temporary_list.append(int(income_bytestring[temporary_value + i: temporary_value + i + 6], 2) + 10)
            temporary_value += 6
        for el in temporary_list:
            result_dict['langeron_integer_code'] += str(el)
        # Read wall_length
        result_dict['wall_length'] = int(income_bytestring[temporary_value: temporary_value + 5], 2) + 15
        temporary_value += 5
        # Read wall_angle
        result_dict['wall_angle'] = int(income_bytestring[temporary_value:], 2)

        return result_dict

    def update_values(self):
        data_to_update = {}
        for el in self.initialization_list:
            data_to_update[el] = getattr(self, el)
        tmp = BaseModel('langeron')
        tmp.update(new_data=data_to_update)
