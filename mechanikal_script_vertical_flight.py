'''NOTE : All workflows will not be recorded, as recording is under development.'''

location_list = {
    'Resin': Model.NamedSelections.Children[3],
    'Epoxy': Model.NamedSelections.Children[2],
    'Steel': Model.NamedSelections.Children[4],
    'PPS': Model.NamedSelections.Children[1]
}

assigment_list = [
    ('Resin', Model.Materials.Children[4]),
    ('Epoxy', Model.Materials.Children[5]),
    ('Steel', Model.Materials.Children[6]),
    ('PPS', Model.Materials.Children[7])
]

for value in assigment_list:
    value[1].Location = location_list[value[0]]
