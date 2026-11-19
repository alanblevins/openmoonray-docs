Renders the documentation images and videos listed in `manifest.json` files under `docs/assets/doc-scenes/`.
How the scenes and manifests are made is up to each class (see
[docs/assets/doc-scenes/README.md](../../docs/assets/doc-scenes/README.md)); this tool only renders them.

To run it from any directory:
```bash
./generate_doc_images -a                                     # every class with a manifest
./generate_doc_images -c SpotLight                           # one class
./generate_doc_images -c SpotLight --attr lens_radius,color  # some attributes of one class
```

Other options:
- `-d <docs_path>` sets the docs folder. The default is the `docs` folder of this repo.
- `--list` lists the classes that have manifests, with their image and video counts.
- `--dry-run` shows what would be rendered.
- `--skip-animations` renders stills only, for machines without `ffmpeg`.
- `--force` replaces existing images and videos even when the new render looks the same, for example after changing
  the JPEG or video encoding settings.

`./generate_doc -c <Class> -d <docs_path> --images` (or `-a --images`) in `cmd/generate_doc` runs this tool after
writing the pages.

An existing image is only replaced once its new render has succeeded, and only if it looks different. If a render
fails, the others still run, and the failures are listed at the end with a non-zero exit code. Images removed from a
manifest aren't deleted; whoever edits the manifest, by hand or with a script, is responsible for that.

## Unchanged renders

MoonRay renders aren't bit-for-bit repeatable, so every render of a scene differs slightly from the last. To avoid
storing those copies in Git LFS again, each render is compared with the existing file, and the file is left alone
(reported as `Unchanged`) unless there's a visible difference. Both images are shrunk to 25% with `oiiotool`, which
averages out most of the noise, and they differ if any pixel differs by more than 0.03, or more than 1% of pixels by
more than 0.008. A video differs if its frame count differs or any frame does.

## Requirements

- Stills: `moonray` and `oiiotool` on `PATH`. The tool itself only uses the Python standard library.
- Videos: also `ffmpeg` and MoonRay's `rdla_wedge` on `PATH`, and a Python that can import `scene_rdl2`, since
  `rdla_wedge` is run with the same Python as this tool. The wrapper uses `${PYTHON:-python3}`.

On macOS, run `generate_doc_images.py` directly with a Python that can import `scene_rdl2`. The `generate_doc_images`
wrapper runs through `/bin/sh`, which loses `DYLD_LIBRARY_PATH`, so `rdla_wedge` can't import `scene_rdl2`.

## Manifest

A class's folder is `docs/assets/doc-scenes/<site path>/<Class>/`, for example `lights/SpotLight/`. Its images go to
the same path under `docs/assets/images/user-reference/scene-objects/`, unless the manifest sets `image_dir` (relative
to that folder), for a class whose images are elsewhere. Scene paths are relative to the manifest's folder, and scenes
are rendered from there, so relative texture paths work.

```json
{
  "images": [
    {"scene": "spotlight_base.rdla", "image": "spotlight_base.jpg"},
    {"attr": "lens_radius", "scene": "scenes/lens_radius_3.rdla", "image": "lens_radius_3.jpg"}
  ],
  "animations": [
    {"object": "/lights/spot", "attr": "outer_cone_angle", "from": 30.0, "to": 90.0,
     "scenes": ["spotlight_base.rdla"], "frames": 16, "pingpong": true,
     "video": "outer_cone_angle_anim.mp4"}
  ]
}
```

- **Images:** `attr` is optional, and only used by `--attr`.
- **Animations:** the attribute `attr` of the object named `object` is animated from `from` to `to` over `frames`
  frames of `scenes`, using `rdla_wedge --animate-parameter`. Colors and vectors are lists, such as
  `"from": [1, 0, 0]`. With `pingpong`, it animates there and back; otherwise the last frame reaches `to`. `scenes`
  can list more than one file, with later files overriding earlier ones, for example to lower the resolution. Videos
  are H.264 MP4 at 10 frames per second, with the same settings `rdla_wedge` uses. They use the yuv420p pixel format,
  which browsers need, and which stores color at half the width and height of the image, so the scene's width and
  height must be even.

The tool doesn't check entries against the class's attributes, and doesn't read or write the class's data file. Add
images to the page with `images:` and videos with `videos:` entries in the data file, as usual.
