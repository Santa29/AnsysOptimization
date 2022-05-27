# Create the material assignments list
material_polyester = ['Resin Polyester Assignment', '', 'Fullfillment']
material_epoxy = ['E-Glass Assignment', '', 'Epoxy']
material_steel = ['Structural Steel Assignment', '', 'Antiflatter']
material_pps = ['PPS with 40% CF Assignment', '', 'Composite']
material_assignments = [material_pps, material_steel, material_epoxy, material_polyester]

# Create the named selections list
ns_polyester = ['Fullfillment', '']
ns_epoxy = ['Epoxy', '']
ns_steel = ['Antiflatter', '']
ns_pps = ['Composite', '']
ns_langeron_wall = ['Langeron_wall', '']
named_selections = [ns_pps, ns_polyester, ns_steel, ns_epoxy, ns_langeron_wall]

# Update geometry
Model.Geometry.UpdateGeometryFromSource()

# Fill the material assignment list with actual data
for material in Model.Materials.Children:
    for assignment in material_assignments:
        if material.Name == assignment[0]:
            assignment[1] = material

# Fill the named selections list with actual data
for ns in Model.NamedSelections.Children:
    for selection in named_selections:
        if ns.Name == selection[0]:
            selection[1] = ns

# Compare the assignments to named selections:
for assignment in material_assignments:
    for selection in named_selections:
        if assignment[2] == selection[0]:
            assignment[1].Location = selection[1]

# Start finding and setting the thinkness of plane bodies from named selection Composite
current_selection = ns_pps[1].Location
bodies_id_list = current_selection.Entities

for body in bodies_id_list:
    body.Thickness = 2

# Generate mesh
mesh = Model.Mesh
mesh.GenerateMesh()

# Find and fill the remote point coordinates
remote_point = Model.RemotePoints.Children[0]
remote_point.Location = ns_langeron_wall[1]
