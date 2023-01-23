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


def search_duplicate_values():
    """
    This function search duplicate values throw all previous calculated models. If model already calculated,
    this function change series status of the current duplicate.
    """
    tmp_1 = table.select_by_series('need_calculate')
    tmp_2 = table.select_by_series('calculated')
    current_object_list = []
    search_list = []
    for langeron in tmp_1:
        current_object_list.append(LangeronModel(langeron))
    for langeron in tmp_2:
        search_list.append(LangeronModel(langeron))
    for elem in search_list:
        elem.prepare_to_wb()
        elem.series = 'calculated'
        elem.update_values()
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
