# Documentation scenes

Small MoonRay scenes used to make the images in the attribute reference, and
for you to download and experiment with. Each scene object type has its own
folder, following the layout of `user-reference/scene-objects`:

```
doc-scenes/
  lights/SpotLight/
    make_spotlight_scenes.py   # builds every scene in this folder
    manifest.json              # the images and videos to render from them
    spotlight_base.rdla        # the base scene
    wedges/*.rdla              # the base scene with one attribute changed
    textures/                  # textures referenced by the scenes
```

Each `wedges/<attribute>_<value>.rdla` file is the scene behind the image
`<attribute>_<value>.jpg` on that object's reference page. The comment at the top
of each scene says which value it uses.

## Rendering a scene

Scenes reference textures with relative paths, so render from the scene's
folder:

```bash
source /path/to/openmoonray/scripts/setup.sh
cd lights/SpotLight
moonray -in wedges/lens_radius_3.rdla -out lens_radius_3.exr
```

## Regenerating scenes and images

This takes two steps: generate the scenes, then render them.

**1. Generate the scenes.** The scenes are not edited by hand. The Python
script next to them builds them with the `scene_rdl2` Python API. It also
writes:

- the part of the object's data file (`docs/_data/user-reference/...`) that
  puts the images and videos, their captions and their scene links on the
  reference page
- `manifest.json`, which lists the images and videos to render

A full run (without `--only`) removes scenes, images and videos that are no
longer in the script. It needs `oiiotool` on `PATH` to make the textures.

```bash
source /path/to/openmoonray/scripts/setup.sh
export PYTHONPATH=/path/to/openmoonray/python/lib/python3.9:$PYTHONPATH
cd lights/SpotLight
python3 make_spotlight_scenes.py
python3 make_spotlight_scenes.py --only lens_radius,color   # just these wedges
```

**2. Render them** with [`cmd/generate_doc_images`](../../../cmd/generate_doc_images/README.md),
which reads `manifest.json` and writes the images and videos into
`docs/assets/images/user-reference/...`:

```bash
cmd/generate_doc_images/generate_doc_images -c SpotLight
cmd/generate_doc_images/generate_doc_images -c SpotLight --attr lens_radius,color
```

Stills need `moonray` and `oiiotool` on `PATH`. Videos also need `ffmpeg` and
MoonRay's `rdla_wedge`.

MoonRay renders aren't bit-for-bit repeatable, so every re-rendered image
differs slightly from the last one and is stored again in Git LFS. Re-render
only the attributes you changed, with `--attr`.

To change what's shown for an attribute, edit its entry in the script's
`WEDGES` list (or `ANIMATIONS` for videos), then run both steps again.

Use the Python version the `scene_rdl2` bindings were built against (3.9 for
current releases).

### macOS notes

The macOS bindings link against Xcode's `Python3.framework`. Run the framework's
interpreter directly and point it at the MoonRay libraries.
`/usr/bin/python3` won't work because macOS strips `DYLD_LIBRARY_PATH`
from it.

```bash
export DYLD_LIBRARY_PATH=/path/to/openmoonray/lib
PY=/Applications/Xcode.app/Contents/Developer/Library/Frameworks/Python3.framework/Versions/3.9/bin/python3.9
$PY make_spotlight_scenes.py
$PY /path/to/openmoonray-docs/cmd/generate_doc_images/generate_doc_images.py -c SpotLight
```

Run `generate_doc_images.py` with `$PY` rather than through the
`generate_doc_images` wrapper. The wrapper's shell also loses
`DYLD_LIBRARY_PATH`, which `rdla_wedge` needs to import `scene_rdl2`.

`oiiotool` is in the `bin` directory of the MoonRay dependency install, e.g.
`/Applications/MoonRay/installs/bin`.

## Writing a new scene script

Some things that aren't obvious from the `scene_rdl2` Python bindings:

- Geometry must be added to a `GeometrySet`, or it won't render.
  `GeometrySet.add()` and `LightSet.add()` must be called between
  `beginUpdate()` and `endUpdate()`.
- `Layer` assignments can't be set from Python. Declare the `Layer` as an RDLA
  string and load it into the same `SceneContext` with
  `scene_rdl2.AsciiReader(ctx).fromString(...)`.
- Pass vector, color, and matrix values to `set()` as plain Python lists. A
  `Mat4d` is a flat list of 16 numbers in row-major order, with the
  translation in the last row. Passing `scene_rdl2.Rgb`/`Vec3f` objects writes
  garbage values without raising an error.
- `BoxGeometry`'s `size` attribute swaps y and z. Scale a unit box with
  `node_xform` instead. Very thin boxes, such as a floor 0.2 units thick, can
  show ring artifacts where the camera looks straight down at them, so make
  floors thicker.
- Cameras and lights point down their local -z axis.
