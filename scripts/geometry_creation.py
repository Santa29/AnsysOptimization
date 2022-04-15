






















# Python Script, API Version = V19
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
start = Point2D.Create(MM(Parameters.wall_length + SCALE_FACTOR * math.tan(Parameters.wall_angle)),
MM(SCALE_FACTOR))
end = Point2D.Create(MM(Parameters.wall_length - SCALE_FACTOR * math.tan(Parameters.wall_angle)),
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
 
# Set Sketch Plane
sectionPlane = Plane.PlaneZX
result = ViewHelper.SetSketchPlane(sectionPlane)
# EndBlock

# Set New Sketch
result = SketchHelper.StartConstraintSketching()
# EndBlock

# Sketch Line
start = Point2D.Create(MM(0), MM(-97))
end = Point2D.Create(MM(0), MM(203))
result = SketchLine.Create(start, end)

baseSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[0].GetChildren[ICurvePoint]()[0])
targetSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].GetChildren[IDatumLine]()[1])

result = Constraint.CreateCoincident(baseSel, targetSel)

baseSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[0].GetChildren[ICurvePoint]()[1])
targetSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].GetChildren[IDatumLine]()[1])

result = Constraint.CreateCoincident(baseSel, targetSel)

curveSelList = Selection.Create(GetRootPart().DatumPlanes[0].Curves[0])
result = Constraint.CreateVertical(curveSelList)

baseSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[0])
targetSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].GetChildren[IDatumLine]()[0])

result = Constraint.CreatePerpendicular(baseSel, targetSel)
# EndBlock

# Sketch Line
start = Point2D.Create(MM(0), MM(203))
end = Point2D.Create(MM(1299.03810567665), MM(953.000000000006))
result = SketchLine.Create(start, end)

baseSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[1].GetChildren[ICurvePoint]()[0])
targetSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].GetChildren[IDatumLine]()[1])

result = Constraint.CreateCoincident(baseSel, targetSel)

baseSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[1].GetChildren[ICurvePoint]()[0])
targetSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[0].GetChildren[ICurvePoint]()[1])

result = Constraint.CreateCoincident(baseSel, targetSel)
# EndBlock

# Sketch Line
start = Point2D.Create(MM(0), MM(-97))
end = Point2D.Create(MM(1299.03810567666), MM(-846.999999999997))
result = SketchLine.Create(start, end)

baseSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[2].GetChildren[ICurvePoint]()[0])
targetSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].GetChildren[IDatumLine]()[1])

result = Constraint.CreateCoincident(baseSel, targetSel)

baseSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[2].GetChildren[ICurvePoint]()[0])
targetSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[0].GetChildren[ICurvePoint]()[0])

result = Constraint.CreateCoincident(baseSel, targetSel)
# EndBlock

# Create Three Point Arc
point1 = Point2D.Create(MM(1299.03810567665), MM(953.000000000006))
point2 = Point2D.Create(MM(1299.03810567666), MM(-846.999999999997))
point3 = Point2D.Create(MM(1540.08973132457), MM(72.2229188163787))
result = SketchArc.Create3PointArc(point1, point2, point3)

baseSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[3].GetChildren[ICurvePoint]()[1])
targetSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[2].GetChildren[ICurvePoint]()[1])

result = Constraint.CreateCoincident(baseSel, targetSel)
# EndBlock

# Solidify Sketch
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode, None)
# EndBlock

# Thicken 1 Face
selection = FaceSelection.Create(GetRootPart().Bodies[3].Faces[0])
options = ThickenFaceOptions()
options.PullSymmetric = True
options.ExtrudeType = ExtrudeType.ForceIndependent
result = ThickenFaces.Execute(selection, Direction.DirY, MM(150), options)
# EndBlock

# Intersect Bodies
targets = BodySelection.Create(GetRootPart().Bodies[3])
tools = BodySelection.Create(GetRootPart().Bodies[1])
options = MakeSolidsOptions()
result = Combine.Intersect(targets, tools, options)
# EndBlock

# Delete Objects
selection = BodySelection.Create(GetRootPart().Bodies[4])
result = Combine.RemoveRegions(selection)
# EndBlock

# Intersect Bodies
targets = BodySelection.Create(GetRootPart().Bodies[3])
tools = BodySelection.Create(GetRootPart().Bodies[2])
options = MakeSolidsOptions()
result = Combine.Intersect(targets, tools, options)
# EndBlock

# Delete Objects
selection = BodySelection.Create(GetRootPart().Bodies[4])
result = Combine.RemoveRegions(selection)
# EndBlock

# Intersect Bodies
targets = BodySelection.Create(GetRootPart().Bodies[3])
tools = BodySelection.Create(GetRootPart().Bodies[0])
options = MakeSolidsOptions()
result = Combine.Intersect(targets, tools, options)
# EndBlock

