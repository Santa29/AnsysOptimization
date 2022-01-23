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

from random import randint
import os
import sys

dir_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(dir_path, 'scripts', 'log.txt')
acp_pre_path = os.path.join(dir_path, 'scripts', 'acp_pre.py')
acp_post_path = os.path.join(dir_path, 'scripts', 'acp_post.py')
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
        system1 = GetSystem(Name=name)
        geometry1 = system1.GetContainer(ComponentName=component)
        geometry1.Edit(IsSpaceClaimGeometry=True)
        DSscript = open(script_path, "r")
        DSscriptcommand = DSscript.read()
        DSscript.close()
        geometry1.SendCommand(Command=DSscriptcommand, Language="Python")
        geometry1.Exit()
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


def put_values_into_algorithm():
    """This function put the new values to the optimization alhoritm"""
    f = open(r'C:\Users\1\Desktop\Work\Lopast_helicopter_13_10\Scripts\angles.txt', 'w')
    for i in range(randint(5, 20)):
        value = randint(0, 900) / 10
        f.write(str(value) + '\n')
    f.close()


# update_component('ACP-Pre', ('Setup', 'Geometry', 'Model', 'Results', 'Engineering Data'))
recreate_geometry('Geom-3', 'Geometry-5', geometry_script_path_vertical, 'Geometry update success', 'Geometry failed')
