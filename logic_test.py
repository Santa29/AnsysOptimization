import unittest
from random import randint

from models.my_orm import BaseModel
from models.langeron import LangeronModel


class TestLangeron(unittest.TestCase):
    def setUp(self):
        self.base = BaseModel('current_item')
        self.test_case = {'id': 1,
                          'langeron_angles': '-58.0625, 20.6875, 48.8125, 1.0, 54.4375',
                          'langeron_wall_angles': '46.0, -77.75, 82.5625, 34.75, 29.125',
                          'wall_length': 25,
                          'wall_angle': 23,
                          'polymer_volume_coordinate': 3,
                          'series': 'test_langeron',
                          'model_name': '',
                          'shell_angles': '-60.875, -55.25, -7.4375',
                          'value_vertical': '',
                          'value_horizontal': '',
                          'value_spectrum_modal': '',
                          'antiflatter_value': 3,
                          'antiflatter_diam': 2,
                          'antiflatter_length': 400,
                          'bytestring': '',
                          'creation_time': ''}
        self.langeron = LangeronModel(self.test_case.values())

    def test_model_creation(self):
        for el in self.test_case:
            if el != 'model_name' and el != 'creation_time':
                self.assertEqual(self.langeron.__getattribute__(el), self.test_case[el])

    def test_repr(self):
        self.assertEqual(self.langeron.model_name, 'Series.test_langeron Angles:-60.875, -55.25, -7.4375')

    def test_decode_angles_to_list(self):
        self.assertEqual(self.langeron.decode_angles_to_list('shell_angles'), ['-60.875', '-55.25', '-7.4375'])
        self.assertEqual(self.langeron.decode_angles_to_list('langeron_angles'), ['-58.0625', '20.6875', '48.8125', '1.0', '54.4375'])

    def test_create_integer_code(self):
        self.assertEqual(self.langeron.create_integer_code('shell_angles'), '202239')
        self.assertEqual(self.langeron.create_integer_code('langeron_angles'), '2250435962')

    def test_get_attr(self):
        self.assertEqual(self.langeron.__getattribute__('shell_angles').split(', '), ['-60.875', '-55.25', '-7.4375'])
        self.assertEqual(self.langeron.__getattribute__('langeron_angles').split(', '), ['-58.0625', '20.6875', '48.8125', '1.0', '54.4375'])

    def test_prepare_to_wb(self):
        self.langeron.prepare_to_wb()
        self.assertEqual(self.langeron.shell_integer_code, '202239')
        self.assertEqual(self.langeron.langeron_integer_code, '2250435962')
        self.assertEqual(self.langeron.bytestring, '00110101010100010110100111010010001111000111101110101011110101010010111')

    def test_read_from_bytes(self):
        self.langeron.prepare_to_wb()
        self.test_case['shell_integer_code'] = self.langeron.shell_integer_code
        self.test_case['langeron_integer_code'] = self.langeron.langeron_integer_code
        result = self.langeron.read_from_bites(self.langeron.bytestring)
        for el in result:
            self.assertEqual(self.test_case[el], result[el])


if __name__ == '__main__':
    unittest.main()
