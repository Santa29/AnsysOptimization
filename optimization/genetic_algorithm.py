import math
from random import randint

from .variables import population_size, max_generation_number


class GeneticAlgorithm:
    def __init__(self, list_of_wings):
        self.parents = []
        for wing in list_of_wings:
            self.parents.append(wing)
        self.children = []
        self.mutation_rate = 0.02
        self.best_individual = list_of_wings[0]

    def selection(self):
        # Set initial values
        total_parents_cost = 0
        max_parent_cost = -math.inf

        # Calculating total cost of parents
        for parent in self.parents:
            total_parents_cost += parent.get_cost()
            if max_parent_cost < parent.get_cost():
                max_parent_cost = parent.get_cost()

        # Calculating cost function
        t = 1.1
        f_max = t * max_parent_cost
        d = population_size * f_max - total_parents_cost
        p_selection = []
        for i in range(0, population_size):
            p_selection.append((f_max - self.parents[i].get_cost()) / d)

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

    def crossover(self, indices_parents):
        ch = [self.parents[indices_parents[0]], self.parents[indices_parents[1]]]
        crossover_points = [
            randint(0, len(ch[0].bytestring)),
            randint(0, len(ch[0].bytestring))
        ]
        if crossover_points[0] > crossover_points[1]:
            crossover_points[0], crossover_points[1] = crossover_points[1], crossover_points[0]
        for i in range(crossover_points[0], crossover_points[1]):
            ch[0].binary_encoding[i] = self.parents[indices_parents[1]].binary_encoding[i]
            ch[1].binary_encoding[i] = self.parents[indices_parents[0]].binary_encoding[i]
        self.children.append(ch[0])
        self.children.append(ch[1])

    def mutation(self):
        for child in self.children:
            for i in range(8, len(child.bytestring)):
                if randint(1, 100) <= 100 * self.mutation_rate:
                    if child.binary_encoding[i]:
                        child.binary_encoding[i] = False
                    else:
                        child.binary_encoding[i] = True

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
