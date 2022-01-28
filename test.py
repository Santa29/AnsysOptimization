"""Some minor functions to test the script working"""
from random import randint, randrange


def test_values_for_orm(model_type='Shell'):
    if model_type == 'Langeron':
        values = {
            'series': 'test_langeron',
            'antiflatter_value': randint(0, 7),
            'antiflatter_diam': randint(1, 5),
            'antiflatter_length': randint(3, 9) * 100,
            'wall_length': randint(15, 40),
            'wall_angle': randint(0, 25),
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
            'antiflatter_length': randint(300, 900) * 100,
            'wall_length': randint(15, 40),
            'wall_angle': randint(0, 25),
            'polymer_volume_coordinate': randint(5, 15),
            'shell_angles': generate_test_angles(3),
        }
        return values


def generate_test_angles(value):
    angles = ''
    for i in range(value):
        if i < (value - 1):
            angles = angles + str(randrange(0, 91, 15)) + ', '
        else:
            angles = angles + str(randrange(0, 91, 15))
    return angles
