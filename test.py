"""Some minor functions to test the script working"""
from random import randint, choice
from models.my_orm import BaseModel
from models.langeron import LangeronModel
from models.shell import ShellModel


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


def test_values_for_logic_test(test_id, model='langeron'):
    if model == 'langeron':
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
            'cost': randint(5, 15) / 10
        }
        return values
    elif model == 'shell':
        modes_min = generate_modal_values(6)
        modes_max = generate_max_modal_values(modes_min)
        values = {
            'id': test_id,
            'polymer_volume_coordinate': choice([14, 16, 18, 20]),
            'series': 'need_calculate',
            'model_name': '',
            'shell_angles': generate_test_angles(3),
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
            'cost': randint(5, 15) / 10
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
    if mode in ['values', 'test', 'prepare', 'search_doubles']:
        a = BaseModel('langeron')
    elif mode in ['values_shell', 'test_shell', 'prepare_shell', 'search_doubles_shell']:
        a = BaseModel('shell')
    else:
        a = BaseModel('langeron')
    current_object_list = []
    data_set = []
    if mode == 'values':
        for i in range(50):
            current_object_list.append(test_values_for_logic_test(i))
        a.bulk_insert(current_object_list)
    if mode == 'values_shell':
        for i in range(500):
            current_object_list.append(test_values_for_logic_test(i, model='shell'))
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
    if mode == 'test_shell':
        current_object_list = a.select_by_series('calculated')
        shell_list = []
        for obj in current_object_list:
            shell_list.append(ShellModel(obj))
        for obj in shell_list:
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
    if mode == 'prepare_shell':
        current_object_list = a.select_by_series('need_calculate')
        shell_list = []
        for obj in current_object_list:
            shell_list.append(ShellModel(obj))
        for obj in shell_list:
            obj.prepare_to_wb()
    if mode == 'search_doubles':
        tmp_1 = a.select_by_series('need_calculate')
        tmp_2 = a.select_by_series('calculated')
        current_object_list = []
        search_list = []
        for langeron in tmp_1:
            current_object_list.append(LangeronModel(langeron))
        for langeron in tmp_2:
            search_list.append(LangeronModel(langeron))
        for elem in search_list:
            elem.prepare_to_wb()
        for langeron in current_object_list:
            langeron.prepare_to_wb()
            langeron.series = 'calculated'
            for elem in search_list:
                if elem.bytestring == langeron.bytestring:
                    langeron.series = elem.series
                    langeron.value_vertical = elem.value_vertical
                    langeron.value_horizontal = elem.value_horizontal
                    langeron.value_spectrum_modal_max = elem.value_spectrum_modal_max
                    langeron.value_spectrum_modal_min = elem.value_spectrum_modal_min
                    langeron.mass = elem.mass
                    langeron.tip_flap = elem.tip_flap
                    langeron.twist_tip = elem.twist_tip
                    langeron.mass_center = elem.mass_center
                    langeron.update_values()
    if mode == "search_doubles_shell":
        tmp_1 = a.select_by_series('need_calculate')
        tmp_2 = a.select_by_series('calculated')
        current_object_list = []
        search_list = []
        for shell in tmp_1:
            current_object_list.append(ShellModel(shell))
        for shell in tmp_2:
            search_list.append(ShellModel(shell))
        for elem in search_list:
            elem.prepare_to_wb()
        for shell in current_object_list:
            shell.prepare_to_wb()
            shell.series = 'calculated'
            for elem in search_list:
                if elem.bytestring == shell.bytestring:
                    shell.series = elem.series
                    shell.value_vertical = elem.value_vertical
                    shell.value_horizontal = elem.value_horizontal
                    shell.value_spectrum_modal_max = elem.value_spectrum_modal_max
                    shell.value_spectrum_modal_min = elem.value_spectrum_modal_min
                    shell.mass = elem.mass
                    shell.tip_flap = elem.tip_flap
                    shell.twist_tip = elem.twist_tip
                    shell.mass_center = elem.mass_center
                    shell.update_values()