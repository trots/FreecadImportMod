import json
import FreeCAD
import Part


def addExtension():
    FreeCAD.addImportType("Box file type (*.box)", "FreecadImportMod")


def insert(file_name, document_name):
    FreeCAD.Console.PrintMessage("Importing file " + file_name)

    with open(file_name) as box_file:
        # Read box file data
        data = json.load(box_file)
        width = data["width"]
        height = data["height"]
        depth = data["depth"]

        # Get target document
        doc = FreeCAD.getDocument(document_name)

        # Create sketch with box profile lines
        doc.addObject('Sketcher::SketchObject', 'Sketch')
        doc.Sketch.Placement = FreeCAD.Placement(FreeCAD.Vector(0.0, 0.0, 0.0), 
                                                 FreeCAD.Rotation(0.0, 0.0, 0.0, 1.0))
        line1 = Part.LineSegment()
        line1.StartPoint = (0.0, 0.0, 0.0)
        line1.EndPoint = (width, 0.0, 0.0)
        doc.Sketch.addGeometry(line1, False)
        line2 = Part.LineSegment()
        line2.StartPoint = (width, 0.0, 0.0)
        line2.EndPoint = (width, height, 0.0)
        doc.Sketch.addGeometry(line2, False)
        line3 = Part.LineSegment()
        line3.StartPoint = (width, height, 0.0)
        line3.EndPoint = (0.0, height, 0.0)
        doc.Sketch.addGeometry(line3, False)
        line4 = Part.LineSegment()
        line4.StartPoint = (0.0, height, 0.0)
        line4.EndPoint = (0.0, 0.0, 0.0)
        doc.Sketch.addGeometry(line4, False)

        # Extrude sketch
        doc.addObject('Part::Extrusion','Extrude')
        doc.Extrude.Base = doc.Sketch
        doc.Extrude.DirMode = "Normal"
        doc.Extrude.DirLink = None
        doc.Extrude.LengthFwd = depth
        doc.Extrude.LengthRev = 0.0
        doc.Extrude.Solid = True
        doc.Extrude.Reversed = False
        doc.Extrude.Symmetric = False
        doc.Extrude.TaperAngle = 0.0
        doc.Extrude.TaperAngleRev = 0.0

        doc.recompute()
