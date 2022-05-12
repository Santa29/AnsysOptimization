

# Python Script, API Version = V19
ClearAll()
import math
import os

base_path = r'C:\Ansys projects\Lopast_helicopter\AnsysOptimization\scripts'
path = os.path.join(base_path, 'rc410.dat')

print(path)

#Get the profile lines from file
f = open(path, "r")
SCALE_FACTOR = 100
tmp = f.readlines()
f.close()
tmp = [line.rstrip() for line in tmp]
top_line = tmp[3:44]
top_line = [line.split() for line in top_line]
bottom_line = tmp[45:88]
bottom_line = [line.split() for line in bottom_line]
for el in top_line:
    el[0] = round(SCALE_FACTOR * float(el[0]), 2)
    el[1] = round(SCALE_FACTOR * float(el[1]), 2)
for el in bottom_line:
    el[0] = round(SCALE_FACTOR * float(el[0]), 2)
    el[1] = round(SCALE_FACTOR * float(el[1]), 2)
#EndBlock

# Set Sketch Plane
selection = Plane.PlaneXY
result = ViewHelper.SetSketchPlane(selection)
# EndBlock

# Set New Sketch
result = SketchHelper.StartConstraintSketching()
# EndBlock

# Sketch generate cycle
for i in range(10):
    # Sketch Spline
    points = List[Point2D]()
    for el in top_line:
        points.Add(Point2D.Create(MM(el[0]), MM(el[1])))
    result = SketchNurbs.CreateFrom2DPoints(False, points)
    # EndBlock

    # Sketch Spline
    points = List[Point2D]()
    for el in bottom_line:
        points.Add(Point2D.Create(MM(el[0]), MM(el[1])))
    result = SketchNurbs.CreateFrom2DPoints(False, points)
    # EndBlock

    # Solidify Sketch
    mode = InteractionMode.Solid
    result = ViewHelper.SetViewMode(mode)
    # EndBlock
#EndBlock

# Set Sketch Plane
sectionPlane = Plane.PlaneXY
result = ViewHelper.SetSketchPlane(sectionPlane, None)
# EndBlock

# Set New Sketch
result = SketchHelper.StartConstraintSketching()
# EndBlock

# Sketch Line
start = Point2D.Create(MM(Parameters.wall_length + SCALE_FACTOR * math.tan(math.radians(Parameters.wall_angle))),
MM(SCALE_FACTOR))
end = Point2D.Create(MM(Parameters.wall_length - SCALE_FACTOR * math.tan(math.radians(Parameters.wall_angle))),
MM(-SCALE_FACTOR))
result = SketchLine.Create(start, end)
# EndBlock

# Sketch Line
start = Point2D.Create(MM(Parameters.polymer_volume_coordinate), MM(SCALE_FACTOR))
end = Point2D.Create(MM(Parameters.polymer_volume_coordinate), MM(-SCALE_FACTOR))
result = SketchLine.Create(start, end)
# EndBlock

# Solidify Sketch
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

#Move bodies and split faces on it
bodies_list = BodySelection.Create([GetRootPart().Bodies[0],
    GetRootPart().Bodies[1],
    GetRootPart().Bodies[2],
    GetRootPart().Bodies[3],
    GetRootPart().Bodies[4],
    GetRootPart().Bodies[5],
    GetRootPart().Bodies[6],
    GetRootPart().Bodies[7],
    GetRootPart().Bodies[8],
    GetRootPart().Bodies[9]])

