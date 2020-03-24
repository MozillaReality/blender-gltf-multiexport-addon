import bpy



class ClipboardToolsProps(bpy.types.PropertyGroup):
  decimals: bpy.props.IntProperty(name="Decimals", default = 3, min = 0)
  scale: bpy.props.FloatProperty(name="Scale", default = 1.0)


class CopyPositionToClipboard(bpy.types.Operator):
  """Copies selected object's position to clipboard (in OpenGL coords)"""
  bl_idname = "object.copy_position_to_clipboard"
  bl_label = "Copy Position to Clipboard"

  @classmethod
  def poll(cls, context):
    return context.active_object is not None

  def execute(self, context):
    props = context.scene.clipboard_tools_props
    decimals = props.decimals
    scale = props.scale

    obj = context.active_object
    x = round(obj.location.x * scale, decimals)
    y = round(obj.location.y * scale, decimals)
    z = round(obj.location.z * scale, decimals)

    if decimals == 0:
      x = int(x)
      y = int(y)
      z = int(z)

    clipdata = str(x) + ', ' + str(z) + ', ' + str(-y)
    bpy.context.window_manager.clipboard = clipdata
    return {'FINISHED'}


class CopyRotationToClipboard(bpy.types.Operator):
  """Copies selected object's rotation to clipboard (in OpenGL coords)"""
  bl_idname = "object.copy_rotation_to_clipboard"
  bl_label = "Copy Rotation to Clipboard"

  @classmethod
  def poll(cls, context):
    return context.active_object is not None

  def execute(self, context):
    props = context.scene.clipboard_tools_props
    decimals = props.decimals

    obj = context.active_object
    x = round(obj.rotation_euler.x, decimals)
    y = round(obj.rotation_euler.y, decimals)
    z = round(obj.rotation_euler.z, decimals)

    if decimals == 0:
      x = int(x)
      y = int(y)
      z = int(z)

    clipdata = str(x) + ', ' + str(z) + ', ' + str(-y)
    bpy.context.window_manager.clipboard = clipdata
    return {'FINISHED'}


class CopyScaleToClipboard(bpy.types.Operator):
  """Copies selected object's scale to clipboard (in OpenGL coords)"""
  bl_idname = "object.copy_scale_to_clipboard"
  bl_label = "Copy Scale to Clipboard"

  @classmethod
  def poll(cls, context):
    return context.active_object is not None

  def execute(self, context):
    props = context.scene.clipboard_tools_props
    decimals = props.decimals
    scale = props.scale

    obj = context.active_object
    x = round(obj.scale.x * scale, decimals)
    y = round(obj.scale.y * scale, decimals)
    z = round(obj.scale.z * scale, decimals)

    if decimals == 0:
      x = int(x)
      y = int(y)
      z = int(z)

    clipdata = str(x) + ', ' + str(z) + ', ' + str(y)
    bpy.context.window_manager.clipboard = clipdata
    return {'FINISHED'}



class CopyGeometryToClipboard(bpy.types.Operator):
  """Copies selected object's geometry (verts + faces) to clipboard (in OpenGL coords)"""
  bl_idname = "object.copy_geometry_to_clipboard"
  bl_label = "Copy Geometry to Clipboard"

  @classmethod
  def poll(cls, context):
    return context.active_object is not None

  def execute(self, context):
    props = context.scene.clipboard_tools_props
    decimals = props.decimals
    scale = props.scale

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

    clipdata = 'var ' + obj.name + ' = {\n'
    clipdata += '\tvertices: ['+', '.join(verts)+'],\n'
    clipdata += '\tfaces: ['+', '.join(faces)+']\n};'

    bpy.context.window_manager.clipboard = clipdata

    return {'FINISHED'}



class ClipboardToolsPanel(bpy.types.Panel):
    """Clipboard tools panel"""
    bl_label = "WebXR - Clipboard Tools"
    bl_idname = "OBJECT_PT_clipboardtools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_context = 'objectmode'
    bl_category = "Edit"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text = "Decimals")
        row.prop(context.scene.clipboard_tools_props, "decimals", text = "")
        row = layout.row()
        row.label(text = "Scale factor")
        row.prop(context.scene.clipboard_tools_props, "scale", text = "")

        row = layout.separator()

        row = layout.row()
        row.operator("object.copy_position_to_clipboard", text = "Copy Position", icon = "COPYDOWN")
        row = layout.row()
        row.operator("object.copy_rotation_to_clipboard", text = "Copy Rotation", icon = "COPYDOWN")
        row = layout.row()
        row.operator("object.copy_scale_to_clipboard", text = "Copy Scale", icon = "COPYDOWN")
        row = layout.row()
        row.operator("object.copy_geometry_to_clipboard", text = "Copy Geometry", icon = "COPYDOWN")


def register():
  bpy.utils.register_class(ClipboardToolsProps)
  bpy.types.Scene.clipboard_tools_props = bpy.props.PointerProperty(type=ClipboardToolsProps)
  bpy.utils.register_class(CopyPositionToClipboard)
  bpy.utils.register_class(CopyRotationToClipboard)
  bpy.utils.register_class(CopyScaleToClipboard)
  bpy.utils.register_class(CopyGeometryToClipboard)
  bpy.utils.register_class(ClipboardToolsPanel)

def unregister():
  bpy.utils.unregister_class(ClipboardToolsPanel)
  bpy.utils.unregister_class(CopyGeometryToClipboard)
  bpy.utils.unregister_class(CopyScaleToClipboard)
  bpy.utils.unregister_class(CopyRotationToClipboard)
  bpy.utils.unregister_class(CopyPositionToClipboard)
  del bpy.types.Scene.clipboard_tools_props
  bpy.utils.unregister_class(ClipboardToolsProps)

if __name__ == "__main__":
    register()
