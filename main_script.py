import subprocess

from models.langeron import LangeronModel
from models.shell import ShellModel
from models.my_orm import BaseModel

from optimization.genetic_algorithm import GeneticAlgorithm

import os

# Get 20 values from db
# Run wb_script to calculate all values
# Run optimization script to get the children
# Write children in db

dir_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(dir_path, 'scripts', 'log.txt')
db_path = os.path.join(dir_path, 'experiment.sqlite')
wb_script_path = r'C:\Ansys projects\Lopast_helicopter\AnsysOptimization\workbench_script.py'
wb_project_path = r'C:\Ansys projects\Lopast_helicopter\Lopast_helicopter.wbpj'
wb_main_path = r'C:\Program Files\ANSYS Inc\V221\Framework\bin\win64\runwb2'

table = BaseModel('langeron')


def make_optimization(parents_list, model='langeron'):
    """
    This function get 20 LangeronModels with all calculated values from db and return the new 20 LangeronModels for
    future analyse
    """
    optimization = GeneticAlgorithm(parents_list, model)
    optimization.optimization()
    list_to_bulk_insert = []
    for child in optimization.children:
        list_to_bulk_insert.append(child.get_dict_representation())
    return list_to_bulk_insert


def calculate_values_in_wb(series_counter, model='langeron'):
    # TODO fix this function to avoid solid series counter, see main code for example
    """This function calculate the values in wb and return list of calculated LangeronModels depends on
    series_counter """
    if model == 'shell':
        current_table = BaseModel('shell')
    else:
        current_table = BaseModel('langeron')
    langeron_list = []
    for el in current_table.select_by_series('need_calculate'):
        langeron_list.append(LangeronModel(el))
    for el in langeron_list:
        el.prepare_to_wb()
    process = subprocess.Popen("%s -B -F %s -R %s" % (wb_main_path, wb_project_path, wb_script_path))
    process.wait()
    for el in langeron_list:
        el.get_cost()
    langeron_list = []
    for j in range(series_counter * 20 + 241, series_counter * 20 + 261):
        langeron_list.append(LangeronModel(current_table.select_by_id(j).fetchone()))
    return langeron_list


def add_best_individuals(model='langeron'):
    """
    This function searches for the two best individuals in all generations and replaces the first two generated
    individuals in the last generation with them.
    """
    if model == 'shell':
        current_table = BaseModel('shell')
    else:
        current_table = BaseModel('langeron')
    remaining_individuals = []
    current_generation = []
    best_individuals = []
    current_generation_rows_set = current_table.select_by_series('need_calculate').fetchall()
    for k in range(2):
        current_generation.append(LangeronModel(current_generation_rows_set[k]))
    all_rows_list = current_table.select_by_series('calculated').fetchall()
    for n in all_rows_list:
        remaining_individuals.append(LangeronModel(n))
    remaining_individuals.sort(key=lambda x: x.cost)
    best_individuals.append(remaining_individuals[0])
    for individual in remaining_individuals:
        if individual.cost != best_individuals[0].cost:
            best_individuals.append(individual)
            break
    for elem in best_individuals:
        print(elem.cost)
    replace_values(best_individuals, current_generation)


def replace_values(first_pair: list, second_pair: list):
    """
    this function replaces the properties of objects from the second list with the properties of objects from the
    first list.
    """
    for i in range(2):
        first_pair[i].prepare_to_wb()
        second_pair[i].prepare_to_wb()
        for current_property in second_pair[i].__dict__.keys():
            if current_property in ['id', 'angles_range']:
                pass
            temp = getattr(first_pair[i], current_property)
            setattr(second_pair[i], current_property, temp)
            second_pair[i].update_values()


def search_duplicate_values(model='langeron'):
    """
    This function search duplicate values throw all previous calculated models. If model already calculated,
    this function change series status of the current duplicate.
    """
    if model == 'shell':
        current_table = BaseModel('shell')
    else:
        current_table = BaseModel('langeron')
    tmp_1 = current_table.select_by_series('need_calculate')
    tmp_2 = current_table.select_by_series('calculated')
    current_object_list = []
    search_list = []
    if model == 'shell':
        for shell in tmp_1:
            current_object_list.append(ShellModel(shell))
        for shell in tmp_2:
            search_list.append(ShellModel(shell))
    else:
        for langeron in tmp_1:
            current_object_list.append(LangeronModel(langeron))
        for langeron in tmp_2:
            search_list.append(LangeronModel(langeron))
    for elem in search_list:
        elem.prepare_to_wb()
        elem.series = 'calculated'
        elem.update_values()
    if model == 'shell':
        for shell in current_object_list:
            shell.prepare_to_wb()
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
    else:
        for langeron in current_object_list:
            langeron.prepare_to_wb()
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


# Read the mode of the script. If mode == 0 - this is first initialization
mode = int(input())
temporary_langeron_list = []
# Preselected id valuable items from expert
selected_langeron_ids = [12, 26, 91, 23, 19, 57, 21, 69, 88, 72, 87, 85, 100, 35, 6, 97, 4, 80, 95, 59]
selected_shell_ids = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

if mode == 0:
    for j in selected_langeron_ids:
        temporary_langeron_list.append(LangeronModel(table.select_by_id(j).fetchone()))
    calculated_langeron_list = make_optimization(temporary_langeron_list)
    table.bulk_insert(calculated_langeron_list)
elif mode == 1:
    tmp = int(table.select_by_series('calculated').fetchall()[-1][0]) - 19
    for j in range(20):
        temporary_langeron_list.append(LangeronModel(table.select_by_id(tmp + j).fetchone()))
    calculated_langeron_list = make_optimization(temporary_langeron_list)
    for el in calculated_langeron_list:
        el['series'] = 'need_calculate'
    table.bulk_insert(calculated_langeron_list)
    search_duplicate_values()
    add_best_individuals()
elif mode == 2:
    tmp_list = table.select_by_series('calculated').fetchall()
    langeron_tmp_list = []
    for el in tmp_list:
        langeron_tmp_list.append(LangeronModel(el))
    for el in langeron_tmp_list:
        el.get_cost()
        el.prepare_to_wb()
        el.update_values()
elif mode == 3:
    table = BaseModel('shell')
    for j in selected_shell_ids:
        temporary_langeron_list.append(ShellModel(table.select_by_id(j).fetchone()))
    calculated_langeron_list = make_optimization(temporary_langeron_list)
    table.bulk_insert(calculated_langeron_list)
elif mode == 4:
    table = BaseModel('shell')
    tmp = int(table.select_by_series('calculated').fetchall()[-1][0]) - 19
    for j in range(20):
        temporary_langeron_list.append(ShellModel(table.select_by_id(tmp + j).fetchone()))
    calculated_langeron_list = make_optimization(temporary_langeron_list, model='shell')
    for el in calculated_langeron_list:
        el['series'] = 'need_calculate'
    table.bulk_insert(calculated_langeron_list)
    search_duplicate_values()
    add_best_individuals()
elif mode == 5:
    table = BaseModel('shell')
    tmp_list = table.select_by_series('calculated').fetchall()
    langeron_tmp_list = []
    for el in tmp_list:
        langeron_tmp_list.append(ShellModel(el))
    for el in langeron_tmp_list:
        el.get_cost()
        el.prepare_to_wb()
        el.update_values()
