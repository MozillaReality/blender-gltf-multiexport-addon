bl_info = {
    "name": "WebXR Tools",
    "author": "Diego F. Goberna",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Tools",
    "description": "Set of tools to help with WebXR & WebGL development",
    "warning": "",
    "wiki_url": "",
    "category": "Import-Export",
}

from . import clipboard_tools

def register():
  clipboard_tools.register()

def unregister():
  clipboard_tools.unregister()