# Delete Objects
selection = BodySelection.Create(GetRootPart().Bodies[4])
result = Combine.RemoveRegions(selection)
# EndBlock

# 
result = Copy.ToClipboard(FaceSelection.Create([GetRootPart().Bodies[0].Faces[3],
    GetRootPart().Bodies[2].Faces[5],
    GetRootPart().Bodies[2].Faces[4],
    GetRootPart().Bodies[0].Faces[4],
    GetRootPart().Bodies[2].Faces[3],
    GetRootPart().Bodies[0].Faces[1],
    GetRootPart().Bodies[2].Faces[1]]))
# EndBlock

# Paste from Clipboard
result = Paste.FromClipboard()
# EndBlock

# 
result = Copy.ToClipboard(FaceSelection.Create([GetRootPart().Bodies[1].Faces[4],
    GetRootPart().Bodies[1].Faces[3],
    GetRootPart().Bodies[1].Faces[1]]))
# EndBlock

# Paste from Clipboard
result = Paste.FromClipboard()
# EndBlock

# Set Sketch Plane
sectionPlane = Plane.PlaneXY
result = ViewHelper.SetSketchPlane(sectionPlane, None)
# EndBlock

# Set New Sketch
result = SketchHelper.StartConstraintSketching()
# EndBlock

# Project to Sketch
selection = BodySelection.Create(GetRootPart().Bodies[0])
plane = Plane.PlaneXY
result = ProjectToSketch.Create(selection, plane)
# EndBlock

# Delete Selection
selection = Selection.Create([GetRootPart().DatumPlanes[0].Curves[7],
    GetRootPart().DatumPlanes[0].Curves[8],
    GetRootPart().DatumPlanes[0].Curves[4],
    GetRootPart().DatumPlanes[0].Curves[2],
    GetRootPart().DatumPlanes[0].Curves[1],
    GetRootPart().DatumPlanes[0].Curves[3],
    GetRootPart().DatumPlanes[0].Curves[9]])
result = Delete.Execute(selection)
# EndBlock

# Offset Sketch Curve
curvesToOffset = Selection.Create([GetRootPart().DatumPlanes[0].Curves[2],
    GetRootPart().DatumPlanes[0].Curves[1],
    GetRootPart().DatumPlanes[0].Curves[0]])
if Parameters.antiflatter_diam + 0.2 > 2.1 and Parameters.antiflatter_diam + 0.2 < 2.8:
    offsetDistance = MM(3.1)
else:
    offsetDistance = MM(Parameters.antiflatter_diam + 0.2)
result = SketchOffsetCurve.Create(curvesToOffset, offsetDistance)
# EndBlock

# Delete Selection
selection = Selection.Create([GetRootPart().DatumPlanes[0].Curves[2],
    GetRootPart().DatumPlanes[0].Curves[0],
    GetRootPart().DatumPlanes[0].Curves[1]])
result = Delete.Execute(selection)
# EndBlock

# Sketch Line
start = Point2D.Create(MM(9), MM(4.45730746748937))
end = Point2D.Create(MM(9), MM(-1.52255726825586))
result = SketchLine.Create(start, end)

baseSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[3].GetChildren[ICurvePoint]()[0])
targetSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[2], 0.00629471188316736)

result = Constraint.CreateCoincident(baseSel, targetSel)

baseSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[3].GetChildren[ICurvePoint]()[1])
targetSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[1], 0.00998047054233021)

result = Constraint.CreateCoincident(baseSel, targetSel)

baseSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[3])
targetSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].GetChildren[IDatumLine]()[0])

result = Constraint.CreatePerpendicular(baseSel, targetSel)
# EndBlock

# Create coordinates dictionary
coord_dict = {
        0:(0, 0),
        1:(0, 1),
        2:(0, 2),
        3:(1, 2),
        4:(2, 2),
        5:(3, 2),
        6:(3, 1),
        7:(3, 0)
        }
# EndBlock

# Sketch Circle
origin = Point2D.Create(MM(Parameters.polymer_volume_coordinate / 2), MM(0))
result = SketchCircle.Create(origin, MM(Parameters.antiflatter_diam))
# EndBlock

# Move the antiflatter to right position
if Parameters.value_to_calculate_antiflatter_center in coord_dict:
    constraint_1 = coord_dict[Parameters.value_to_calculate_antiflatter_center][0]
    constraint_2 = coord_dict[Parameters.value_to_calculate_antiflatter_center][1]
    
    # Coincident Constraint
    baseSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[4].GetChildren[ICurvePoint]()[0])
    targetSel = SelectionPoint.Create(GetRootPart().DatumPlanes[0].Curves[constraint_1].GetChildren[ICurvePoint]()[constraint_2])
    result = Constraint.CreateCoincident(baseSel, targetSel)
    # EndBlock