for i, body in enumerate(bodies_list):
    # Split Faces
    options = SplitFaceOptions()
    selection = FaceSelection.Create(GetRootPart().Bodies[i].Faces[0])
    cutter = Selection.Create(GetRootPart().Curves[0])
    result = SplitFace.ByCutter(selection, cutter, options)
    # EndBlock
    
    # Split Faces
    options = SplitFaceOptions()
    selection = FaceSelection.Create(GetRootPart().Bodies[i].Faces[0])
    cutter = Selection.Create(GetRootPart().Curves[1])
    result = SplitFace.ByCutter(selection, cutter, options)
    # EndBlock

    # Translate Along Z Handle
    selection = body
    direction = Direction.DirZ
    options = MoveOptions()
    result = Move.Translate(selection, direction, MM(100 * i), options)
    # EndBlock
    
    # Rotate About Z Handle
    selection = body
    anchorPoint = Move.GetAnchorPoint(selection)
    axis = Line.Create(anchorPoint, Direction.DirZ)
    options = MoveOptions()
    result = Move.Rotate(selection, axis, DEG(-0.5 * i), options)
    # EndBlock
#EndBlock

# Delete Selection
selection = Selection.Create(GetRootPart().Curves[0])
result = Delete.Execute(selection)
# EndBlock

# Delete Selection
selection = Selection.Create(GetRootPart().Curves[0])
result = Delete.Execute(selection)
# EndBlock

# Create Blend
selection = FaceSelection.Create([GetRootPart().Bodies[0].Faces[1],
    GetRootPart().Bodies[1].Faces[1],
    GetRootPart().Bodies[2].Faces[1],
    GetRootPart().Bodies[3].Faces[1],
    GetRootPart().Bodies[4].Faces[1],
    GetRootPart().Bodies[5].Faces[1],
    GetRootPart().Bodies[6].Faces[1],
    GetRootPart().Bodies[7].Faces[1],
    GetRootPart().Bodies[8].Faces[1],
    GetRootPart().Bodies[9].Faces[1]])
options = LoftOptions()
options.GeometryCommandOptions = GeometryCommandOptions()
result = Loft.Create(selection, None, options)
# EndBlock

# Create Blend
selection = FaceSelection.Create([GetRootPart().Bodies[0].Faces[0],
    GetRootPart().Bodies[1].Faces[0],
    GetRootPart().Bodies[2].Faces[0],
    GetRootPart().Bodies[3].Faces[0],
    GetRootPart().Bodies[4].Faces[0],
    GetRootPart().Bodies[5].Faces[0],
    GetRootPart().Bodies[6].Faces[0],
    GetRootPart().Bodies[7].Faces[0],
    GetRootPart().Bodies[8].Faces[0],
    GetRootPart().Bodies[9].Faces[0]])
options = LoftOptions()
options.GeometryCommandOptions = GeometryCommandOptions()
options.ExtrudeType = ExtrudeType.ForceIndependent
result = Loft.Create(selection, None, options)
# EndBlock


# Create Blend
selection = FaceSelection.Create([GetRootPart().Bodies[0].Faces[0],
    GetRootPart().Bodies[1].Faces[2],
    GetRootPart().Bodies[2].Faces[2],
    GetRootPart().Bodies[3].Faces[2],
    GetRootPart().Bodies[4].Faces[2],
    GetRootPart().Bodies[5].Faces[2],
    GetRootPart().Bodies[6].Faces[2],
    GetRootPart().Bodies[7].Faces[2],
    GetRootPart().Bodies[8].Faces[2],
    GetRootPart().Bodies[9].Faces[0]])
options = LoftOptions()
options.GeometryCommandOptions = GeometryCommandOptions()
options.ExtrudeType = ExtrudeType.ForceIndependent
result = Loft.Create(selection, None, options)
# EndBlock

# Delete Selection
selection = BodySelection.Create([GetRootPart().Bodies[7],
    GetRootPart().Bodies[0],
    GetRootPart().Bodies[1],
    GetRootPart().Bodies[2],
    GetRootPart().Bodies[3],
    GetRootPart().Bodies[4],
    GetRootPart().Bodies[5],
    GetRootPart().Bodies[6]])
result = Delete.Execute(selection)
# EndBlock

# 
result = Copy.ToClipboard(FaceSelection.Create([GetRootPart().Bodies[1].Faces[4],
    GetRootPart().Bodies[1].Faces[3],
    GetRootPart().Bodies[1].Faces[1]]))
