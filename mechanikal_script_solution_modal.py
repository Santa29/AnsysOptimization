# Update geometry
Model.Geometry.UpdateGeometryFromSource()

# Clear generated data and solve
Model.Analyses[0].ClearGeneratedData()
Model.Analyses[0].Solve()
Model.Analyses[1].ClearGeneratedData()
Model.Analyses[1].Solve()
