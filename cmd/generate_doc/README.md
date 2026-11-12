Generates Moonray class documentation by filling in a template using data obtained through the scene_rdl2 Python
bindings.

Before running this you'll want to pick up the latest openmoonray release, and make sure you have jinja2 available:
```bash
rez-env openmoonray jinja2
```

To run the script from this directory:
```bash
./generate_doc -a -d ../../docs/
```

Generate docs for a specific class: `./generate_doc -c DwaBaseMaterial -d <docs_path>`

Generate docs for all classes with the given interface: `./generate_doc -i LIGHT -d <docs_path>`

Generate docs for all classes: `./generate_doc -a -d <docs_path>`

Add `--images` with `-a` or `-c` to also render the classes' documentation images and videos with
[generate_doc_images](../generate_doc_images/README.md), e.g. `./generate_doc -c SpotLight -d <docs_path> --images`.
Only classes with a `manifest.json` have images to render. Rendering is slow, so it's off by default.

Documentation for template format: [jinja](https://jinja.palletsprojects.com/en/3.1.x/templates/)