# EndBlock

# Set Sketch Plane
selection = Plane.PlaneXY
result = ViewHelper.SetSketchPlane(selection)
# EndBlock

# Set New Sketch
result = SketchHelper.StartConstraintSketching()
# EndBlock

# Calculate the new spline, all points is perpendicular to the parent lines
points = List[Point2D]()
top_line_modifyed = []
top_line_new_points = []
# Get the modify massive of points which contains only points with y <= polymer volume coordinate
for el in top_line:
    if el[0] <= Parameters.polymer_volume_coordinate:
        top_line_modifyed.append(el)
# Start searching the new massive points
for i in range(1, len(top_line_modifyed) - 1):
    x_1 = top_line_modifyed[i][0]
    x_2 = top_line_modifyed[i+1][0]
    y_1 = top_line_modifyed[i][1]
    y_2 =  top_line_modifyed[i+1][1]
    x_center = (x_1 + x_2) / 2
    y_center = (y_1 +y_2) / 2
    b = (y_2 * x_1 - y_1 * x_2) / (x_1 - x_2)
    a = (y_1 - b) / x_1
    delta_l = Parameters.antiflatter_diam + 0.5
    delta_x = (delta_l ** 2 / (a ** 2 + 1)) ** 0.5
    print(delta_x, delta_l)
    delta_y = (delta_l ** 2 - delta_x ** 2) ** 0.5
    x_4 = x_center + delta_y
    y_4 = y_center - delta_x
    top_line_new_points.append([x_4, y_4])
# Get garantee distance
counter_top = len(top_line_new_points) - 1
if top_line_new_points[counter_top][0] > Parameters.polymer_volume_coordinate - Parameters.antiflatter_diam - 0.5:
    top_line_new_points[counter_top][0] = Parameters.polymer_volume_coordinate - Parameters.antiflatter_diam - 0.5
# Draw the new line
for el in top_line_new_points:
    points.Add(Point2D.Create(MM(el[0]), MM(el[1])))
result = SketchNurbs.CreateFrom2DPoints(False, points)
# EndBlock

# Calculate the new spline, all points is perpendicular to the parent lines
points = List[Point2D]()
bottom_line_modifyed = []
bottom_line_new_points = []
# Get the modify massive of points which contains only points with y <= polymer volume coordinate
for el in bottom_line:
    if el[0] <= Parameters.polymer_volume_coordinate:
        bottom_line_modifyed.append(el)
# Start searching the new massive points
for i in range(1, len(bottom_line_modifyed) - 1):
    x_1 = bottom_line_modifyed[i][0]
    x_2 = bottom_line_modifyed[i+1][0]
    y_1 = bottom_line_modifyed[i][1]
    y_2 =  bottom_line_modifyed[i+1][1]
    x_center = (x_1 + x_2) / 2
    y_center = (y_1 +y_2) / 2
    b = (y_2 * x_1 - y_1 * x_2) / (x_1 - x_2)
    a = (y_1 - b) / x_1
    delta_l = Parameters.antiflatter_diam + 0.5
    delta_x = (delta_l ** 2 / (a ** 2 + 1)) ** 0.5
    print(delta_x, delta_l)
    delta_y = (delta_l ** 2 - delta_x ** 2) ** 0.5
    x_4 = x_center + delta_y
    y_4 = y_center + delta_x
    bottom_line_new_points.append([x_4, y_4])
# Set the first point as sterting point of top_line massive
bottom_line_new_points[0] = top_line_new_points[0]
# Get garantee distance
counter_bottom = len(bottom_line_new_points) - 1
if bottom_line_new_points[counter_bottom][0] > Parameters.polymer_volume_coordinate - Parameters.antiflatter_diam - 0.5:
    bottom_line_new_points[counter_bottom][0] = Parameters.polymer_volume_coordinate - Parameters.antiflatter_diam - 0.5
