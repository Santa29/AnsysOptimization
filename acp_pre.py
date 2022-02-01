import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models import langeron
from models import shell
from models.my_orm import ShellTable, LangeronTable


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


def connect_db_and_build_model(current_id, model='langeron'):
    if model == 'langeron':
        return LangeronTable.objects.select_by_id(current_id)
    elif model == 'shell':
        return ShellTable.objects.select_by_id(current_id)
    else:
        raise ValueError


def model_choice(current_id, model='langeron'):
    temp = connect_db_and_build_model(current_id)
    temp = temp.fetchall()
    if model == 'langeron':
        return langeron.LangeronModel(temp)
    elif model == 'shell':
        return shell.ShellModel(temp)
    else:
        raise ValueError


wall_angles = []
langeron_angles = []
shell_angles = []

model_id = db.models['ACP Model'].selection.set([db.models['ACP Model'].parameters['Fabric.1.area_price']])
model_type = db.models['ACP Model'].selection.set([db.models['ACP Model'].parameters['Fabric.2.area_price']])
if model_type:
    current_model = 'shell'
else:
    current_model = 'langeron'
db.models['ACP Model'].update()
