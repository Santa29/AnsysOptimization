"""
Order to set the calculation begin:
1.Run start_calculation()

How start_calculation actually works:
1.From test_script.py run update_acp_pre
2.update_acp_pre call acp_pre.py
3.From test_script.py run update_project
4.From test_script.py run update_acp_post
5.update_acp_post call acp_post.py
"""

import os
import sys

current_path = os.path.dirname(__file__)
sys.path.append(current_path)
sys.path.append(os.path.join(current_path, 'models'))
try:
    os.chdir(current_path)
except:
    pass

from models import database_creation
from models.my_orm import BaseModel
from models import langeron
from models import shell
from test import test_values_for_orm

dir_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(dir_path, 'scripts', 'log.txt')
acp_pre_path = os.path.join(dir_path, 'acp_pre.py')
geometry_script_path_vertical = os.path.join(dir_path, 'scripts', 'geometry_creation.py')
geometry_script_path_horizontal = os.path.join(dir_path, 'scripts', 'geometry_creation_rotate_bodies.py')
db_path = os.path.join(dir_path, 'experiment.sqlite')


def logging(message):
    """This function create the new records in logging file"""
    f = open(log_path, 'a')
    f.write(message + '\n')
    f.close()


def update_component(name, container_list):
    """This function update current component"""
    system = GetSystem(Name=name)
    invalid_containers = []
    for container in container_list:
        invalid_containers.append(system.GetContainer(ComponentName=container))
    Parameters.SetRetainedDesignPointDataInvalid(InvalaidContainers=invalid_containers)
    Update()


def run_script(name, component, script_path, message_success, message_fail):
    """This function run script in the current module with the current name"""
    try:
        system1 = GetSystem(Name=name)
        setup1 = system1.GetContainer(ComponentName=component)
        setup1.RunScript(ScriptPath=script_path)
    except:
        logging(message_fail)
    else:
        logging(message_success)


def update_project():
    """This function update the project in Workbench window"""
    try:
        update_component('ACP-Pre', ('Setup', 'Geometry', 'Model', 'Results', 'Engineering Data'))
        run_script('ACP-pre', 'Setup 2', acp_pre_path, 'ACP-pre successful updated', 'ACP-pre failed to update')
        run_script('ACP-Post', 'Results', acp_post_path, 'Get the values from ACP success', 'Error when trying get '
                                                                                            'the values from ACP')
        Update()
    except:
        logging('Update_failing')
    else:
        logging('Update success')


def create_integer_code(field):
    angles_range = [-89.0]
    step = 180 / 64
    for i in range(1, 64):
        angles_range.append(angles_range[i - 1] + step)
    result = ''
    for angle in field.split(', '):
        for i, el in enumerate(angles_range):
            if float(angle) == el:
                result += str(i + 11)
    if len(result) <= 8:
        return result
    else:
        return result[0:8], result[8:]


def split_integer_id_to_list(integer_id):
    if len(integer_id) <= 8:
        tmp = []
        for i in range(0, len(integer_id), 2):
            tmp.append(int(integer_id[i:i + 2]))
        return tmp
    else:
        tmp_1, tmp_2 = [], []
        for i in range(0, len(integer_id), 2):
            if i < 8:
                tmp_1.append(int(integer_id[i:i + 2]))
            else:
                tmp_2.append(int(integer_id[i:i + 2]))
        return tmp_1 + tmp_2


def simple_generation():
    test_list = []
    for i in range(20):
        test_list.append(test_values_for_orm(model_type='Shell'))
    a = BaseModel('shell')
    a.bulk_insert(insert_list=test_list)
    for i in range(20):
        test_list.append(test_values_for_orm(model_type='Langeron'))
    test_list = []
    b = BaseModel('langeron')
    b.bulk_insert(insert_list=test_list)


# update_component('ACP-Pre', ('Setup', 'Geometry', 'Model', 'Results', 'Engineering Data'))
# recreate_geometry('Geom', 'Geometry', geometry_script_path_vertical, 'Geometry update success', 'Geometry failed')
database_creation.create_table('experiment.sqlite')

a = BaseModel('shell')
b = BaseModel('langeron')
a, b = b.execute_series(series_param='test_langeron'), a.execute_series(series_param='test_shell')

# Start the db test
objects_list_1 = []
objects_list_2 = []
for el in a.fetchall():
    objects_list_1.append(langeron.LangeronModel(el))
for el in b.fetchall():
    objects_list_2.append(shell.ShellModel(el))
tmp1 = objects_list_1[0]
tmp1.update_values()
tmp2 = objects_list_2[0]
tmp2.update_values()
value_1 = create_integer_code(tmp1.shell_angles)
value_1 = split_integer_id_to_list(value_1)
value_2, value_3 = create_integer_code(getattr(tmp1, 'langeron_angles'))
value_2 = split_integer_id_to_list(value_2 + value_3)

print(value_1, value_2)
print(tmp1.shell_integer_code)
print(tmp1.bytestring)
