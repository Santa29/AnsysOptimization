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
os.chdir(current_path)

from models import database_creation
from models.my_orm import BaseModel
from models import langeron
from models import shell
from test import test_values_for_orm

dir_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(dir_path, 'scripts', 'log.txt')
acp_pre_path = os.path.join(dir_path, 'acp_pre.py')
acp_post_path = os.path.join(dir_path,  'acp_post.py')
geometry_script_path_vertical = os.path.join(dir_path, 'scripts', 'geometry_creation.py')
geometry_script_path_horizontal = os.path.join(dir_path, 'scripts', 'geometry_creation_rotate_bodies.py')
db_path = os.path.join(dir_path, 'experiment.db')


def logging(message):
    """This function create the new records in logging file"""
    f = open(log_path, 'a')
    f.write(message + '\n')
    f.close()


def update_acp_pre():
    """This function update the ACP pre window by running the acp_pre.py"""
    try:
        system1 = GetSystem(Name="ACP-Pre")
        setup1 = system1.GetContainer(ComponentName="Setup")
        setup1.RunScript(ScriptPath=acp_pre_path)
    except:
        logging('Update ACP failed')
    else:
        logging('Update ACP success')


def recreate_geometry(name, component, script_path, message_success, message_fail):
    try:
        system = GetSystem(Name=name)
        geometry = system.GetContainer(ComponentName=component)
        geometry.Edit(IsSpaceClaimGeometry=True)
        DSscript = open(script_path, "r")
        DSscriptcommand = DSscript.read()
        DSscript.close()
        geometry.SendCommand(Command=DSscriptcommand, Language="Python")
        # geometry.Exit()
    except:
        logging(message_fail)
    else:
        logging(message_success)


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
        Parameters.SetDesignPointsOutOfDate()
        system2 = GetSystem(Name="ACP-Post")
        results1 = system2.GetContainer(ComponentName="Results")
        system3 = GetSystem(Name="CFX")
        mesh1 = system3.GetContainer(ComponentName="Mesh")
        setup2 = system3.GetContainer(ComponentName="Setup")
        solution1 = system3.GetContainer(ComponentName="Solution")
        results2 = system3.GetContainer(ComponentName="Results")
        system4 = GetSystem(Name="SYS")
        model2 = system4.GetContainer(ComponentName="Model")
        setup3 = system4.GetContainer(ComponentName="Setup")
        solution2 = system4.GetContainer(ComponentName="Solution")
        results3 = system4.GetContainer(ComponentName="Results")
        Parameters.SetRetainedDesignPointDataInvalid(
            InvalidContainers=[engineeringData1, geometry1, model1, results1, setup1, mesh1, setup2, solution1,
                               results2, model2, setup3, solution2, results3])
        setupComponent1 = system1.GetComponent(Name="Setup")
        modelComponent1 = system4.GetComponent(Name="Model")
        setupComponent2 = system4.GetComponent(Name="Setup")
        solutionComponent1 = system4.GetComponent(Name="Solution")
        resultsComponent1 = system4.GetComponent(Name="Results")
        resultsComponent2 = system2.GetComponent(Name="Results")
        MarkComponentsOutOfDateForDps(
            Components=[setupComponent1, modelComponent1, setupComponent2, solutionComponent1, resultsComponent1,
                        resultsComponent2])
        Parameters.SetPartiallyRetainedDataInvalid(Containers=[setup1, model2, setup3, solution2, results3, results1])
        Update()
    except:
        logging('Update_failing')
    else:
        logging('Update success')


def update_acp_post():
    """This function get the values from ACP Post window by running the acp_post.py"""
    try:
        system1 = GetSystem(Name="ACP-Post")
        setup1 = system1.GetContainer(ComponentName="Results")
        setup1.RunScript(ScriptPath=acp_post_path)
    except:
        logging('Error when trying get the values from ACP')
    else:
        logging('Get the values from ACP success')


# update_component('ACP-Pre', ('Setup', 'Geometry', 'Model', 'Results', 'Engineering Data'))
# recreate_geometry('Geom', 'Geometry', geometry_script_path_vertical, 'Geometry update success', 'Geometry failed')
test_list = []
database_creation.create_table('experiment.sqlite')
for i in range(1):
    test_list.append(test_values_for_orm(model_type='Shell'))
a = BaseModel('shell')
a.bulk_insert(insert_list=test_list)
test_list = []
for i in range(1):
    test_list.append(test_values_for_orm(model_type='Langeron'))
b = BaseModel('langeron')
b.bulk_insert(insert_list=test_list)
a, b = b.execute_series(series_param='test_langeron'), a.execute_series(series_param='test_shell')

# Start the db test
objects_list_1 = []
objects_list_2 = []
for el in a.fetchall():
    objects_list_1.append(langeron.LangeronModel(el))
for el in b.fetchall():
    objects_list_2.append(shell.ShellModel(el))
tmp1 = objects_list_1[0]
print(tmp1.shell_angles)
tmp1.update_values()
tmp2 = objects_list_2[0]
print(tmp2.shell_angles)
tmp2.update_values()
