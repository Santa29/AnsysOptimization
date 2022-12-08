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


def make_optimization(parents_list):
    """
    This function get 20 LangeronModels with all calculated values from db and return the new 20 LangeronModels for
    future analyse
    """
    optimization = GeneticAlgorithm(parents_list)
    optimization.optimization()
    list_to_bulk_insert = []
    for child in optimization.children:
        list_to_bulk_insert.append(child.get_dict_representation())
    return list_to_bulk_insert


def calculate_values_in_wb(series_counter):
    """This function calculate the values in wb and return list of calculated LangeronModels depends on
    series_counter """
    langeron_list = []
    for el in table.select_by_series('need_calculate'):
        langeron_list.append(LangeronModel(el))
    for el in langeron_list:
        el.prepare_to_wb()
    process = subprocess.Popen("%s -B -F %s -R %s" % (wb_main_path, wb_project_path, wb_script_path))
    process.wait()
    for el in langeron_list:
        el.get_cost()
    langeron_list = []
    for j in range(series_counter * 20 + 241, series_counter * 20 + 261):
        langeron_list.append(LangeronModel(table.select_by_id(j).fetchone()))
    return langeron_list


counter = 0
for i in range(5):
    temporary_langeron_list = []
    if i == 0:
        for j in range(1, 21):
            temporary_langeron_list.append(LangeronModel(table.select_by_id(j).fetchone()))
        calculated_langeron_list = make_optimization(temporary_langeron_list)
        table.bulk_insert(calculated_langeron_list)
        counter += 1
    else:
        temporary_langeron_list = calculate_values_in_wb(counter)
        calculated_langeron_list = make_optimization(temporary_langeron_list)
        table.bulk_insert(calculated_langeron_list)
        counter += 1
