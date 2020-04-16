import bpy
from os import path
from bpy.app.handlers import persistent

bl_info = {
    "name": "glTF MultiExporter",
    "category": "Import-Export",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    'location': 'File > Export > glTF 2.0 multiexport',
    'description': 'Allows to batch export objects to individual glTFs',
    'isDraft': False,
    'developer': "Diego F. Goberna",
    'url': 'https://github.com/feiss/blender-addons-for-webxr'
}

bpy.types.Object.gltf_export_do = bpy.props.BoolProperty(
        name='Export',
        description='Export object?',
        default=True
    )

bpy.types.Object.gltf_export_basename = bpy.props.StringProperty(
        name='Alternative file name',
        description='Base name for the exported file, without extension. If empty, object name will be used',
        default='',
    )


bpy.types.Object.gltf_export_format = bpy.props.EnumProperty(
        name='Format',
        items=(('GLB', 'glTF Binary (.glb)',
                'Exports a single file, with all data packed in binary form. '
                'Most efficient and portable, but more difficult to edit later'),
               ('GLTF_EMBEDDED', 'glTF Embedded (.gltf)',
                'Exports a single file, with all data packed in JSON. '
                'Less efficient than binary, but easier to edit later'),
               ('GLTF_SEPARATE', 'glTF Separate (.gltf + .bin + textures)',
                'Exports multiple files, with separate JSON, binary and texture data. '
                'Easiest to edit later')),
        description=(
            'Output format and embedding options. Binary is most efficient, '
            'but JSON (embedded or separate) may be easier to edit later'
        ),
        default='GLB'
    )

bpy.types.Object.gltf_export_image_format = bpy.props.EnumProperty(
        name='Images',
        items=(('NAME', 'Automatic',
                'Determine the image format from the blender image name'),
                ('JPEG', 'JPEG Format (.jpg)',
                'Encode and save textures as .jpg files. Be aware of a possible loss in quality'),
               ('PNG', 'PNG Format (.png)',
                'Encode and save textures as .png files')
               ),
        description=(
            'Output format for images. PNG is lossless and generally preferred, but JPEG might be preferable for web '
            'applications due to the smaller file size'
        ),
        default='NAME'
    )

bpy.types.Object.gltf_export_texture_dir = bpy.props.StringProperty(
        name='Textures',
        description='Folder to place texture files in. Relative to the .gltf file',
        default='',
    )

bpy.types.Object.gltf_export_texcoords = bpy.props.BoolProperty(
        name='UVs',
        description='Export UVs (texture coordinates) with meshes',
        default=True
    )

bpy.types.Object.gltf_export_normals = bpy.props.BoolProperty(
        name='Normals',
        description='Export vertex normals with meshes',
        default=True
    )

bpy.types.Object.gltf_export_draco_mesh_compression_enable = bpy.props.BoolProperty(
        name='Draco mesh compression',
        description='Compress mesh using Draco',
        default=False
    )

bpy.types.Object.gltf_export_draco_mesh_compression_level = bpy.props.IntProperty(
        name='Compression level',
        description='Compression level (0 = most speed, 6 = most compression, higher values currently not supported)',
        default=6,
        min=0,
        max=6
    )

bpy.types.Object.gltf_export_draco_position_quantization = bpy.props.IntProperty(
        name='Quantize Position',
        description='Quantization bits for position values (0 = no quantization)',
        default=14,
        min=0,
        max=30
    )

bpy.types.Object.gltf_export_draco_normal_quantization = bpy.props.IntProperty(
        name='Normal',
        description='Quantization bits for normal values (0 = no quantization)',
        default=10,
        min=0,
        max=30
    )

bpy.types.Object.gltf_export_draco_texcoord_quantization = bpy.props.IntProperty(
        name='Tex Coords',
        description='Quantization bits for texture coordinate values (0 = no quantization)',
        default=12,
        min=0,
        max=30
    )

