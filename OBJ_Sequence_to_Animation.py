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

# Function to import obj files
def import_obj_files():
    imported_objects = []
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        bpy.ops.wm.obj_import(filepath=file_path)
        obj_name = os.path.splitext(file_name)[0]
        obj = bpy.context.selected_objects[0]
        obj.name = obj_name
        imported_objects.append(obj)
        print(f"Imported {file_name}")
    return imported_objects

# Function to create animation
def create_animation(imported_objects):
    for frame, obj in enumerate(imported_objects):
        bpy.context.scene.frame_set(frame + 1)
        
        for other_obj in imported_objects:
            other_obj.hide_viewport = True
            other_obj.hide_render = True
            other_obj.keyframe_insert(data_path="hide_viewport", frame=frame + 1)
            other_obj.keyframe_insert(data_path="hide_render", frame=frame + 1)
        
        obj.hide_viewport = False
        obj.hide_render = False
        obj.keyframe_insert(data_path="hide_viewport", frame=frame + 1)
        obj.keyframe_insert(data_path="hide_render", frame=frame + 1)
        print(f"Frame {frame + 1}: Showing {obj.name}")

# Import the obj files
imported_objects = import_obj_files()

# Create the animation
create_animation(imported_objects)

print("Animation creation complete.")