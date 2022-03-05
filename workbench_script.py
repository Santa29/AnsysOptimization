"""
Order to set the calculation begin:
1.Run start_calculation()

How start_calculation actually works:
1.From workbench_script.py run update_acp_pre
2.update_acp_pre call acp_pre.py
3.From workbench_script.py run update_project
4.From workbench_script.py run update_acp_post
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
from models.langeron import LangeronModel
from models.shell import ShellModel

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
        system1 = GetSystem(Name="Geom 3")
        geometry1 = system1.GetContainer(ComponentName="Geometry")
        geometry1.Edit(IsSpaceClaimGeometry=True)
        setup1.RunScript(ScriptPath=script_path)
        geometry1.Exit()
    except:
        logging(message_fail)
    else:
        logging(message_success)


def recreate_geometry(name, component, parameters_list, message_success, message_fail):
    """This function run script in the current module with the current name"""
    try:
        system = GetSystem(Name=name)
        geometry = system.GetContainer(ComponentName=component)
        for element_id, value in parameters_list:
            change_parameter(element_id, value)
        geometry.Edit(IsSpaceClaimGeometry=True)
        geometry.Exit()
    except:
        logging(message_fail)
    else:
        logging(message_success)


def change_parameter(param_id, value):
    designPoint1 = Parameters.GetDesignPoint(Name="0")
    parameter1 = Parameters.GetParameter(Name=param_id)
    designPoint1.SetParameterExpression(
        Parameter=parameter1,
        Expression=value)


def update_project():
    """This function update the project in Workbench window"""
    try:
        recreate_geometry('Geom 3',
                          'Geometry 5',
                          ('P13', '30'),
                          'geometry recreation success in vertical',
                          'geometry recreation fail in vertical')

        recreate_geometry('Geom 2',
                          'Geometry 4',
                          ('P19', '30'),
                          'geometry recreation success in vertical',
                          'geometry recreation fail in vertical')
        run_script('ACP-pre-1', 'Setup 3', acp_pre_path, 'ACP-pre-hor successful updated', 'ACP-pre failed to update')
        run_script('ACP-pre', 'Setup 2', acp_pre_path, 'ACP-pre-vert successful updated', 'ACP-pre failed to update')
        Update()
    except:
        logging('Update_failing')
    else:
        logging('Update success')


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


database_creation.create_table('experiment.sqlite')

a = BaseModel('langeron')
current_object_list = []
for i in range(1, 21):
    temp = a.select_by_id(i).fetchall()
    current_object_list.append(LangeronModel(temp))

for el in current_object_list:
    print(el.__getattribute__('shell_angles'))
print(current_object_list)
# update_project()
