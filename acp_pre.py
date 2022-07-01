def send_data_to_stackups(angles, model='langeron'):
    if model == 'langeron':
        tmp_1, tmp_2, tmp_3 = angles
        build_stackup(tmp_1, 'Langeron')
        build_stackup(tmp_2, 'Langeron_wall')
        build_stackup(tmp_3, 'Shell')
    elif model == 'shell':
        build_stackup(angles, 'Shell')
    else:
        raise ValueError


def build_stackup(angles, stackup_name):
    db.models['ACP Model'].material_data.stackups[stackup_name].fabrics = [
        (db.models['ACP Model'].material_data.fabrics['Fabric.1'], float(angle)) for angle in angles]


def create_plies(ply_name, stackup_name):
    db.models['ACP Model'].modeling_groups['ModelingGroup.1'].plies[ply_name].ply_material = \
    db.models['ACP Model'].material_data.stackups[stackup_name]


def read_number_of_layers(layers_id, model='langeron'):
    if model == 'langeron':
        shell_angles_count = int(layers_id[0])
        langeron_angles_count = int(layers_id[1])
        langeron_wall_angles_count = int(layers_id[2])
        return shell_angles_count, langeron_angles_count, langeron_wall_angles_count
    elif model == 'shell':
        shell_angles_count = int(layers_id[0])
        return shell_angles_count
    else:
        print('Wrong input')


def parameter_value(param_name):
    return db.models['ACP Model'].parameters[param_name].value


def decode_angles_list(value):
    integer_code = str(value)
    tmp = []
    angles = []
    counter = int(len(integer_code) / 2)
    for j in range(0, counter * 2, 2):
        integer_value = integer_code[j:j + 2]
        tmp.append(int(integer_value))
    for el in tmp:
        angles.append(ANGLES_LIST[el - 10])
    return angles


def append_encoding_values_to_list(list_name, set_name):
    for el in decode_angles_list(parameter_value(set_name)):
        list_name.append(el)


def create_orientation_lists(
        shell_angles_set='',
        langeron_set_1='',
        langeron_set_2='',
        langeron_wall_set_1='',
        langeron_wall_set_2='',
        model_type='langeron'):
    if model_type == 'langeron':
        shell_list = []
        langeron_list = []
        langeron_wall_list = []
        append_encoding_values_to_list(shell_list, shell_angles_set)
        append_encoding_values_to_list(langeron_list, langeron_set_1)
        append_encoding_values_to_list(langeron_list, langeron_set_2)
        append_encoding_values_to_list(langeron_wall_list, langeron_wall_set_1)
        append_encoding_values_to_list(langeron_wall_list, langeron_wall_set_2)
        return shell_list, langeron_list, langeron_wall_list
    elif model_type == 'shell':
        shell_list = []
        append_encoding_values_to_list(shell_list, shell_angles_set)
        return shell_list


# Get the new geometry
db.models['ACP Model'].update()

# Prepare the angles lists
wall_angles = []
langeron_angles = []
shell_angles = []

# Prepare the global values to decode input parameters
ANGLES_LIST = [-89.0]
STEP = 180 / 64
for i in range(1, 64):
    ANGLES_LIST.append(ANGLES_LIST[i - 1] + STEP)

# Read the current model type and number of layers
number_of_layers = str(parameter_value('Number of layers'))
model_type = parameter_value('Model type')
if model_type == 1:
    current_model = 'shell'
else:
    current_model = 'langeron'

# Create the angles list depends on model type
shell_layer_number, langeron_layer_number, langeron_wall_number = read_number_of_layers(number_of_layers, current_model)
if current_model == "langeron":
    shell_angles, langeron_angles, wall_angles = create_orientation_lists(
        shell_angles_set='Shell_set',
        langeron_set_1='Langeron_set_1',
        langeron_set_2='Langeron_set_2',
        langeron_wall_set_1='Langeron_wall_set_1',
        langeron_wall_set_2='Langeron_wall_set_2',
        model_type=current_model
    )
else:
    shell_angles = create_orientation_lists(shell_angles_set=parameter_value('Shell set'), model_type=current_model)

# Create stackups
build_stackup(shell_angles, 'Shell')
build_stackup(langeron_angles, 'Langeron')
build_stackup(wall_angles, 'Langeron_wall')

# Create plies
create_plies('Langeron', 'Langeron')
create_plies('Shell', 'Shell')
create_plies('Langeron_wall', 'Langeron_wall')

# Update project
db.models['ACP Model'].update()