bpy.types.Object.gltf_export_draco_generic_quantization = bpy.props.IntProperty(
        name='Generic',
        description='Quantization bits for generic coordinate values like weights or joints (0 = no quantization)',
        default=12,
        min=0,
        max=30
    )

bpy.types.Object.gltf_export_tangents = bpy.props.BoolProperty(
        name='Tangents',
        description='Export vertex tangents with meshes',
        default=False
    )

bpy.types.Object.gltf_export_materials = bpy.props.BoolProperty(
        name='Materials',
        description='Export materials',
        default=True
    )

bpy.types.Object.gltf_export_colors = bpy.props.BoolProperty(
        name='Vertex Colors',
        description='Export vertex colors with meshes',
        default=True
    )

bpy.types.Object.gltf_export_extras = bpy.props.BoolProperty(
        name='Custom Properties',
        description='Export custom properties as glTF extras',
        default=False
    )

bpy.types.Object.gltf_export_yup = bpy.props.BoolProperty(
        name='+Y Up',
        description='Export using glTF convention, +Y up',
        default=True
    )

bpy.types.Object.gltf_export_apply = bpy.props.BoolProperty(
        name='Apply Modifiers',
        description='Apply modifiers (excluding Armatures) to mesh objects -'
                    'WARNING: prevents exporting shape keys',
        default=False
    )

bpy.types.Object.gltf_export_animations = bpy.props.BoolProperty(
        name='Animations',
        description='Exports active actions and NLA tracks as glTF animations',
        default=True
    )

bpy.types.Object.gltf_export_frame_range = bpy.props.BoolProperty(
        name='Limit to Playback Range',
        description='Clips animations to selected playback range',
        default=True
    )

bpy.types.Object.gltf_export_frame_step = bpy.props.IntProperty(
        name='Sampling Rate',
        description='How often to evaluate animated values (in frames)',
        default=1,
        min=1,
        max=120
    )

bpy.types.Object.gltf_export_force_sampling = bpy.props.BoolProperty(
        name='Always Sample Animations',
        description='Apply sampling to all animations',
        default=True
    )

bpy.types.Object.gltf_export_nla_strips = bpy.props.BoolProperty(
        name='NLA Strips',
        description='Export NLA Strip animations',
        default=True
    )

bpy.types.Object.gltf_export_def_bones = bpy.props.BoolProperty(
        name='Export Deformation bones only',
        description='Export Deformation bones only (and needed bones for hierarchy)',
        default=False
    )

bpy.types.Object.gltf_export_current_frame = bpy.props.BoolProperty(
        name='Use Current Frame',
        description='Export the scene in the current animation frame',
        default=False
    )

bpy.types.Object.gltf_export_skins = bpy.props.BoolProperty(
        name='Skinning',
        description='Export skinning (armature) data',
        default=True
    )

bpy.types.Object.gltf_export_all_influences = bpy.props.BoolProperty(
        name='Include All Bone Influences',
        description='Allow >4 joint vertex influences. Models may appear incorrectly in many viewers',
        default=False
    )

bpy.types.Object.gltf_export_morph = bpy.props.BoolProperty(
        name='Shape Keys',
        description='Export shape keys (morph targets)',
        default=True
    )

bpy.types.Object.gltf_export_morph_normal = bpy.props.BoolProperty(
        name='Shape Key Normals',
        description='Export vertex normals with shape keys (morph targets)',
        default=True
    )

bpy.types.Object.gltf_export_morph_tangent = bpy.props.BoolProperty(
        name='Shape Key Tangents',
        description='Export vertex tangents with shape keys (morph targets)',
        default=False
    )

bpy.types.Object.gltf_export_displacement = bpy.props.BoolProperty(
        name='Displacement Textures (EXPERIMENTAL)',
        description='EXPERIMENTAL: Export displacement textures. '
                    'Uses incomplete "KHR_materials_displacement" glTF extension',
        default=False
    )


#@persistent
#def gltfmulti_scene_update(scene):
#    obj = bpy.context.edit_object
#    if obj is not None and obj.is_updated_data is True:
#        obj.gltf_export_basename = obj.name
#        print(obj.name +' changed')


