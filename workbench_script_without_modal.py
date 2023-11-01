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
from models.wb_ansys_langeron import WBLangeronModel
from models.shell import ShellModel

dir_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(dir_path, 'scripts', 'log.txt')
acp_pre_path = os.path.join(dir_path, 'acp_pre.py')
geometry_script_path_vertical = os.path.join(dir_path, 'scripts', 'geometry_creation.py')
geometry_script_path_horizontal = os.path.join(dir_path, 'scripts', 'geometry_creation_rotate_bodies.py')
db_path = os.path.join(dir_path, 'experiment.sqlite')
mass_and_mass_center_file_path = os.path.join(dir_path, 'scripts', 'mass_and_mass_center.txt')


def logging(message):
    """This function create the new records in logging file"""
    f = open(log_path, 'a')
    f.write(message + '\n')
    f.close()


def update_component(system_name, container_name, message_success, message_fail):
    """
    This function update current component
    params:
    system_name: str -> name of updating component from workbench tree
    message_success: str -> success message to log file
    message_fail: str -> fail message to log file
    """
    system = GetSystem(Name=system_name)
    container = system.GetComponent(Name=container_name)
    try:
        container.Update(AllDependencies=True)
        logging(message_success)
    except:
        logging(message_fail)


def run_script(name, component, script_path, message_success, message_fail):
    """This function run script in the current module with the current name"""
    try:
        system1 = GetSystem(Name=name)
        setup1 = system1.GetContainer(ComponentName=component)
        setup1.Refresh()
        # setup1.StartACP(ACPMode='pre')
        setup1.RunScript(ScriptPath=script_path)
        setup1.Update(AllDependencies=True)
        # setup1.ExitACP(Save=True)
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


def get_parameter(param_id):
    """
    Get the numerical value of current parameter
    params: param_id: str -> string with name of current parameter
    output: float -> float value of current parameter
    """
    parameter = Parameters.GetParameter(Name=param_id)
    value = str(parameter.Value).split(' ')
    return value[0]


def update_project():
    """This function update the project in Workbench window"""
    # !!! Start update vertical flight !!!
    update_component('Geom 3', 'Geometry', 'Update geometry success', 'Update geometry failed')
    update_mechanical_component(
        r'C:\Ansys projects\Lopast_helicopter\AnsysOptimization\scripts\geometry_creation_mass_and_mass_center_properties.py',
        'Update mechanical component success',
        'Update mechanical component failed',
        'Geom 3',
        'Geometry',
        mode='geometry'
    )
    # Start update model component in Acp-pre
    update_mechanical_component(
        r'C:\Ansys projects\Lopast_helicopter\AnsysOptimization\mechanikal_script_base.py',
        'Update mechanical component success',
        'Update mechanical component failed',
        'ACP-Pre',
        'Model'
    )
    # Start update setup component in ACP-pre
    run_script('ACP-Pre', 'Setup', acp_pre_path, 'ACP-pre-vert successful updated', 'ACP-pre failed to update')
    # Start update model component in static structural
    update_mechanical_component(
        r'C:\Ansys projects\Lopast_helicopter\AnsysOptimization\mechanikal_script_horizontal_flight_total.py',
        'Update total mechanical component success',
        'Update total mechanical component failed',
        'SYS',
        'Model'
    )
    update_mechanical_component(
        r'C:\Ansys projects\Lopast_helicopter\AnsysOptimization\mechanikal_script_solution_static.py',
        'Update solution mechanical component success',
        'Update solution mechanical component failed',
        'SYS',
        'Model',
        mode='setup'
    )
    # !!! Start update horizontal flight !!!
    update_component('Geom 2', 'Geometry', 'Update geometry success', 'Update geometry failed')
    # Start update model component in Acp-pre
    update_mechanical_component(
        r'C:\Ansys projects\Lopast_helicopter\AnsysOptimization\mechanikal_script_base.py',
        'Update mechanical component success',
        'Update mechanical component failed',
        'ACP-Pre 1',
        'Model'
    )
    # Start update setup component in ACP-pre
    run_script('ACP-Pre 1', 'Setup', acp_pre_path, 'ACP-pre-hor successful updated', 'ACP-pre failed to update')
    # Start update component model in static structural
    update_mechanical_component(
        r'C:\Ansys projects\Lopast_helicopter\AnsysOptimization\mechanikal_script_horizontal_flight_total.py',
        'Update total mechanical component success',
        'Update total mechanical component failed',
        'SYS 1',
        'Model'
    )
    update_mechanical_component(
        r'C:\Ansys projects\Lopast_helicopter\AnsysOptimization\mechanikal_script_solution_static.py',
        'Update total mechanical component success',
        'Update total mechanical component failed',
        'SYS 1',
        'Model',
        mode='setup'
    )
    Update()


