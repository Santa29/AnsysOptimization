Model.Materials.Children[4].Location = Model.NamedSelections.Children[2]
Model.Materials.Children[5].Location = Model.NamedSelections.Children[1]
Model.Materials.Children[6].Location = Model.NamedSelections.Children[5]
Model.Materials.Children[7].Location = Model.NamedSelections.Children[6]

# Start finding and setting the thinkness of plane bodies from named selection Composite
bodies_selection_list = Model.NamedSelections.Children[6].Location
bodies_id_list = bodies_selection_list.Entities

for body in bodies_id_list:
    body.Thickness = 2
