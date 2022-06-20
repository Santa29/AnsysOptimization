# Update geometry
Model.Geometry.UpdateGeometryFromSource()

# Clear generated data and solve
Model.Analyses[0].ClearGeneratedData()
Model.Analyses[0].Solve()