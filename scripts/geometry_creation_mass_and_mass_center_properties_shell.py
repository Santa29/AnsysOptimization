# Python Script, API Version = V19
import math
import os

base_path = r'C:\Ansys projects\Lopast_helicopter\AnsysOptimization\scripts'

density_steel = 7800
density_polyester = 1200
density_epoxy = 2600
density_pps = 1490

# Calculate mass properties
edge_list = [GetRootPart().Bodies[4].Edges[0],
    GetRootPart().Bodies[4].Edges[4],
    GetRootPart().Bodies[3].Edges[7],
    GetRootPart().Bodies[3].Edges[11],
    GetRootPart().Bodies[3].Edges[0],
    GetRootPart().Bodies[3].Edges[4]]
mass_and_coord_list = []
length = 0.0
body_list = [
        GetRootPart().Bodies[0].Faces[4],
        GetRootPart().Bodies[1].Faces[0],
        GetRootPart().Bodies[0].Faces[3],
        ]
for edge in edge_list:
    mass_and_coord_list.append([edge.Shape.Length * 0.0012 * density_pps, edge.EvalMid().Point])
mass_and_coord_list.append([body_list[0].Area * density_epoxy, body_list[0].EvalMid().Point])
mass_and_coord_list.append([body_list[1].Area * density_polyester, body_list[1].EvalMid().Point])
mass_and_coord_list.append([body_list[2].Area * density_steel, body_list[2].EvalMid().Point])
total_mass = 0.0
for el in mass_and_coord_list:
    total_mass += el[0] * 0.9
total_mass -= body_list[2].Area * density_steel * Parameters.antiflatter_length / 1000
for body in body_list:
    total_mass += body.Area * density_pps * 0.0012
tmp_mass = 0
tmp_mass_sum = 0
for el in mass_and_coord_list:
    tmp_mass += el[1][0] * el[0]
    tmp_mass_sum += el[0]
mass_center = 0.03 - tmp_mass / tmp_mass_sum
print(total_mass, mass_center)
# EndBlock

# Write results to txt file
path = os.path.join(base_path, 'mass_and_mass_center.txt')
f = open(path, 'w')
f.write(str(total_mass * 1000) + '\n' + str(mass_center))
f.close()