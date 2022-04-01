from .my_orm import BaseModel


class WBLangeronModel:
    def __init__(self, row):
        self.initialization_list = [
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
            'langeron_integer_code',
            'shell_integer_code'
        ]
        self.id = 0
        self.langeron_angles = ''
        self.langeron_wall_angles = ''
        self.wall_length = 0
        self.wall_angle = 0
        self.polymer_volume_coordinate = 0
        self.series = ''
        self.model_name = ''
        self.shell_angles = ''
        self.value_vertical = 0.0
        self.value_horizontal = 0.0
        self.value_spectrum_modal_min = ''
        self.value_spectrum_modal_max = ''
        self.antiflatter_value = 0
        self.antiflatter_diam = 0
        self.antiflatter_length = 0
        self.bytestring = ''
        self.creation_time = ''
        self.mass = 0
        self.tip_flap = 0
        self.twist_tip = 0.0
        self.mass_center = 0.0
        self.cost = 0.0
        self.langeron_integer_code = ''
        self.shell_integer_code = ''
        for i, el in enumerate(row):
            setattr(self, self.initialization_list[i], el)

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
        tmp = BaseModel('langeron')
        tmp.update(new_data=data_to_update)