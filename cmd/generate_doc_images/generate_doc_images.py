# Copyright 2026 DreamWorks Animation LLC
# SPDX-License-Identifier: Apache-2.0

"""
Renders the documentation images and videos listed in manifest.json files
under docs/assets/doc-scenes/.

Each class with generated images has a folder docs/assets/doc-scenes/<site
path>/<Class>/ containing its scenes and a manifest.json. Images are written to
the same relative path under docs/assets/images/user-reference/scene-objects/,
or to the manifest's image_dir if set. See README.md for the manifest format.

Stills need moonray and oiiotool on PATH. Animations also need ffmpeg and
rdla_wedge, and must be run with a Python that can import scene_rdl2.
"""

import argparse
import glob
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DOCS_DIR = os.path.abspath(os.path.join(HERE, '..', '..', 'docs'))
SCENES_SUBDIR = os.path.join('assets', 'doc-scenes')
IMAGES_SUBDIR = os.path.join('assets', 'images', 'user-reference', 'scene-objects')

# The same settings rdla_wedge uses for its own MP4 output
FFMPEG_ARGS = ['-framerate', '10', '-vf', 'format=yuv420p', '-c:v', 'libx264', '-crf', '18']

ANIMATION_KEYS = ('object', 'attr', 'from', 'to', 'scenes', 'frames', 'video')


class ManifestError(Exception):
    pass


class DocClass(object):
    """A class with a manifest: its scene folder, image folder and entries."""
    def __init__(self, docs_dir, manifest_path):
        self.manifest_path = manifest_path
        self.scene_dir = os.path.dirname(manifest_path)
        self.name = os.path.basename(self.scene_dir)
        self.rel_dir = os.path.relpath(self.scene_dir, os.path.join(docs_dir, SCENES_SUBDIR))
        try:
            with open(manifest_path) as f:
                manifest = json.load(f)
        except (OSError, ValueError) as e:
            raise ManifestError('%s: %s' % (manifest_path, e))
        self.image_dir = os.path.join(docs_dir, IMAGES_SUBDIR,
                                      manifest.get('image_dir', self.rel_dir))
        self.images = manifest.get('images', [])
        self.animations = manifest.get('animations', [])
        for entry in self.images:
            if 'scene' not in entry or 'image' not in entry:
                raise ManifestError('%s: images need "scene" and "image": %s'
                                    % (manifest_path, entry))
        for entry in self.animations:
            missing = [k for k in ANIMATION_KEYS if k not in entry]
            if missing:
                raise ManifestError('%s: animation is missing %s: %s'
                                    % (manifest_path, ', '.join(missing), entry))

    def attrs(self):
        return {e['attr'] for e in self.images + self.animations if 'attr' in e}


def find_classes(docs_dir):
    """Returns {class name: DocClass} for every manifest under docs_dir."""
    pattern = os.path.join(docs_dir, SCENES_SUBDIR, '**', 'manifest.json')
    classes = {}
    for path in sorted(glob.glob(pattern, recursive=True)):
        cls = DocClass(docs_dir, path)
        if cls.name in classes:
            raise ManifestError('Two manifests for %s: %s and %s'
                                % (cls.name, classes[cls.name].manifest_path, path))
        classes[cls.name] = cls
    return classes


def format_value(value):
    """Formats a manifest value for rdla_wedge: lists become comma-separated."""
    if isinstance(value, (list, tuple)):
        return ','.join('%g' % v for v in value)
    return '%g' % value


def replace_file(src, dest):
    """Moves src over dest, so dest is only replaced once src is complete."""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.move(src, dest)


def run(cmd, cwd):
    """Runs cmd, raising RuntimeError with the end of its output on failure."""
    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True)
    if result.returncode != 0:
        tail = '\n'.join(result.stdout.strip().splitlines()[-10:])
        raise RuntimeError('%s exited with %d\n%s' % (os.path.basename(cmd[0]),
                                                      result.returncode, tail))
    return result.stdout