# EndBlock

# Delete Selection
selection = Selection.Create([GetRootPart().DatumPlanes[0].Curves[1],
    GetRootPart().DatumPlanes[0].Curves[2],
    GetRootPart().DatumPlanes[0].Curves[3],
    GetRootPart().DatumPlanes[0].Curves[0]])
result = Delete.Execute(selection)
# EndBlock

# Solidify Sketch
mode = InteractionMode.Solid
result = ViewHelper.SetViewMode(mode)
# EndBlock

# Sweep 1 Face
selection = FaceSelection.Create(GetRootPart().Bodies[0].Faces[4])
trajectories = EdgeSelection.Create(GetRootPart().Bodies[4].Edges[7])
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
selection = BodySelection.Create(GetRootPart().Bodies[7])
datum = Selection.Create(GetRootPart().DatumPlanes[0])
result = SplitBody.ByCutter(selection, datum)
# EndBlock

# Delete Objects
selection = BodySelection.Create(GetRootPart().Bodies[8])
result = Combine.RemoveRegions(selection)
# EndBlock

# Delete Selection
selection = Selection.Create(GetRootPart().DatumPlanes[0])
result = Delete.Execute(selection)
# EndBlock

# Intersect Bodies
targets = BodySelection.Create(GetRootPart().Bodies[0])
tools = BodySelection.Create(GetRootPart().Bodies[7])
options = MakeSolidsOptions()
result = Combine.Intersect(targets, tools, options)
# EndBlock

# Delete Objects
selection = BodySelection.Create(GetRootPart().Bodies[8])
result = Combine.RemoveRegions(selection)
# EndBlock

# Fix 2 Interferences
result = FixInterference.FindAndFix()
# EndBlock

# Delete Selection
selection = EdgeSelection.Create(GetRootPart().Bodies[0].Edges[8])
result = Delete.Execute(selection)
# EndBlock

# Create Named Selection Group
primarySelection = FaceSelection.Create([GetRootPart().Bodies[0].Faces[2],
    GetRootPart().Bodies[2].Faces[0],
    GetRootPart().Bodies[1].Faces[0]])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Fixed support")
# EndBlock

# Create Named Selection Group
primarySelection = BodySelection.Create([GetRootPart().Bodies[4],
    GetRootPart().Bodies[5],
    GetRootPart().Bodies[6]])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Composite")
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
primarySelection = BodySelection.Create([GetRootPart().Bodies[1],
    GetRootPart().Bodies[2]])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Fullfillment")
# EndBlock

# Create Named Selection Group
primarySelection = BodySelection.Create(GetRootPart().Bodies[7])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Antiflatter")
# EndBlock

# Delete Selection
selection = BodySelection.Create(GetRootPart().Bodies[3])
result = Delete.Execute(selection)
# EndBlock

# 
result = Midsurface.Convert(BodySelection.Create([GetRootPart().Bodies[3],
    GetRootPart().Bodies[4],
    GetRootPart().Bodies[5]]), MM(1))
# EndBlock

# Create Named Selection Group
primarySelection = FaceSelection.Create([GetRootPart().Bodies[3].Faces[2],
    GetRootPart().Bodies[4].Faces[3],
    GetRootPart().Bodies[3].Faces[1],
    GetRootPart().Bodies[4].Faces[1],
    GetRootPart().Bodies[4].Faces[2],
    GetRootPart().Bodies[3].Faces[0],
    GetRootPart().Bodies[2].Faces[0],
    GetRootPart().Bodies[0].Faces[2]])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Langeron")
# EndBlock

# Create Named Selection Group
primarySelection = BodySelection.Create(GetRootPart().Bodies[5])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Shell")
# EndBlock

# Create Named Selection Group
primarySelection = FaceSelection.Create(GetRootPart().Bodies[4].Faces[0])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Langeron_wall")
# EndBlock

# Create Named Selection Group
primarySelection = FaceSelection.Create([GetRootPart().Bodies[5].Faces[2],
    GetRootPart().Bodies[4].Faces[3],
    GetRootPart().Bodies[3].Faces[2],
    GetRootPart().Bodies[3].Faces[1],
    GetRootPart().Bodies[4].Faces[1],
    GetRootPart().Bodies[5].Faces[0]])
secondarySelection = Selection.Empty()
result = NamedSelection.Create(primarySelection, secondarySelection)
# EndBlock

# Rename Named Selection
result = NamedSelection.Rename("Группа1", "Pressure")
# EndBlock