class GLTFMULTI_PT_MultiExportPanel(bpy.types.Panel):
    """Creates a MultiExport Panel in the Object properties window"""
    bl_label = "glTF Export Settings"
    bl_idname = "GLTFMULTI_PT_gltfmultiexport"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    @classmethod
    def poll(cls, context):
        return len(context.selected_objects) > 0

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        obj = context.object

        layout.prop(obj, "gltf_export_do")
        layout.prop(obj, "gltf_export_basename", icon='FILE_BLANK')
        layout.separator()
        layout.prop(obj, "gltf_export_format")
        layout.prop(obj, "gltf_export_image_format")

        if obj.gltf_export_format == 'GLTF_SEPARATE':
            layout.prop(obj, 'gltf_export_texture_dir', icon='FILE_FOLDER')

        layout.separator()
        layout.prop(obj, "gltf_export_yup")
        layout.prop(obj, "gltf_export_apply")
        layout.separator()
        layout.prop(obj, "gltf_export_texcoords")
        layout.prop(obj, "gltf_export_normals")
        layout.prop(obj, "gltf_export_tangents")
        layout.prop(obj, "gltf_export_materials")
        layout.separator()
        layout.prop(obj, "gltf_export_colors")
        layout.prop(obj, "gltf_export_extras")


class GLTFMULTI_PT_MultiExportDracoSubpanel(bpy.types.Panel):
    bl_label = "DRACO Compression"
    bl_idname = "GLTFMULTI_PT_gltfmultiexportdraco"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_parent_id = "GLTFMULTI_PT_gltfmultiexport"
    bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        obj = context.object
        self.layout.prop(obj, "gltf_export_draco_mesh_compression_enable", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        obj = context.object
        layout.active = obj.gltf_export_draco_mesh_compression_enable

        col = layout.column(align=True)
        col.prop(obj, "gltf_export_draco_mesh_compression_level")
        col.prop(obj, "gltf_export_draco_position_quantization")
        col.prop(obj, "gltf_export_draco_normal_quantization")
        col.prop(obj, "gltf_export_draco_texcoord_quantization")
        col.prop(obj, "gltf_export_draco_generic_quantization")


class GLTFMULTI_PT_MultiExportAnimationSubpanel(bpy.types.Panel):
    bl_label = "Animation"
    bl_idname = "GLTFMULTI_PT_gltfmultiexportanimation"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_parent_id = "GLTFMULTI_PT_gltfmultiexport"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        obj = context.object
        layout.prop(obj, "gltf_export_current_frame")


class GLTFMULTI_PT_MultiExportAnimationSubSubpanel(bpy.types.Panel):
    bl_label = "Animation"
    bl_idname = "GLTFMULTI_PT_gltfmultiexportanimationsub"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_parent_id = "GLTFMULTI_PT_gltfmultiexportanimation"

    def draw_header(self, context):
        obj = context.object
        self.layout.prop(obj, "gltf_export_animations", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        obj = context.object
        layout.active = obj.gltf_export_animations
        layout.prop(obj, "gltf_export_frame_range")
        layout.prop(obj, "gltf_export_frame_step")
        layout.prop(obj, "gltf_export_force_sampling")
        layout.prop(obj, "gltf_export_nla_strips")
        layout.prop(obj, "gltf_export_def_bones")


class GLTFMULTI_PT_MultiExportAnimationShapekeysSubpanel(bpy.types.Panel):
    bl_label = "Shape Keys"
    bl_idname = "GLTFMULTI_PT_gltfmultiexportanimationshapekeys"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_parent_id = "GLTFMULTI_PT_gltfmultiexportanimation"

    def draw_header(self, context):
        obj = context.object
        self.layout.prop(obj, "gltf_export_morph", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        obj = context.object
        layout.active = obj.gltf_export_morph
        layout.prop(obj, "gltf_export_morph_normal")
        layout.prop(obj, "gltf_export_morph_tangent")


class GLTFMULTI_PT_MultiExportAnimationSkinningSubpanel(bpy.types.Panel):
    bl_label = "Skinning"
    bl_idname = "GLTFMULTI_PT_gltfmultiexportanimationskinning"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    bl_parent_id = "GLTFMULTI_PT_gltfmultiexportanimation"

    def draw_header(self, context):
        obj = context.object
        self.layout.prop(obj, "gltf_export_skins", text="")

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True

        obj = context.object
        layout.active = obj.gltf_export_skins
        layout.prop(obj, "gltf_export_all_influences")


# operators #######################################################
def messageBox(message = "", title = "glTF MultiExport", icon = 'INFO'):

    def draw(self, context):
        self.layout.label(text = message)

    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)


'''
bpy.ops.export_scene.gltf(export_format='GLB'
ui_tab='GENERAL'
export_copyright=""
export_image_format='NAME'
export_texture_dir=""
export_texcoords=True
export_normals=True
export_draco_mesh_compression_enable=False
export_draco_mesh_compression_level=6
export_draco_position_quantization=14
export_draco_normal_quantization=10
export_draco_texcoord_quantization=12
export_draco_generic_quantization=12
export_tangents=False
export_materials=True
export_colors=True
export_cameras=False
export_selected=False
export_extras=False
export_yup=True
export_apply=False
export_animations=True
export_frame_range=True
export_frame_step=1
export_force_sampling=True
export_nla_strips=True
export_def_bones=False
export_current_frame=False
export_skins=True
export_all_influences=False
export_morph=True
export_morph_normal=True
export_morph_tangent=False
export_lights=False
export_displacement=False
will_save_settings=False
filepath=""
check_existing=True
'''
def export(context):
    count = 0
    files = []
    copyright = context.scene.gltfmultisettings.copyright
    output_path = context.scene.gltfmultisettings.output_path.strip()
    output_path += '' if output_path[-1] == path.sep else path.sep
    for obj in bpy.data.objects:
        bpy.ops.object.select_all(action='DESELECT')
        if not obj.gltf_export_do: continue
        obj.select_set(True)
        filename = obj.gltf_export_basename.strip()
        if not filename: filename = obj.name.strip()
        filename = bpy.path.clean_name(filename)
        filename += '.glb' if obj.gltf_export_format == 'GLB' else '.gltf'
        bpy.ops.export_scene.gltf(
            export_format = obj.gltf_export_format,
            export_copyright = copyright,
            export_selected = True,
            filepath= bpy.path.abspath(output_path + filename),

            export_image_format = obj.gltf_export_image_format,
            export_texture_dir= obj.gltf_export_texture_dir,
            export_texcoords= obj.gltf_export_texcoords,
            export_normals= obj.gltf_export_normals,
            export_draco_mesh_compression_enable= obj.gltf_export_draco_mesh_compression_enable,
            export_draco_mesh_compression_level= obj.gltf_export_draco_mesh_compression_level,
            export_draco_position_quantization= obj.gltf_export_draco_position_quantization,
            export_draco_normal_quantization= obj.gltf_export_draco_normal_quantization,
            export_draco_texcoord_quantization= obj.gltf_export_draco_texcoord_quantization,
            export_draco_generic_quantization= obj.gltf_export_draco_generic_quantization,
            export_tangents= obj.gltf_export_tangents,
            export_materials= obj.gltf_export_materials,
            export_colors= obj.gltf_export_colors,
            export_extras= obj.gltf_export_extras,
            export_yup= obj.gltf_export_yup,
            export_apply= obj.gltf_export_apply,
            export_animations= obj.gltf_export_animations,
            export_frame_range= obj.gltf_export_frame_range,
            export_frame_step= obj.gltf_export_frame_step,
            export_force_sampling= obj.gltf_export_force_sampling,
            export_nla_strips= obj.gltf_export_nla_strips,
            export_def_bones= obj.gltf_export_def_bones,
            export_current_frame= obj.gltf_export_current_frame,
            export_skins= obj.gltf_export_skins,
            export_all_influences= obj.gltf_export_all_influences,
            export_morph= obj.gltf_export_morph,
            export_morph_normal= obj.gltf_export_morph_normal,
            export_morph_tangent= obj.gltf_export_morph_tangent,
            export_displacement= obj.gltf_export_displacement
        )

        count += 1
        files.append(filename)

    messageBox(str(count) + " objects exported: " + ", ".join(files))
    return {'FINISHED'}

class GLTFMultiExport(bpy.types.Operator):
    """Exports objects to individual glTFs with their own settings"""
    bl_idname = "export_scene.gltf_multi"
    bl_label = "glTF MultiExport"

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        res = export(context)
        return res





# global settings panel ###########################################

class GLTF_MultiProps(bpy.types.PropertyGroup):
  output_path: bpy.props.StringProperty(name="Export path", default="//")
  copyright: bpy.props.StringProperty(name="Copyright", default="")
  #scale: bpy.props.FloatProperty(name="Scale")

class GLTFMULTI_PT_MultiExportGlobal(bpy.types.Panel):
    """Creates a MultiExport Panel settings in the Scene properties window"""
    bl_label = "glTF MultiExport Global Settings"
    bl_idname = "GLTFMULTI_PT_gltfmultiexportglobal"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"

    @classmethod
    def poll(cls, context):
        return True

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.prop(context.scene.gltfmultisettings, "output_path", icon="FILE_FOLDER")
        layout.prop(context.scene.gltfmultisettings, "copyright")
        layout.operator('export_scene.gltf_multi', text='EXPORT')

#def menu_func_export(self, context):
#    print('hola')
#    self.layout.operator('export_scene.gltfmulti', text='glTF 2.0 Multiexport (.glb/.gltf)')


def register():
    bpy.utils.register_class(GLTF_MultiProps)
    bpy.types.Scene.gltfmultisettings = bpy.props.PointerProperty(type=GLTF_MultiProps)

    bpy.utils.register_class(GLTFMULTI_PT_MultiExportPanel)
    bpy.utils.register_class(GLTFMULTI_PT_MultiExportDracoSubpanel)
    bpy.utils.register_class(GLTFMULTI_PT_MultiExportAnimationSubpanel)
    bpy.utils.register_class(GLTFMULTI_PT_MultiExportAnimationSubSubpanel)
    bpy.utils.register_class(GLTFMULTI_PT_MultiExportAnimationShapekeysSubpanel)
    bpy.utils.register_class(GLTFMULTI_PT_MultiExportAnimationSkinningSubpanel)
    bpy.utils.register_class(GLTFMULTI_PT_MultiExportGlobal)

    bpy.utils.register_class(GLTFMultiExport)

#    bpy.app.handlers.depsgraph_update_post.append(gltfmulti_scene_update)

def unregister():
    bpy.utils.unregister_class(GLTF_MultiProps)
    del bpy.types.Scene.gltfmultisettings

    bpy.utils.unregister_class(GLTFMULTI_PT_MultiExportPanel)
    bpy.utils.unregister_class(GLTFMULTI_PT_MultiExportDracoSubpanel)
    bpy.utils.unregister_class(GLTFMULTI_PT_MultiExportAnimationSubpanel)
    bpy.utils.unregister_class(GLTFMULTI_PT_MultiExportAnimationSubSubpanel)
    bpy.utils.unregister_class(GLTFMULTI_PT_MultiExportAnimationShapekeysSubpanel)
    bpy.utils.unregister_class(GLTFMULTI_PT_MultiExportAnimationSkinningSubpanel)
    bpy.utils.unregister_class(GLTFMULTI_PT_MultiExportGlobal)

    bpy.utils.unregister_class(GLTFMultiExport)

#    bpy.app.handlers.depsgraph_update_post.remove(gltfmulti_scene_update)


if __name__ == "__main__":
    register()