def to_srgb(exr, image, cwd, extra_args=()):
    """Converts a rendered EXR to an 8-bit sRGB image. --nosoftwareattrib keeps
    the command line, with its local paths, out of the image's metadata."""
    run(['oiiotool', '--nosoftwareattrib', exr, '--ch', 'R,G,B', '--colorconvert', 'linear', 'sRGB',
         '-d', 'uint8'] + list(extra_args) + ['-o', image], cwd)


def render_still(cls, entry, tmp):
    image = os.path.join(cls.image_dir, entry['image'])
    exr = os.path.join(tmp, 'still.exr')
    jpg = os.path.join(tmp, 'still' + os.path.splitext(image)[1])
    run(['moonray', '-in', entry['scene'], '-out', exr], cls.scene_dir)
    to_srgb(exr, jpg, cls.scene_dir, ['--quality', '90'])
    replace_file(jpg, image)


def oiiotool_writes_png():
    help_text = subprocess.run(['oiiotool', '--help'], stdout=subprocess.PIPE,
                               universal_newlines=True).stdout
    for line in help_text.splitlines():
        if line.startswith('Output formats supported:'):
            return 'png' in line.split(':', 1)[1].replace(',', ' ').split()
    return False


def render_animation(cls, entry, tmp, rdla_wedge, png):
    video = os.path.join(cls.image_dir, entry['video'])
    mp4 = os.path.join(tmp, 'out.mp4')
    # rdla_wedge's shebang doesn't work on macOS, so run it with this Python,
    # which also has to be able to import scene_rdl2
    cmd = [sys.executable, rdla_wedge,
           '--animate-parameter', entry['object'], entry['attr'],
           format_value(entry['from']), format_value(entry['to']),
           '--pingpong' if entry.get('pingpong') else '--inclusive']
    cmd += entry['scenes'] + [str(entry['frames'])]
    if png:
        run(cmd + [mp4], cls.scene_dir)
    else:
        frames = os.path.join(tmp, 'frames')
        run(cmd + [os.path.join(frames, 'out.*.exr')], cls.scene_dir)
        exrs = sorted(glob.glob(os.path.join(frames, 'out.*.exr')))
        if not exrs:
            raise RuntimeError('rdla_wedge wrote no frames')
        for i, exr in enumerate(exrs):
            to_srgb(exr, os.path.join(frames, 'frame_%04d.ppm' % i), cls.scene_dir)
        run(['ffmpeg', '-y', '-loglevel', 'error'] + FFMPEG_ARGS[:2] +
            ['-i', os.path.join(frames, 'frame_%04d.ppm')] + FFMPEG_ARGS[2:] + [mp4],
            cls.scene_dir)
    # rdla_wedge returns success even when its conversion fails
    if not os.path.exists(mp4):
        raise RuntimeError('no video was written')
    replace_file(mp4, video)


def select(cls, attrs):
    """Returns the image and animation entries of cls to render."""
    if attrs is None:
        return cls.images, cls.animations
    return ([e for e in cls.images if e.get('attr') in attrs],
            [e for e in cls.animations if e['attr'] in attrs])


def check_scenes(cls, images, animations):
    scenes = [e['scene'] for e in images]
    scenes += [s for e in animations for s in e['scenes']]
    missing = sorted({s for s in scenes if not os.path.isfile(os.path.join(cls.scene_dir, s))})
    if missing:
        raise ManifestError('%s: missing scene files: %s' % (cls.name, ', '.join(missing)))


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    which = parser.add_mutually_exclusive_group(required=True)
    which.add_argument('-a', '--all', action='store_true',
                       help='render every class with a manifest')
    which.add_argument('-c', '--class', dest='class_name',
                       help='render one class')
    which.add_argument('--list', action='store_true',
                       help='list the classes with manifests, and their image and video counts')
    parser.add_argument('--attr', metavar='ATTRS',
                        help='with -c, only render entries for these comma-separated attributes')
    parser.add_argument('-d', '--dir', default=DEFAULT_DOCS_DIR,
                        help='the docs folder (default: %(default)s)')
    parser.add_argument('--dry-run', action='store_true',
                        help='show what would be rendered, without rendering')
    parser.add_argument('--skip-animations', action='store_true',
                        help='render stills only, for machines without ffmpeg')
    args = parser.parse_args()
    if args.attr and not args.class_name:
        parser.error('--attr needs -c')
    return args


