import bpy
import csv

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

# Export the scene
bpy.ops.wm.alembic_export(filepath="/Users/jorgemuyo/Desktop/GH/GH-KS/Exported_Animation.abc")


import bpy
import os
import re

# Delete all objects in the scene
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# Path to the folder containing the obj files
folder_path = "/Users/jorgemuyo/Desktop/GH/GH-KS/OBJ_SEQUENCE"

# Function to sort files by numerical suffix
def numerical_sort(value):
    numbers = re.findall(r'\d+', value)
    return int(numbers[-1]) if numbers else -1

# List all files in the directory, filter .obj files, and sort them
file_list = sorted([f for f in os.listdir(folder_path) if f.endswith('.obj')], key=numerical_sort)

# Function to import obj file
def import_obj_file(file_path):
    bpy.ops.wm.obj_import(filepath=file_path)
    obj = bpy.context.selected_objects[0]
    return obj

# Import the first OBJ file and use it as the base mesh
base_obj = import_obj_file(os.path.join(folder_path, file_list[0]))
base_obj.name = "BaseMesh"
bpy.context.view_layer.objects.active = base_obj
base_obj.shape_key_add(name="Basis", from_mix=False)

# Function to create shape keys from subsequent OBJ files
def create_shape_keys(base_obj, file_list):
    for i, file_name in enumerate(file_list[1:]):
        file_path = os.path.join(folder_path, file_name)
        temp_obj = import_obj_file(file_path)
        
        shape_key = base_obj.shape_key_add(name=f"Frame_{i+1}", from_mix=False)
        
        # Copy vertex positions from the imported object to the shape key
        for j, vert in enumerate(temp_obj.data.vertices):
            shape_key.data[j].co = vert.co
        
        # Delete the temporary object
        bpy.data.objects.remove(temp_obj, do_unlink=True)
        
        print(f"Created shape key for {file_name}")

# Create shape keys
create_shape_keys(base_obj, file_list)

# Function to animate shape key influence
def animate_shape_keys(base_obj, file_list):
    for frame, file_name in enumerate(file_list[1:], start=1):
        bpy.context.scene.frame_set(frame)
        for sk in base_obj.data.shape_keys.key_blocks:
            sk.value = 0.0
            sk.keyframe_insert(data_path="value", frame=frame)
        shape_key = base_obj.data.shape_keys.key_blocks[f"Frame_{frame}"]
        shape_key.value = 1.0
        shape_key.keyframe_insert(data_path="value", frame=frame)
        print(f"Frame {frame}: Shape key {shape_key.name} set to 1.0")

# Animate shape keys
animate_shape_keys(base_obj, file_list)

# Clean up the scene by deleting all objects except the base_obj
def cleanup_scene(base_obj):
    for obj in bpy.context.scene.objects:
        if obj != base_obj and obj.type != 'CAMERA' and obj.type != 'LIGHT':
            bpy.data.objects.remove(obj, do_unlink=True)

# Perform cleanup
cleanup_scene(base_obj)

print("Mesh deforming animation creation complete.")