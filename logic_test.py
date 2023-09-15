import unittest
from test import test_values_for_logic_test
from random import randint

from models.my_orm import BaseModel
from models.langeron import LangeronModel
from optimization.genetic_algorithm import GeneticAlgorithm
from optimization.variables import population_size


class TestLangeron(unittest.TestCase):
    def setUp(self):
        self.base = BaseModel('current_item')
        self.test_case = {'id': 1,
                          'langeron_angles': '-58.0625, 20.6875, 48.8125, 1.0, 54.4375',
                          'langeron_wall_angles': '46.0, -77.75, 82.5625, 34.75, 29.125',
                          'wall_length': 25,
                          'wall_angle': 23,
                          'polymer_volume_coordinate': 14,
                          'series': 'test_langeron',
                          'model_name': '',
                          'shell_angles': '-60.875, -55.25, -7.4375',
                          'value_vertical': '',
                          'value_horizontal': '',
                          'value_spectrum_modal_min': '',
                          'value_spectrum_modal_max': '',
                          'antiflatter_value': 3,
                          'antiflatter_diam': 2,
                          'antiflatter_length': 400,
                          'bytestring': '',
                          'creation_time': '',
                          'mass': 430,
                          'tip_flap': 40.0,
                          'twist_tip': 15.0,
                          'mass_center': 110,
                          'cost': 0.0,
                          'langeron_integer_code': '',
                          'shell_integer_code': ''
                          }
        self.langeron = LangeronModel(self.test_case.values())

    def test_model_creation(self):
        for el in self.test_case:
            if el != 'model_name' and el != 'creation_time':
                self.assertEqual(self.langeron.__getattribute__(el), self.test_case[el])

    def test_repr(self):
        self.assertEqual(self.langeron.model_name, 'Series.test_langeron Angles:-60.875, -55.25, -7.4375')

    def test_decode_angles_to_list(self):
        self.assertEqual(self.langeron.decode_angles_to_list('shell_angles'), ['-60.875', '-55.25', '-7.4375'])
        self.assertEqual(self.langeron.decode_angles_to_list('langeron_angles'),
                         ['-58.0625', '20.6875', '48.8125', '1.0', '54.4375'])

    def test_create_integer_code(self):
        self.assertEqual(self.langeron.create_integer_code('shell_angles'), '202239')
        self.assertEqual(self.langeron.create_integer_code('langeron_angles'), '2149594261')

    def test_get_attr(self):
        self.assertEqual(self.langeron.__getattribute__('shell_angles').split(', '), ['-60.875', '-55.25', '-7.4375'])
        self.assertEqual(self.langeron.__getattribute__('langeron_angles').split(', '),
                         ['-58.0625', '20.6875', '48.8125', '1.0', '54.4375'])

    def test_prepare_to_wb(self):
        self.langeron.prepare_to_wb()
        self.assertEqual(self.langeron.shell_integer_code, '202239')
        self.assertEqual(self.langeron.langeron_integer_code, '2149594261')
        self.assertEqual(self.langeron.bytestring,
                         '00110101001010001100011101010110110010111001111100011000001100110001011100')

    def test_read_from_bytes(self):
        self.langeron.prepare_to_wb()
        self.test_case['shell_integer_code'] = self.langeron.shell_integer_code
        self.test_case['langeron_integer_code'] = self.langeron.langeron_integer_code
        result = self.langeron.read_from_bites(self.langeron.bytestring)
        for el in result:
            self.assertEqual(self.test_case[el], result[el])

    def test_replace_values_from_bytestring(self):
        self.langeron.prepare_to_wb()
        list_of_calculated_attributes = [
            'model_name',
            'creation_time',
            'bytestring',
            'series',
            'langeron_integer_code',
            'shell_integer_code'
        ]
        for el in self.test_case:
            if el not in list_of_calculated_attributes:
                self.assertEqual(self.langeron.__getattribute__(el), self.test_case[el])

    def test_repr_dict(self):
        self.langeron.prepare_to_wb()
        print(self.langeron.get_dict_representation())


class OptimizationTest(unittest.TestCase):
    def setUp(self):
        self.base = BaseModel('current_item')
        self.langeron_list = []
        for i in range(population_size):
            tmp = test_values_for_logic_test(i)
            tmp['id'] = i
            self.langeron_list.append(LangeronModel(tmp.values()))
        self.optimization_test = GeneticAlgorithm(self.langeron_list)

    def test_full_optimization_operation_for_high_level_mistakes(self):
        for i in range(10):
            tmp = self.optimization_test.selection()
            self.optimization_test.crossover(tmp)
        self.optimization_test.mutation()

    def test_calculating_total_cost_of_parents(self):
        tmp_list = []
        for parent in self.optimization_test.parents:
            parent.prepare_to_wb()
            tmp_list.append(parent.get_cost())
        t_cost, m_cost = self.optimization_test.calculating_total_cost_of_parents()
        self.assertEqual(t_cost, sum(tmp_list))
        self.assertEqual(m_cost, max(tmp_list))

    def test_calculating_p_selection(self):
        t_cost, m_cost = self.optimization_test.calculating_total_cost_of_parents()
        self.assertAlmostEqual(sum(self.optimization_test.calculating_p_selection(m_cost, t_cost)), 1, 2)

    def test_roulette(self):
        t_cost, m_cost = self.optimization_test.calculating_total_cost_of_parents()
        p_selection = self.optimization_test.calculating_p_selection(m_cost, t_cost)
        id_list = [0] * len(p_selection)
        for i in range(len(p_selection) * 100):
            tmp = self.optimization_test.roulette(p_selection)
            id_list[tmp[0]] += 1
            id_list[tmp[1]] += 1
        for i in range(len(id_list)):
            id_list[i] /= (len(p_selection) * 100 * 2)
        print('\n', id_list, '\n', p_selection)

    def test_optimization(self):
        pass

    def test_selection(self):
        pass

    def test_mutation(self):
        parents_list = ''
        children_list = ''
        for i in range(10):
            tmp = self.optimization_test.selection()
            self.optimization_test.crossover(tmp)
        for child in self.optimization_test.children:
            child.prepare_to_wb()
            parents_list += child.bytestring
        self.optimization_test.mutation()
        for child in self.optimization_test.children:
            child.prepare_to_wb()
            children_list += child.bytestring
        counter = 0
        for i in range(len(parents_list)):
            if parents_list[i] != children_list[i]:
                counter += 1
        print('\n' + parents_list + '\n' + children_list)
        self.assertAlmostEqual(self.optimization_test.mutation_rate * 0.01, counter / len(parents_list), 1)


if __name__ == '__main__':
    unittest.main()
