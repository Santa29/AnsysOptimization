"""Some minor functions to test the script working"""
from random import randint, choice
from models.my_orm import BaseModel
from models.langeron import LangeronModel


def test_values_for_orm(model_type='Shell'):
    if model_type == 'Langeron':
        values = {
            'series': 'test_langeron',
            'antiflatter_value': randint(0, 7),
            'antiflatter_diam': randint(1, 5),
            'antiflatter_length': randint(3, 8) * 100,
            'wall_length': randint(15, 30),
            'wall_angle': randint(0, 25),
            'polymer_volume_coordinate': randint(5, 15),
            'shell_angles': generate_test_angles(2),
            'langeron_angles': generate_test_angles(5),
            'langeron_wall_angles': generate_test_angles(5)
        }
        return values

    if model_type == 'Shell':
        values = {
            'series': 'test_shell',
            'antiflatter_value': randint(0, 7),
            'antiflatter_diam': randint(1, 5),
            'antiflatter_length': randint(3, 8) * 100,
            'shell_angles': generate_test_angles(3),
        }
        return values


def test_values_for_logic_test(test_id):
    modes_min = generate_modal_values(6)
    modes_max = generate_max_modal_values(modes_min)
    values = {
        'id': test_id,
        'langeron_angles': generate_test_angles(3),
        'langeron_wall_angles': generate_test_angles(3),
        'wall_length': randint(25, 32),
        'wall_angle': randint(0, 31),
        'polymer_volume_coordinate': choice([14, 16, 18, 20]),
        'series': 'need_calculate',
        'model_name': '',
        'shell_angles': generate_test_angles(2),
        'value_vertical': randint(30, 1000) / 100,
        'value_horizontal': randint(30, 1000) / 100,
        'value_spectrum_modal_min': list_to_string(modes_min),
        'value_spectrum_modal_max': list_to_string(modes_max),
        'antiflatter_value': randint(0, 7),
        'antiflatter_diam': choice([1, 2, 3, 4]),
        'antiflatter_length': choice([200, 250, 300, 400, 500, 600, 700, 800]),
        'bytestring': '',
        'creation_time': '',
        'mass': randint(0, 300),
        'tip_flap': randint(10, 100) / 10,
        'twist_tip': randint(100, 250) / 10,
        'mass_center': randint(50, 300),
        'cost': 0.0
    }
    return values


def generate_test_angles(value):
    angles_range = [float(-89.0)]
    step = float(180 / 64)
    for i in range(1, 64):
        angles_range.append(angles_range[i - 1] + step)
    angles = ''
    for i in range(value):
        if i < (value - 1):
            angles = angles + str(choice(angles_range)) + ', '
        else:
            angles = angles + str(choice(angles_range))
    return angles


def generate_modal_values(value):
    values = []
    for i in range(value):
        values.append(randint(100, 1300))
    values = sorted(values)
    return values


def list_to_string(list_values):
    modal_range = ''
    for i, el in enumerate(list_values):
        if i < (len(list_values) - 1):
            modal_range += str(el) + ', '
        else:
            modal_range += str(el)
    return modal_range


def generate_max_modal_values(modes_list):
    new_list = []
    for el in modes_list:
        new_list.append(el + randint(10, 40))
    return new_list


if __name__ == '__main__':
    mode = input()
    a = BaseModel('langeron')
    current_object_list = []
    data_set = []
    if mode == 'values':
        for i in range(50):
            current_object_list.append(test_values_for_logic_test(i))
        a.bulk_insert(current_object_list)
    if mode == 'test':
        current_object_list = a.select_by_series('calculated')
        langeron_list = []
        for obj in current_object_list:
            langeron_list.append(LangeronModel(obj))
        for obj in langeron_list:
            obj.get_cost()
            obj.prepare_to_wb()
            obj.update_values()
    if mode == 'prepare':
        current_object_list = a.select_by_series('need_calculate')
        langeron_list = []
        for obj in current_object_list:
            langeron_list.append(LangeronModel(obj))
        for obj in langeron_list:
            obj.prepare_to_wb()
