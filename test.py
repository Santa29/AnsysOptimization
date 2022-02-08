"""Some minor functions to test the script working"""
from random import randint, choice


def test_values_for_orm(model_type='Shell'):
    if model_type == 'Langeron':
        values = {
            'series': 'test_langeron',
            'antiflatter_value': randint(0, 7),
            'antiflatter_diam': randint(1, 5),
            'antiflatter_length': randint(3, 8) * 100,
            'wall_length': randint(15, 30),
            'wall_angle': randint(-25, 25),
            'polymer_volume_coordinate': randint(5, 15),
            'shell_angles': generate_test_angles(3),
            'langeron_angles': generate_test_angles(6),
            'langeron_wall_angles': generate_test_angles(6)
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
