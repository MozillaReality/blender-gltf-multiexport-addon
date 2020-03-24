# WebXR Tools

Small tools that may be useful for WebXR and WebGL development



## Blender scripts

### webxr-tools

Add-on with a set of operators and features:

* Clipboard tools

Copies to the clipboard the position, rotation or scale of the selected object
```js
// Example output:
1, 4.3, 24
```

It can also copy the **geometry** (vertices and faces) of the selected object.
```js
// Example output:
var Plane = {
  vertices: [-1.56, 0.0, 1.56, 1.56, 0.0, 1.56, -1.56, 0.0, -1.56, 1.56, 0.0, -1.56],
  faces: [0, 1, 3, 2]
}
```

### vertex_color_to_selection

Allows to apply a specific color to the selected vertices.



## Texture viewer

Basic texture viewer. Drag and drop an image file to inspect it. Supports .Basis textures

1. Start a webserver on the folder and open localhost in a browser.
2. Drag and drop a image or .basis file on the page (WIP: maybe you have to do it twice)

Controls:
* `+` and `-` to **zoom**
* Use cursor keys to **pan**
