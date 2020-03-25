# Blender Add-ons for WebXR

Small Blender Add-ons that may be useful for WebXR and WebGL development


## Clipboard tools

![screenshot](./doc/clipboardtools.png)

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


