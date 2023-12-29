import math
from random import randint

from test import test_values_for_logic_test
from .variables import population_size
from models.my_orm import BaseModel
from models.langeron import LangeronModel
from models.shell import ShellModel


class GeneticAlgorithm:
    def __init__(self, list_of_wings, model='langeron'):
        self.table_name = model
        self.table = BaseModel(self.table_name)
        self.parents = []
        for wing in list_of_wings:
            self.parents.append(wing)
        self.children = []
        self.mutation_rate = 2
        self.best_individual = list_of_wings[0]

    def roulette(self, p_selection):
        # Creating the roulette
        indices_parents = [0, 1]
        for i in range(len(indices_parents)):
            sector = 0
            r = randint(1, 100) / 100
            wheel_sector_max = p_selection[0]
            while sector != population_size - 1 and r > wheel_sector_max:
                sector += 1
                wheel_sector_max += p_selection[sector]
            if i == 1 and sector == indices_parents[0]:
                i -= 1
            else:
                indices_parents[i] = sector
        return indices_parents

    def calculating_total_cost_of_parents(self):
        # Set initial values
        total_parents_cost = 0
        max_parent_cost = -math.inf

        # Calculating total cost of parents
        for parent in self.parents:
            total_parents_cost += parent.get_cost()
            if max_parent_cost < parent.get_cost():
                max_parent_cost = parent.get_cost()
        return total_parents_cost, max_parent_cost

    def calculating_p_selection(self, max_cost, total_cost):
        t = 1.1
        max_parent_cost = max_cost
        total_parents_cost = total_cost
        f_max = t * max_parent_cost
        d = population_size * f_max - total_parents_cost
        p_selection = []
        for i in range(0, population_size):
            p_selection.append((f_max - self.parents[i].get_cost()) / d)

        return p_selection

    def selection(self):
        total_parents_cost, max_parent_cost = self.calculating_total_cost_of_parents()
        p_selection = self.calculating_p_selection(total_parents_cost, max_parent_cost)
        return self.roulette(p_selection)

    def crossover(self, indices_parents):
        # create tuple of selected variants
        ch = [self.parents[indices_parents[0]], self.parents[indices_parents[1]]]
        # get the bytestring
        for parent in ch:
            parent.prepare_to_wb()
            parent.series = 'calculated'
            parent.update_values()
        # get the points of crossover
        crossover_points = [
            randint(0, len(ch[0].bytestring)),
            randint(0, len(ch[0].bytestring))
        ]
        # sort crossover points
        if crossover_points[0] > crossover_points[1]:
            crossover_points[0], crossover_points[1] = crossover_points[1], crossover_points[0]
        # create temporary list representation of selected variants
        tmp_list_ch_0 = list(ch[0].bytestring)
        tmp_list_ch_1 = list(ch[1].bytestring)
        floating_chapter_0 = tmp_list_ch_0[crossover_points[0]:crossover_points[1]]
        floating_chapter_1 = tmp_list_ch_1[crossover_points[0]:crossover_points[1]]
        # make crossover in temporary list representation
        for i in range(crossover_points[0], crossover_points[1]):
            tmp_index = i - crossover_points[0]
            tmp_list_ch_0[i] = floating_chapter_1[tmp_index]
            tmp_list_ch_1[i] = floating_chapter_0[tmp_index]
        # change initial values from bytestring to selected variants
        # for parent in ch:
        #     parent.read_from_bites(parent.bytestring)
        #     parent.series = 'calculated'
        #     parent.update_values()
        # calculate current last id value
        tmp = int(self.table.select_by_series('calculated').fetchall()[-1][0]) + len(self.children)
        if self.table_name == 'langeron':
            random_new_wing_list = [
                LangeronModel(test_values_for_logic_test(tmp + 1).values()),
                LangeronModel(test_values_for_logic_test(tmp + 2).values())
            ]
        else:
            random_new_wing_list = [
                ShellModel(test_values_for_logic_test(tmp + 1, model='shell').values()),
                ShellModel(test_values_for_logic_test(tmp + 2, model='shell').values())
            ]
        random_new_wing_list[0].read_from_bites(''.join(tmp_list_ch_0))
        random_new_wing_list[1].read_from_bites(''.join(tmp_list_ch_1))
        self.children.append(random_new_wing_list[0])
        self.children.append(random_new_wing_list[1])

    def mutation(self):
        for child in self.children:
            child.prepare_to_wb()
            list_representation = list(child.bytestring)
            for i in range(8, len(child.bytestring)):
                if randint(1, 100) <= self.mutation_rate:
                    if list_representation[i] == '0':
                        list_representation[i] = '1'
                    else:
                        list_representation[i] = '0'
            child.bytestring = ''.join(list_representation)
            child.read_from_bites(child.bytestring)
            child.update_values()

    def optimization(self):
        # generation_number = 1
        for parent in self.parents:
            parent.get_cost()
            if parent.cost < self.best_individual.cost:
                self.best_individual = parent
        indices_parent = [0, 0]
        # while generation_number <= max_generation_number:
        for j in range(0, int(population_size / 2)):
            self.crossover(self.selection())
        self.mutation()
        # Estimate children cost
        for child in self.children:
            child.get_cost()
            if child.cost < self.best_individual.cost:
                self.best_individual = child
        # Next generation
        # self.parents = self.children
        # self.children.clear()
        # generation_number += 1
        return self.children