# Draw the new line
for el in bottom_line_new_points:
    points.Add(Point2D.Create(MM(el[0]), MM(el[1])))
result = SketchNurbs.CreateFrom2DPoints(False, points)
# EndBlock

# Sketch Line
start = Point2D.Create(MM(bottom_line_new_points[counter_bottom][0]), MM(bottom_line_new_points[counter_bottom][1]))
end = Point2D.Create(MM(top_line_new_points[counter_top][0]), MM(top_line_new_points[counter_top][1]))
result = SketchLine.Create(start, end)

# Create coordinates dictionary
coord_dict = {
        0:(2, 0),
        1:(2, 1),
        2:(2, 2),
        3:(0, 0),
        4:(1, math.ceil(len(bottom_line_new_points))),
        5:(0, math.ceil(len(top_line_new_points))),
        6:(0, 2),
        7:(1, 2)
        }
# EndBlock

# Move the antiflatter to right position
if Parameters.value_to_calculate_antiflatter_center in coord_dict:
    constraint_1 = coord_dict[Parameters.value_to_calculate_antiflatter_center][0]
    constraint_2 = coord_dict[Parameters.value_to_calculate_antiflatter_center][1]
else:
    constraint_1 = coord_dict[0][0]
    constraint_2 = coord_dict[0][1]
    
# Sketch Circle
position = GetRootPart().DatumPlanes[0].Curves[constraint_1].GetChildren[ICurvePoint]()[constraint_2]
position_x, position_y, position_z = position.Position
origin = Point2D.Create(MM(position_x * 1000), MM(position_y * 1000))
result = SketchCircle.Create(origin, MM(Parameters.antiflatter_diam))
# EndBlock

# Delete Selection
selection = Selection.Create([GetRootPart().DatumPlanes[0].Curves[1],
    GetRootPart().DatumPlanes[0].Curves[2],
    GetRootPart().DatumPlanes[0].Curves[0]])
result = Delete.Execute(selection)
# EndBlock

# Solidify Sketch
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode)
# EndBlock

# Sweep 1 Face
selection = FaceSelection.Create(GetRootPart().Bodies[0].Faces[4])
trajectories = EdgeSelection.Create(GetRootPart().Bodies[0].Edges[6])
options = SweepCommandOptions()
options.ExtrudeType = ExtrudeType.ForceIndependent
options.Select = True
result = Sweep.Execute(selection, trajectories, options, None)
# EndBlock

# Create Datum Plane
selection = FaceSelection.Create(GetRootPart().Bodies[2].Faces[0])
result = DatumPlaneCreator.Create(selection, False, None)
# EndBlock

# Translate Along Z Handle
selection = Selection.Create(GetRootPart().DatumPlanes[0])
direction = Move.GetDirection(selection)
options = MoveOptions()
result = Move.Translate(selection, direction, MM(-(1100 - Parameters.antiflatter_length)), options)
# EndBlock

# Slice Bodies by Plane
selection = BodySelection.Create(GetRootPart().Bodies[3])
datum = Selection.Create(GetRootPart().DatumPlanes[0])
result = SplitBody.ByCutter(selection, datum)
# EndBlock

# Delete Objects
selection = BodySelection.Create(GetRootPart().Bodies[4])
result = Combine.RemoveRegions(selection)
# EndBlock

# Delete Selection
selection = Selection.Create(GetRootPart().DatumPlanes[0])
result = Delete.Execute(selection)
# EndBlock

# Intersect Bodies
targets = BodySelection.Create(GetRootPart().Bodies[0])
tools = BodySelection.Create(GetRootPart().Bodies[3])
options = MakeSolidsOptions()
result = Combine.Intersect(targets, tools, options)
# EndBlock

# Delete Objects
selection = BodySelection.Create(GetRootPart().Bodies[4])
result = Combine.RemoveRegions(selection)
# EndBlock

