# Create the material assignments list
material_polyester = ['Resin Polyester Assignment(Mechanical Model)', '', 'Fullfillment']
material_epoxy = ['E-Glass Assignment(Mechanical Model)', '', 'Epoxy']
material_steel = ['Structural Steel Assignment(Mechanical Model)', '', 'Antiflatter']
material_pps = ['PPS with 40% CF Assignment(Mechanical Model)', '', 'Composite']
material_assignments = [material_pps, material_steel, material_epoxy, material_polyester]

# Create the named selections list
ns_polyester = ['Fullfillment(Mechanical Model)', '']
ns_epoxy = ['Epoxy(Mechanical Model)', '']
ns_steel = ['Antiflatter(Mechanical Model)', '']
ns_pps = ['Composite(Mechanical Model)', '']
ns_pressure = ['Pressure(Mechanical Model)', '']
ns_fixed_support = ['Fixed Support(Mechanical Model)', '']
named_selections = [ns_pps, ns_polyester, ns_steel, ns_epoxy, ns_pressure, ns_fixed_support]

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

# Generate mesh
mesh = Model.Mesh
mesh.GenerateMesh()

# Find and fill Fixed Support boundary in both analyses
analysis_children_list = Model.Analyses[0].Children
for child in analysis_children_list:
    if 'Fixed Support' in child.Name:
        child.Location = ns_fixed_support[1]
analysis_children_list = Model.Analyses[1].Children
for child in analysis_children_list:
    if 'Fixed Support' in child.Name:
        child.Location = ns_fixed_support[1]
