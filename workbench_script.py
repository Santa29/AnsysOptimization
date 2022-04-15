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


def get_parameter(param_id):
    parameter = Parameters.GetParameter(Name=param_id)
    value = str(parameter.Value).split(' ')
    return value[0]


def update_project():
    """This function update the project in Workbench window"""
    try:
        # recreate_geometry('Geom 3',
        #                   'Geometry 5',
        #                   ('P13', '30'),
        #                   'geometry recreation success in vertical',
        #                   'geometry recreation fail in vertical')
        DSscript = open(r"C:\Ansys projects\Lopast_helicopter\AnsysOptimization\workbench_script.py", "r")
        DSscriptcommand = DSscript.read()
        DSscript.close()
        # Send the command
        model1.SendCommand(Command=DSscriptcommand)
        model1.Exit()
        run_script('ACP-Pre 1', 'Setup 3', acp_pre_path, 'ACP-pre-hor successful updated', 'ACP-pre failed to update')
        run_script('ACP-Pre', 'Setup 2', acp_pre_path, 'ACP-pre-vert successful updated', 'ACP-pre failed to update')
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

logging('Start working')

a = BaseModel('langeron')
current_object_list = []
for el in a.select_by_series('need_calculate'):
    current_object_list.append(WBLangeronModel(el))

for i, el in enumerate(current_object_list):
    if i != 1:
        continue
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
    change_parameter('P66', el.langeron_integer_code[0:8])
    change_parameter('P67', el.langeron_integer_code[8:])
    change_parameter('P36', el.langeron_integer_code[0:8])
    change_parameter('P37', el.langeron_integer_code[8:])
    change_parameter('P42', el.langeron_integer_code[0:8])
    change_parameter('P43', el.langeron_integer_code[8:])
    change_parameter('P45', el.langeron_integer_code[0:8])
    change_parameter('P46', el.langeron_integer_code[8:])
    update_project()
    # Read safety factors
    el.value_vertical = float(get_parameter('P65'))
    el.value_horizontal = float(get_parameter('P64'))
    # Read and build correct modal string
    tmp = get_parameter('P53') + ', ' + get_parameter('P54') + ', ' + get_parameter('P55') + ', ' + get_parameter('P56')
    tmp += ', ' + get_parameter('P57') + ', ' + get_parameter('P58')
    el.value_spectrum_modal_min = tmp
    tmp = get_parameter('P76') + ', ' + get_parameter('P77') + ', ' + get_parameter('P78') + ', ' + get_parameter('P79')
    tmp += ', ' + get_parameter('P80') + ', ' + get_parameter('P81')
    el.value_spectrum_modal_max = tmp
    # Read wing mass
    el.mass = round(float(get_parameter('P60')) * 1000)
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
    # Calculate and read the mass_center
    tmp_x = float(get_parameter('P82'))
    tmp_y = float(get_parameter('P83'))
    tmp = ((tmp_x - 25) ** 2 + ((tmp_y - 2) ** 2) ** 0.5)
    el.mass_center = tmp
    el.update_values()

logging('finish work')