def main():
    args = parse_args()
    docs_dir = os.path.abspath(args.dir)
    try:
        classes = find_classes(docs_dir)
    except ManifestError as e:
        sys.exit('Error: %s' % e)

    if args.list:
        for name, cls in sorted(classes.items()):
            print('%-30s %-40s %4d images %3d videos'
                  % (name, cls.rel_dir, len(cls.images), len(cls.animations)))
        return

    if args.class_name:
        if args.class_name not in classes:
            sys.exit('Error: no manifest for %s under %s'
                     % (args.class_name, os.path.join(docs_dir, SCENES_SUBDIR)))
        selected = [classes[args.class_name]]
    else:
        selected = [cls for _, cls in sorted(classes.items())]

    attrs = set(args.attr.split(',')) if args.attr else None
    if attrs and attrs - selected[0].attrs():
        sys.exit('Error: no %s entries for: %s'
                 % (selected[0].name, ', '.join(sorted(attrs - selected[0].attrs()))))

    jobs = []
    try:
        for cls in selected:
            images, animations = select(cls, attrs)
            if args.skip_animations:
                animations = []
            check_scenes(cls, images, animations)
            jobs.append((cls, images, animations))
    except ManifestError as e:
        sys.exit('Error: %s' % e)

    if args.dry_run:
        for cls, images, animations in jobs:
            for e in images:
                print('%s: %s -> %s' % (cls.name, e['scene'],
                                        os.path.relpath(os.path.join(cls.image_dir, e['image']))))
            for e in animations:
                print('%s: %s %s %s..%s over %s -> %s'
                      % (cls.name, e['object'], e['attr'], format_value(e['from']),
                         format_value(e['to']), ' '.join(e['scenes']),
                         os.path.relpath(os.path.join(cls.image_dir, e['video']))))
        return

    tools = ['moonray', 'oiiotool']
    if any(animations for _, _, animations in jobs):
        tools.append('rdla_wedge')
    missing = [t for t in tools if shutil.which(t) is None]
    if missing:
        sys.exit('Error: not found on PATH: %s' % ', '.join(missing))
    animation_problem = None
    rdla_wedge = shutil.which('rdla_wedge')
    if shutil.which('ffmpeg') is None:
        animation_problem = 'ffmpeg not found on PATH (use --skip-animations to render stills only)'
    elif rdla_wedge and subprocess.run([sys.executable, '-c', 'import scene_rdl2'],
                                       stdout=subprocess.DEVNULL,
                                       stderr=subprocess.DEVNULL).returncode != 0:
        # On macOS this usually means DYLD_LIBRARY_PATH was lost by running
        # through the shell wrapper
        animation_problem = ('%s can\'t import scene_rdl2, which rdla_wedge needs; see README.md'
                             % sys.executable)
    png = rdla_wedge is not None and oiiotool_writes_png()

    failures = []
    for cls, images, animations in jobs:
        for entry in images:
            image = os.path.relpath(os.path.join(cls.image_dir, entry['image']), docs_dir)
            with tempfile.TemporaryDirectory() as tmp:
                try:
                    render_still(cls, entry, tmp)
                    print('Rendered', image)
                except RuntimeError as e:
                    failures.append((image, str(e)))
                    print('FAILED', image)
        for entry in animations:
            video = os.path.relpath(os.path.join(cls.image_dir, entry['video']), docs_dir)
            if animation_problem:
                failures.append((video, animation_problem))
                print('FAILED', video)
                continue
            # rdla_wedge always works in /tmp/rdla_wedge, so animations run one at a time
            with tempfile.TemporaryDirectory() as tmp:
                try:
                    render_animation(cls, entry, tmp, rdla_wedge, png)
                    print('Rendered', video)
                except RuntimeError as e:
                    failures.append((video, str(e)))
                    print('FAILED', video)

    if failures:
        print('\n%d failed:' % len(failures))
        for path, message in failures:
            print('  %s: %s' % (path, message.replace('\n', '\n    ')))
        sys.exit(1)


if __name__ == '__main__':
    main()
