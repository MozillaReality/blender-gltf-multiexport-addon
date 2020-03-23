import bpy

decimals = 2
scale = 1

obj = bpy.context.active_object.data
verts = []
faces = []
for v in obj.vertices:
    x = round(v.co.x * scale, decimals)
    y = round(v.co.z * scale, decimals)
    z = round(-v.co.y * scale, decimals)
    if decimals == 0:
        x = int(x)
        y = int(y)
        z = int(z)
    verts.append(str(x))
    verts.append(str(y))
    verts.append(str(z))

	
for f in obj.polygons:
	for v in f.vertices:
	    faces.append(str(v))

clipdata = 'var object = {\n\tname: "'+ obj.name + '",\n'
clipdata += '\tvertices: ['+', '.join(verts)+'],\n'
clipdata += '\tfaces: ['+', '.join(faces)+']\n}'

bpy.context.window_manager.clipboard = clipdata
