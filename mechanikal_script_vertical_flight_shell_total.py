# Create the material assignments list
material_polyester = ['Resin Polyester Assignment(ACP (Pre))', '', 'Fullfillment(ACP (Pre))']
material_epoxy = ['E-Glass Assignment(ACP (Pre))', '', 'Epoxy(ACP (Pre))']
material_steel = ['Structural Steel Assignment(ACP (Pre))', '', 'Antiflatter(ACP (Pre))']
material_pps = ['PPS with 40% CF Assignment(ACP (Pre))', '', 'Composite(ACP (Pre))']
material_assignments = [material_pps, material_steel, material_epoxy, material_polyester]

# Create the named selections list
ns_polyester = ['Fullfillment(ACP (Pre))', '']
ns_epoxy = ['Epoxy(ACP (Pre))', '']
ns_steel = ['Antiflatter(ACP (Pre))', '']
ns_pps = ['Composite(ACP (Pre))', '']
ns_fixed_support = ['Fixed Support(ACP (Pre))', '']
ns_pressure = ['Pressure(ACP (Pre))', '']
named_selections = [ns_pps, ns_polyester, ns_steel, ns_epoxy, ns_fixed_support, ns_pressure]

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
for body in Model.Geometry.Children:
    if body.Name == 'Thickness':
        body.Location = ns_pps[1]

# Generate mesh
mesh = Model.Mesh
mesh.GenerateMesh()

# Find and fill the remote point coordinates
remote_point = Model.RemotePoints.Children[0]
remote_point.Location = ns_pressure[1]

# Find and fill Fixed Support boundary condition and imported load
analysis_children_list = Model.Analyses[0].Children
for child in analysis_children_list:
    if child.Name == 'Fixed Support':
        child.Location = ns_fixed_support[1]
    elif 'Imported Load' in child.Name:
        child.Children[0].Location = ns_pressure[1]