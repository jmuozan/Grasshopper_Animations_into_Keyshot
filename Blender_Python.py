import bpy
import csv
import os

# Path to the OBJ_SEQUENCE folder
output_dir = "/Users/jorgemuyo/Desktop/GH/GH-KS/OBJ_SEQUENCE"

# Create the directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Delete all objects in the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Read files
with open("/Users/jorgemuyo/Desktop/GH/GH-KS/Face.csv") as f:
    Face_data = list((csv.reader(f)))

with open("/Users/jorgemuyo/Desktop/GH/GH-KS/Vert.csv") as v:
    Vert_data = list((csv.reader(v)))

# Getting vert and face
Vert = ([tuple(map(float, x)) for x in Vert_data])
Face = ([tuple(map(int, x)) for x in Face_data])
Edge = []

# Generating meshes
mesh = bpy.data.meshes.new("from_gh")
obj = bpy.data.objects.new(mesh.name, mesh)
col = bpy.data.collections.get("Collection")
if col is None:
    col = bpy.context.scene.collection
col.objects.link(obj)
bpy.context.view_layer.objects.active = obj
mesh.from_pydata(Vert, Edge, Face)

# Read files for animation_data and arrange
with open("/Users/jorgemuyo/Desktop/GH/GH-KS/Animation.csv") as a:
    Animation_data = list(csv.reader(a, quoting=csv.QUOTE_NONNUMERIC))

itr = len(Animation_data)
no_co = len(Animation_data[0]) - 1
no_v = int(no_co / 3)
v_co = [[tuple(x[i:i+3]) for i in range(0, no_co, 3)] for x in Animation_data]

# Getting last created objects
context = bpy.context
ob = context.object
me = ob.data

print("Start keyframing")
# Keyframing
for i in range(itr):
    for j in range(no_v):
        v = me.vertices[j]
        v.co = v_co[i][j]
        v.keyframe_insert("co")

    bpy.context.scene.frame_current += 3
    perc = "{:.0%}".format(i / itr)
    print(perc, end="\r")
print("Successfully imported")

# Add subdivision modifier with 2 levels
mod_subsurf = obj.modifiers.new(name="Subdivision", type='SUBSURF')
mod_subsurf.levels = 3
mod_subsurf.render_levels = 3

# Deselect all objects
bpy.ops.object.select_all(action='DESELECT')

# Select all objects
bpy.ops.object.select_all(action='SELECT')

# Export each frame as an OBJ file
for frame in range(1, bpy.context.scene.frame_end + 1):
    bpy.context.scene.frame_set(frame)
    filepath = os.path.join(output_dir, f"frame_{frame:04d}.obj")
    bpy.ops.wm.obj_export(filepath=filepath, export_selected_objects=True, export_materials=False)

print("Exported all frames as OBJ files")
