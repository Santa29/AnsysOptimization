"""
This module provides the interface to easy interaction with DB.
"""

import datetime
import math

from .my_orm import BaseModel

BASELINE_MASS = 1290
BASELINE_VALUE_SPECTRUM = 6
OMEGA_MAX = 430
OMEGA_MIN = 35
R_NF = 1
BETA_NF = 2
BASELINE_SAFETY = 10
MAX_BIAS_TIP_FLAP = 6.7
R_BTF = 1
betaBTF = 2
r_twist = 1
beta_twist = 2
MAX_TIP_TWIST = 0.05
BASE_MASS_CENTER = 0.004
# Cost functions parameters
WEIGHT_MASS = 0.1
WEIGHT_NATURAL_FREQUENCIES = 0.02
WEIGHT_AEROELASTIC_STABILITY = 0.2
WEIGHT_STRENGTH = 0.68

WEIGHT_SIGMA = 0.25
WEIGHT_UZ = 0.25
WEIGHT_UR = 0.25
WEIGHT_UTWIST = 0.25


class ShellModel:
    """Default model of wing with longerone"""
    initialization_list = [
        'id',
        'polymer_volume_coordinate',
        'series',
        'model_name',
        'shell_angles',
        'value_vertical',
        'value_horizontal',
        'value_spectrum_modal_min',
        'value_spectrum_modal_max',
        'antiflatter_value',
        'antiflatter_diam',
        'antiflatter_length',
        'bytestring',
        'creation_time',
        'mass',
        'tip_flap',
        'twist_tip',
        'mass_center',
        'cost',
        'shell_integer_code'
    ]

    def __init__(self, row):
        self.series = ''
        self.shell_angles = ''
        self.polymer_volume_coordinate = 0
        self.data = []
        self.mass = 0
        self.value_spectrum_modal_min = ''
        self.value_spectrum_modal_max = ''
        self.value_vertical = 0.0
        self.value_horizontal = 0.0
        self.tip_flap = 0.0
        self.twist_tip = 0.0
        self.mass_center = 0.0
        self.cost = 0.0
        for i, el in enumerate(row):
            setattr(self, self.initialization_list[i], el)
        self.model_name = self.name_autoincrement()
        self.creation_time = datetime.datetime.now().strftime('%Y/%m/%d/%H:%M:%S')
        self.bytestring = ''
        self.shell_integer_code = ''
        self.angles_range = []
        self.create_angles_range()

    def __repr__(self):
        info = '[Shell Series-{} Name-{}, Created-{}]'.format(self.series, self.model_name, self.creation_time)
        return info

    def name_autoincrement(self):
        name = 'Shell Angles:' + str(self.shell_angles)
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

    def prepare_to_wb(self):
        """This function prepare the ShellModel object to introduce with Ansys WB and optimization script by
        create specific values: shell integer code will provide information about shell angles to
        acp-pre, bytestring will introduce with parametric optimization script """
        self.shell_integer_code = self.create_integer_code('shell_angles', 'shell_integer_code')
        self._convert_to_bites()
        self.update_values()

    def create_integer_code(self, field, field_name='shell_integer_code'):
        """
        Takes class field name, returns integer code in string and set it on field_name attribute.
        This need to set the parameters in acp_pre.
        """
        result = ''
        for angle in getattr(self, field).split(', '):
            for i, el in enumerate(self.angles_range):
                if float(angle) == el:
                    result += str(i + 10)
        setattr(self, field_name, result)
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
            200: 0,
            250: 1,
            300: 2,
            400: 3,
            500: 4,
            600: 5,
            700: 6,
            800: 7
        }
        antiflatter_diam_dict = {
            1: 0,
            2: 1,
            3: 2,
            4: 3
        }
        polymer_volume_coordinate_dict = {
            14: 0,
            16: 1,
            18: 2,
            20: 3,
        }
        self.bytestring = ''
        self.bytestring += format(int(len(self.shell_integer_code) / 2), '04b')
        argument = []
        for i in range(0, int(len(self.shell_integer_code) / 2)):
            tmp = int(self.shell_integer_code[2 * i: 2 * i + 2]) - 10
            argument.append(tmp)
        for el in argument:
            self.bytestring += format(el, '06b')
        argument = antiflatter_diam_dict[getattr(self, 'antiflatter_diam')]
        self.bytestring += format(argument, '02b')
        argument = length_dict[getattr(self, 'antiflatter_length')]
        self.bytestring += format(argument, '03b')
        self.bytestring += format(getattr(self, 'antiflatter_value'), '03b')
        argument = polymer_volume_coordinate_dict[getattr(self, 'polymer_volume_coordinate')]
        self.bytestring += format(argument, '02b')

    def read_from_bites(self, income_bytestring):
        # Read the number of shell layers
        number_of_shell_layers = int(income_bytestring[:4], 2)
        temporary_list = []
        antiflatter_diam_dict = {
            0: 1,
            1: 2,
            2: 3,
            3: 4
        }
        length_dict = {
            0: 200,
            1: 250,
            2: 300,
            3: 400,
            4: 500,
            5: 600,
            6: 700,
            7: 800
        }
        polymer_dict = {
            0: 14,
            1: 16,
            2: 18,
            3: 20
        }
        result_dict = {
            'shell_integer_code': '',
            'antiflatter_diam': '',
            'antiflatter_length': '',
            'antiflatter_value': '',
            'polymer_volume_coordinate': ''
        }
        temporary_value = 4
        for i in range(number_of_shell_layers):
            temporary_list.append(int(income_bytestring[temporary_value: temporary_value + 6], 2) + 10)
            temporary_value += 6
        for el in temporary_list:
            result_dict['shell_integer_code'] += str(el)
        # Read antiflatter_diam
        tmp = int(income_bytestring[temporary_value:temporary_value + 2], 2)
        tmp = antiflatter_diam_dict[tmp]
        result_dict['antiflatter_diam'] = tmp
        temporary_value += 2
        # Read antiflatter_length
        tmp = int(income_bytestring[temporary_value: temporary_value + 3], 2)
        tmp = length_dict[tmp]
        result_dict['antiflatter_length'] = tmp
        temporary_value += 3
        # Read antiflatter value
        result_dict['antiflatter_value'] = int(income_bytestring[temporary_value: temporary_value + 3], 2)
        temporary_value += 3
        # Read polymer volume coordinate
        tmp = int(income_bytestring[temporary_value:temporary_value + 2], 2)
        tmp = polymer_dict[tmp]
        result_dict['polymer_volume_coordinate'] = tmp

        for key, value in result_dict.items():
            setattr(self, key, value)
        self.series = 'need_calculate'
        return result_dict

    def update_values(self):
        data_to_update = {}
        for el in self.initialization_list:
            data_to_update[el] = getattr(self, el)
        tmp = BaseModel('shell')
        tmp.update(new_data=data_to_update)

    def cost_mass(self):
        self.mass = int(self.mass)
        return self.mass / BASELINE_MASS

    def cost_natural_frequencies(self):
        minimum_distance = math.inf
        n_f_max = []
        n_f_min = []
        for el in self.value_spectrum_modal_max.split(', '):
            n_f_max.append(float(el))
        for el in self.value_spectrum_modal_min.split(', '):
            n_f_min.append(float(el))
        for i in range(BASELINE_VALUE_SPECTRUM):
            a = (n_f_max[i] - n_f_min[i]) / (OMEGA_MAX ** 2 - OMEGA_MIN ** 2)
            b = n_f_min[i] - a * OMEGA_MIN ** 2
            for k in range(10):
                d = k ** 2 - 4 * a * b
                if d < 0:
                    continue
                omega_res_1 = (k - math.sqrt(d)) / (2 * a)
                omega_res_2 = (k + math.sqrt(d)) / (2 * a)
                dist = min(abs((OMEGA_MIN + OMEGA_MAX) / 2 - omega_res_1),
                           abs(omega_res_2 - (OMEGA_MIN + OMEGA_MAX) / 2))
                if dist < minimum_distance:
                    minimum_distance = dist
        cost = - minimum_distance / ((OMEGA_MAX - OMEGA_MIN) / 2)
        penalty = R_NF * math.pow(max(0.0, cost + 1.1), BETA_NF)
        return cost + penalty

    def cost_stress(self):
        self.value_vertical = float(self.value_vertical)
        self.value_horizontal = float(self.value_horizontal)
        return min(self.value_vertical, self.value_horizontal) / BASELINE_SAFETY

    def cost_aeroelastic_stability(self):
        self.mass_center = float(self.mass_center)
        tmp = abs((self.mass_center - 0.0025) / BASE_MASS_CENTER - 0.0025)
        return tmp

    def cost_penalty(self):
        self.value_vertical = float(self.value_vertical)
        self.value_horizontal = float(self.value_horizontal)
        self.tip_flap = float(self.tip_flap)
        self.twist_tip = float(self.twist_tip)
        safety_factor = max(self.value_vertical, self.value_horizontal)
        safety_factor_utopia = (self.value_horizontal + self.value_vertical) / 2
        delta_safety_factor = (self.value_horizontal - self.value_vertical) / 2
        g_strength = R_NF * pow(
            max(0.0, (abs(safety_factor - safety_factor_utopia) - delta_safety_factor) / delta_safety_factor), BETA_NF)
        g_uz = R_BTF * pow(max(0.0, (abs(self.tip_flap) - MAX_BIAS_TIP_FLAP) / MAX_BIAS_TIP_FLAP), betaBTF)
        g_u_twist = pow(max(0.0, abs(abs(self.twist_tip) - MAX_TIP_TWIST) / MAX_TIP_TWIST), beta_twist)
        return WEIGHT_STRENGTH * g_strength + WEIGHT_UZ * g_u_twist + WEIGHT_UTWIST * g_uz

    def get_cost(self):
        result = WEIGHT_MASS * self.cost_mass() + WEIGHT_NATURAL_FREQUENCIES * self.cost_natural_frequencies()
        result += WEIGHT_AEROELASTIC_STABILITY * self.cost_aeroelastic_stability()
        result += WEIGHT_STRENGTH * self.cost_stress()
        result += self.cost_penalty()
        self.cost = result
        return result

    def get_dict_representation(self):
        repr_dict = {}
        for el in self.initialization_list:
            if el != 'id':
                repr_dict[el] = getattr(self, el)
        return repr_dict