def update_mechanical_component(script_path, message_success, message_fail, system_name, model_name, mode='model'):
    """
    This function update the model component in workbench script tree with the corresponding python script to avoid
    errors with material assignment.
    params:
    script_path: str -> path to the script in r'' form
    message_success: str -> success message to log file
    message_fail: str -> fail message to log file
    system_name: str -> name of updating system, from workbench project tree
    model_name: str -> name of updating component, from workbench project tree
    mode: str -> mode of function behaviour. May be "geometry", "model" (by default), "setup".
    """
    system = GetSystem(Name=system_name)
    container = system.GetContainer(ComponentName=model_name)
    container.Refresh()
    DSscript = open(script_path, 'r')
    DSscriptCommand = DSscript.read()
    DSscript.close()
    if mode == 'geometry':
        container.Edit(IsSpaceClaimGeometry=True, Interactive=False)
    else:
        container.Edit(Interactive=False)
    try:
        container.SendCommand(Language='Python', Command=DSscriptCommand)
        logging(message_success)
    except:
        logging(message_fail)
    if mode == 'geometry':
        container.Exit()
    else:
        container.Close()
    if mode != 'geometry':
        model_component = system.GetComponent(Name=model_name)
        model_component.Update(AllDependencies=True)
    if mode == 'setup':
        model_component = system.GetComponent(Name='Setup')
        model_component.Update(AllDependencies=True)


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


def read_mass_and_mass_center_properties():
    f = open(mass_and_mass_center_file_path, 'r')
    mass, mass_center = f.read().split()
    f.close()
    return mass, mass_center


database_creation.create_table('experiment.sqlite')

logging('Start working')

a = BaseModel('langeron')
current_object_list = []
for el in a.select_by_series('need_calculate'):
    current_object_list.append(WBLangeronModel(el))

for i, el in enumerate(current_object_list):
    # Change parameters for mechanical
    change_parameter('P13', str(el.wall_length))
    change_parameter('P14', str(el.wall_angle))
    change_parameter('P15', str(el.antiflatter_value))
    change_parameter('P16', str(el.antiflatter_diam))
    change_parameter('P17', str(el.polymer_volume_coordinate))
    change_parameter('P18', str(el.antiflatter_length))
    change_parameter('P19', str(el.wall_length))
    change_parameter('P20', str(el.wall_angle))
    change_parameter('P21', str(el.antiflatter_value))
    change_parameter('P22', str(el.antiflatter_diam))
    change_parameter('P23', str(el.polymer_volume_coordinate))
    change_parameter('P24', str(el.antiflatter_length))
    # Calculate Number of layers to correct run the acp=pre script
    number_of_layers = str(int(len(el.shell_integer_code) / 2)) + str(int(len(el.langeron_integer_code) / 2)) * 2
    # Change parameters to use them in acp-pre script
    change_parameter('P39', number_of_layers)
    change_parameter('P41', number_of_layers)
    change_parameter('P35', el.shell_integer_code)
    change_parameter('P44', el.shell_integer_code)
    change_parameter('P84', el.langeron_integer_code[0:8])
    if len(el.shell_integer_code) / 2 >= 4:
        change_parameter('P85', el.langeron_integer_code[8:])
    else:
        change_parameter('P85', '0')
    change_parameter('P36', el.langeron_integer_code[0:8])
    if len(el.shell_integer_code) / 2 >= 4:
        change_parameter('P37', el.langeron_integer_code[8:])
    else:
        change_parameter('P37', '0')
    change_parameter('P42', el.langeron_integer_code[0:8])
    if len(el.shell_integer_code) / 2 >= 4:
        change_parameter('P43', el.langeron_integer_code[8:])
    else:
        change_parameter('P43', '0')
    change_parameter('P45', el.langeron_integer_code[0:8])
    if len(el.shell_integer_code) / 2 >= 4:
        change_parameter('P46', el.langeron_integer_code[8:])
    else:
        change_parameter('P46', '0')
    update_project()
    # Read safety factors
    el.value_vertical = float(get_parameter('P65'))
    el.value_horizontal = float(get_parameter('P64'))
    # Read and build correct modal string
    tmp = '29, 70, 85, 160, 300, 370'
    el.value_spectrum_modal_min = tmp
    tmp = '35, 75, 130, 260, 380, 440'
    el.value_spectrum_modal_max = tmp
    # Read wing mass
    el.mass, el.mass_center = read_mass_and_mass_center_properties()
    # Calculate and read tip_flap
    max_deformation_x = max((float(get_parameter('P61')), float(get_parameter('P68'))))
    max_deformation_y = max((float(get_parameter('P74')), float(get_parameter('P75'))))
    tmp1 = (max_deformation_x ** 2 + max_deformation_y ** 2) ** 0.5
    max_deformation_x = max((float(get_parameter('P59')), float(get_parameter('P72'))))
    max_deformation_y = max((float(get_parameter('P71')), float(get_parameter('P73'))))
    tmp2 = (max_deformation_x ** 2 + max_deformation_y ** 2) ** 0.5
    el.tip_flap = max(tmp1, tmp2)
    # Calculate and read the twist_tip
    el.twist_tip = max((float(get_parameter('P69')), float(get_parameter('P70'))))
    el.series = 'calculated'
    el.update_values()

logging('finish work')