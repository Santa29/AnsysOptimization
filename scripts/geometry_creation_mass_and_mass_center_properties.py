# Python Script, API Version = V19
import math
import os

base_path = r'C:\Ansys projects\Lopast_helicopter\AnsysOptimization\scripts'

density_steel = 7800
density_polyester = 1200
density_epoxy = 2600
density_pps = 1490

# Calculate mass properties
edge_list = [GetRootPart().Bodies[4].Edges[5],
    GetRootPart().Bodies[5].Edges[8],
    GetRootPart().Bodies[6].Edges[2],
    GetRootPart().Bodies[6].Edges[3],
    GetRootPart().Bodies[5].Edges[5],
    GetRootPart().Bodies[4].Edges[2],
    GetRootPart().Bodies[5].Edges[7]]
mass_and_coord_list = []
length = 0.0
body_list = [
        GetRootPart().Bodies[6].Faces[0],
        GetRootPart().Bodies[5].Faces[2],
        GetRootPart().Bodies[3].Faces[0],
        GetRootPart().Bodies[4].Faces[1],
        ]
for edge in edge_list:
    mass_and_coord_list.append([edge.Shape.Length * 0.0012 * density_pps, edge.EvalMid().Point])
mass_and_coord_list.append([body_list[0].Area * density_epoxy, body_list[0].EvalMid().Point])
mass_and_coord_list.append([body_list[1].Area * density_polyester, body_list[1].EvalMid().Point])
mass_and_coord_list.append([body_list[3].Area * density_polyester, body_list[1].EvalMid().Point])
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
mass_center = 0.03 -  tmp_mass / tmp_mass_sum
print(total_mass, mass_center)
# EndBlock

# Write results to txt file
path = os.path.join(base_path, 'mass_and_mass_center.txt')
f = open(path, 'w')
f.write(str(total_mass * 1000) + '\n' + str(mass_center))
f.close()