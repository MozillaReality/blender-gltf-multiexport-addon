import bpy

decimals = 2
scale = 1

obj = bpy.context.active_object
x = round(obj.rotation_euler.x, decimals)
y = round(obj.rotation_euler.y, decimals)
z = round(obj.rotation_euler.z, decimals)

if decimals == 0:
    x = int(x)
    y = int(y)
    z = int(z)
    
clipdata = str(x) + ', ' + str(z) + ', ' + str(y)

bpy.context.window_manager.clipboard = clipdata
