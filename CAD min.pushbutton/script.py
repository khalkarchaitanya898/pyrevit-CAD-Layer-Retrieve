from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from Autodesk.Revit.UI.Selection import ObjectType
import clr
from pyrevit import forms

clr.AddReference('PresentationFramework')
clr.AddReference('PresentationCore')
clr.AddReference('WindowsBase')

def pick_cad_file(ui_doc):
    try:
        with forms.WarningBar(title='Pick a CAD file from the model'):
            picked_ref = ui_doc.Selection.PickObject(ObjectType.Element, "Pick a CAD file:")
            picked_element = ui_doc.Document.GetElement(picked_ref.ElementId)
            return picked_element if isinstance(picked_element, ImportInstance) else None
    except Exception as e:
        forms.alert(f'Error: {str(e)}', exitscript=True)

def print_cad_content(cad_instance, doc):
    layer_geometry = {}
    for geom_obj in cad_instance.get_Geometry(Options()):
        if isinstance(geom_obj, GeometryInstance):
            for geom in geom_obj.GetInstanceGeometry():
                if geom.GraphicsStyleId:
                    style = doc.GetElement(geom.GraphicsStyleId)
                    if style:
                        layer_name = style.GraphicsStyleCategory.Name
                        geom_type = geom.GetType().Name
                        layer_geometry.setdefault(layer_name, {}).setdefault(geom_type, 0)
                        layer_geometry[layer_name][geom_type] += 1

    print("Geometry organized by layer:")
    for layer_name, counts in layer_geometry.items():
        print(f"\nLayer: {layer_name}")
        for geom_type, count in counts.items():
            print(f"  - {geom_type}: {count}")

ui_doc = __revit__.ActiveUIDocument
doc = ui_doc.Document
cad_instance = pick_cad_file(ui_doc)

if cad_instance:
    print("CAD content details:")
    print_cad_content(cad_instance, doc)
else:
    forms.alert('Selected element is not a valid CAD file!', exitscript=True)