# Fix 2 Interferences
result = FixInterference.FindAndFix()
# EndBlock

# Delete Selection
selection = EdgeSelection.Create(GetRootPart().Bodies[0].Edges[8])
result = Delete.Execute(selection)
# EndBlock

# Copy to Clipboard
face_list_with_minor_bug = [GetRootPart().Bodies[1].Faces[4],
GetRootPart().Bodies[2].Faces[5],
GetRootPart().Bodies[0].Faces[1],
GetRootPart().Bodies[0].Faces[2],
GetRootPart().Bodies[2].Faces[3],
GetRootPart().Bodies[1].Faces[3],
GetRootPart().Bodies[0].Faces[8],
GetRootPart().Bodies[1].Faces[1],
GetRootPart().Bodies[2].Faces[1],
GetRootPart().Bodies[2].Faces[4]]
face_list_without_minor_bug = [GetRootPart().Bodies[1].Faces[4],
GetRootPart().Bodies[2].Faces[5],
GetRootPart().Bodies[0].Faces[1],
GetRootPart().Bodies[0].Faces[2],
GetRootPart().Bodies[2].Faces[3],
GetRootPart().Bodies[1].Faces[3],
GetRootPart().Bodies[0].Faces[7],
GetRootPart().Bodies[1].Faces[1],
GetRootPart().Bodies[2].Faces[1],
GetRootPart().Bodies[2].Faces[4]]
if len(GetRootPart().Bodies[0].Faces) == 9:
    result = Copy.ToClipboard(FaceSelection.Create(face_list_with_minor_bug))
else:
    result = Copy.ToClipboard(FaceSelection.Create(face_list_without_minor_bug))
# EndBlock

# Paste from Clipboard
result = Paste.FromClipboard()
# EndBlock

# Create Named Selection Group
primarySelection = FaceSelection.Create(GetRootPart().Bodies[5].Faces[0])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Langeron_wall")
# EndBlock

# Create Named Selection Group
primarySelection = BodySelection.Create(GetRootPart().Bodies[0])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Epoxy")
# EndBlock

# Create Named Selection Group
primarySelection = BodySelection.Create(GetRootPart().Bodies[1],
GetRootPart().Bodies[2])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Fullfillment")
# EndBlock

# Create Named Selection Group
primarySelection = FaceSelection.Create([GetRootPart().Bodies[1].Faces[3],
    GetRootPart().Bodies[2].Faces[3],
    GetRootPart().Bodies[0].Faces[2],
    GetRootPart().Bodies[0].Faces[1],
    GetRootPart().Bodies[2].Faces[5],
    GetRootPart().Bodies[1].Faces[4]])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Pressure")
# EndBlock

# Create Named Selection Group
primarySelection = FaceSelection.Create([GetRootPart().Bodies[0].Faces[4],
    GetRootPart().Bodies[0].Faces[3],
    GetRootPart().Bodies[2].Faces[0],
    GetRootPart().Bodies[1].Faces[0]])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Fixed Support")
# EndBlock

# Create Named Selection Group
primarySelection = BodySelection.Create(GetRootPart().Bodies[3])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Antiflatter")
# EndBlock

# Create Named Selection Group
primarySelection = BodySelection.Create(GetRootPart().Bodies[4],
GetRootPart().Bodies[5],
GetRootPart().Bodies[6])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Composite")
# EndBlock

# Create Named Selection Group
primarySelection = BodySelection.Create(GetRootPart().Bodies[4])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Shell")
# EndBlock

# Create Named Selection Group
primarySelection = BodySelection.Create(GetRootPart().Bodies[6],
GetRootPart().Bodies[5])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Langeron")
# EndBlock

# 
result = Midsurface.Convert(BodySelection.Create([GetRootPart().Bodies[4],
    GetRootPart().Bodies[5],
    GetRootPart().Bodies[6],
    GetRootPart().Bodies[7]]), MM(2))
# EndBlock