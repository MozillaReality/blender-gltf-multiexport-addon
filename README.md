# webxr-tools

Small tools that may be useful for WebXR and WebGL development

## Blender scripts

### copy_position, copy_rotation, copy_scale

Copy to clipboard the position, rotation or scale of the selected object
```js
// Example output:
1, 4.3, 24
```
### copy_geometry

Copy to clipboard a Javascript object with the name, vertices and faces of the selected object.
```js
// Example output:
var object = {
  name: "Plane",
  vertices: [-1.56, 0.0, 1.56, 1.56, 0.0, 1.56, -1.56, 0.0, -1.56, 1.56, 0.0, -1.56],
  faces: [0, 1, 3, 2]
}
```

### vertex_color_to_selection

Allows to apply a specific color to the selected vertices.



## Basis viewer

