# Copyright 2026 DreamWorks Animation LLC
# SPDX-License-Identifier: Apache-2.0

"""
Renders the documentation images and videos listed in manifest.json files
under docs/assets/doc-scenes/.

Each class with generated images has a folder docs/assets/doc-scenes/<site
path>/<Class>/ containing its scenes and a manifest.json. Images are written to
the same relative path under docs/assets/images/user-reference/scene-objects/,
or to the manifest's image_dir if set. See README.md for the manifest format.

MoonRay renders aren't precisely deterministic, so an existing image or video is only
replaced if the new render looks different from it, not just noisier.

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

# Two renders look the same unless, with both shrunk to DIFF_SCALE to average
# out noise, any pixel differs by more than DIFF_HARD_FAIL, or more than
# DIFF_FAIL_PERCENT of the pixels by more than DIFF_FAIL.
DIFF_SCALE = '25%'
DIFF_FAIL = 0.008
DIFF_FAIL_PERCENT = 1
DIFF_HARD_FAIL = 0.03

ANIMATION_KEYS = ('object', 'attr', 'from', 'to', 'scenes', 'frames', 'video')


class ManifestError(Exception):
    """A manifest can't be read, is missing required keys, or names missing scene files."""


class Manifest(object):
    """A class's manifest: its scene folder, image folder and entries.

    Args:
        docs_dir (str): The docs folder.
        manifest_path (str): The class's manifest.json, under docs_dir's assets/doc-scenes/.

    Attributes:
        manifest_path (str): The manifest.json.
        scene_dir (str): The folder containing the manifest. Scene paths are relative to
            it, and scenes are rendered from it.
        name (str): The class name, which is the name of scene_dir.
        rel_dir (str): scene_dir relative to assets/doc-scenes/, for example lights/SpotLight.
        image_dir (str): The folder images and videos are written to.
        images (list[dict]): The image entries, each with at least "scene" and "image".
        animations (list[dict]): The animation entries, each with at least the keys in
            ANIMATION_KEYS.

    Raises:
        ManifestError: If the manifest can't be read or parsed, or an entry is missing
            required keys.
    """
    def __init__(self, docs_dir, manifest_path):
        self.manifest_path = manifest_path
        self.scene_dir = os.path.dirname(manifest_path)
        self.name = os.path.basename(self.scene_dir)
        self.rel_dir = os.path.relpath(self.scene_dir, os.path.join(docs_dir, SCENES_SUBDIR))
        try:
            with open(manifest_path) as f:
                data = json.load(f)
        except (OSError, ValueError) as e:
            raise ManifestError('%s: %s' % (manifest_path, e))
        self.image_dir = os.path.join(docs_dir, IMAGES_SUBDIR,
                                      data.get('image_dir', self.rel_dir))
        self.images = data.get('images', [])
        self.animations = data.get('animations', [])
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
        """Returns the attributes that have entries.

        Returns:
            set[str]: The "attr" values of the image and animation entries.
        """
        return {e['attr'] for e in self.images + self.animations if 'attr' in e}


def find_manifests(docs_dir):
    """Loads every manifest under docs_dir.

    Args:
        docs_dir (str): The docs folder.

    Returns:
        dict[str, Manifest]: The manifests, keyed by class name.

    Raises:
        ManifestError: If a manifest is invalid, or two manifests are for the same class.
    """
    pattern = os.path.join(docs_dir, SCENES_SUBDIR, '**', 'manifest.json')
    manifests = {}
    for manifest_path in sorted(glob.glob(pattern, recursive=True)):
        manifest = Manifest(docs_dir, manifest_path)
        if manifest.name in manifests:
            raise ManifestError('Two manifests for %s: %s and %s' % (
                manifest.name, manifests[manifest.name].manifest_path, manifest_path))
        manifests[manifest.name] = manifest
    return manifests


def format_value(value):
    """Formats a manifest value for rdla_wedge.

    Args:
        value (int | float | bool | list | tuple): A number, or a list of numbers for a
            color or vector.

    Returns:
        str: The value, with lists comma-separated, for example "1,0,0".

    Raises:
        TypeError: If value, or an item of it, isn't a number.
    """
    if isinstance(value, (list, tuple)):
        return ','.join('%g' % v for v in value)
    return '%g' % value


def looks_same(a, b):
    """Compares two images, ignoring render noise.

    Anything oiiotool can't compare, such as a different size, counts as different.

    Args:
        a (str): The first image.
        b (str): The second image.

    Returns:
        bool: True if the images differ only by render noise.
    """
    cmd = ['oiiotool', a, '--resize', DIFF_SCALE, b, '--resize', DIFF_SCALE,
           '--fail', str(DIFF_FAIL), '--failpercent', str(DIFF_FAIL_PERCENT),
           '--hardfail', str(DIFF_HARD_FAIL), '--diff']
    return subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def video_frames(video, frames_dir):
    """Decodes a video into PPM frames.

    Args:
        video (str): The video.
        frames_dir (str): The folder to write the frames to, which mustn't already exist.

    Returns:
        list[str]: The frames, in order.

    Raises:
        RuntimeError: If ffmpeg fails.
    """
    os.makedirs(frames_dir)
    run_checked(['ffmpeg', '-loglevel', 'error', '-i', video, os.path.join(frames_dir, 'f%04d.ppm')],
        frames_dir)
    return sorted(glob.glob(os.path.join(frames_dir, 'f*.ppm')))


def videos_look_same(a, b, tmp):
    """Compares two videos frame by frame, ignoring render noise.

    Args:
        a (str): The first video.
        b (str): The second video.
        tmp (str): A temporary folder to decode the frames into.

    Returns:
        bool: True if the videos have the same number of frames, and each pair of frames
            passes looks_same. False if either video can't be decoded.
    """
    try:
        frames_a = video_frames(a, os.path.join(tmp, 'compare_a'))
        frames_b = video_frames(b, os.path.join(tmp, 'compare_b'))
    except RuntimeError:
        return False
    return len(frames_a) == len(frames_b) and all(map(looks_same, frames_a, frames_b))


def update_file(src, dest, same, force):
    """Moves src over dest, unless dest exists and has no visible difference.

    dest is only replaced once src is complete.

    Args:
        src (str): The new file.
        dest (str): The file to replace. Its folder is created if needed.
        same (Callable[[str, str], bool]): Returns True if the two files it's given have
            no visible difference.
        force (bool): Whether to replace dest even if it has no visible difference.

    Returns:
        bool: True if dest was replaced.
    """
    if not force and os.path.exists(dest) and same(src, dest):
        return False
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    shutil.move(src, dest)
    return True


def run_checked(cmd, cwd):
    """Runs a command.

    Args:
        cmd (list[str]): The command and its arguments.
        cwd (str): The folder to run the command in.

    Returns:
        str: The command's output, with stderr merged into stdout.

    Raises:
        RuntimeError: If the command exits non-zero. The message includes the last 10
            lines of its output.
    """
    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                            universal_newlines=True)
    if result.returncode != 0:
        tail = '\n'.join(result.stdout.strip().splitlines()[-10:])
        raise RuntimeError('%s exited with %d\n%s' % (os.path.basename(cmd[0]),
                                                      result.returncode, tail))
    return result.stdout


def to_srgb(exr, image, cwd, extra_args=()):
    """Converts a rendered EXR to an 8-bit sRGB image.

    --nosoftwareattrib keeps the command line, with its local paths, out of the image's
    metadata.

    Args:
        exr (str): The EXR.
        image (str): The image to write, in the format its extension names.
        cwd (str): The folder to run oiiotool in.
        extra_args (Sequence[str]): More oiiotool arguments, such as --quality, added
            before -o.

    Raises:
        RuntimeError: If oiiotool fails.
    """
    cmd = ['oiiotool', '--nosoftwareattrib', exr, '--ch', 'R,G,B', '--colorconvert', 'linear', 'sRGB',
           '-d', 'uint8'] + list(extra_args) + ['-o', image]
    run_checked(cmd, cwd)


def render_still(manifest, entry, tmp, force):
    """Renders a still, and replaces its image if the render looks different.

    Args:
        manifest (Manifest): The manifest the entry is from.
        entry (dict): An image entry, with "scene" and "image".
        tmp (str): A temporary folder for the render.
        force (bool): Whether to replace the image even if the render looks the same.

    Returns:
        bool: True if the image was replaced.

    Raises:
        RuntimeError: If moonray or oiiotool fails.
    """
    image = os.path.join(manifest.image_dir, entry['image'])
    exr = os.path.join(tmp, 'still.exr')
    jpg = os.path.join(tmp, 'still' + os.path.splitext(image)[1])
    run_checked(['moonray', '-in', entry['scene'], '-out', exr], manifest.scene_dir)
    to_srgb(exr, jpg, manifest.scene_dir, ['--quality', '90'])
    return update_file(jpg, image, looks_same, force)


def render_animation(manifest, entry, tmp, force):
    """Renders an animation, and replaces its video if the render looks different.

    rdla_wedge only renders the frames, which are converted like stills rather than by
    rdla_wedge, whose conversion depends on oiiotool writing PNG.

    Args:
        manifest (Manifest): The manifest the entry is from.
        entry (dict): An animation entry, with the keys in ANIMATION_KEYS.
        tmp (str): A temporary folder for the frames and video.
        force (bool): Whether to replace the video even if the render looks the same.

    Returns:
        bool: True if the video was replaced.

    Raises:
        RuntimeError: If rdla_wedge, oiiotool or ffmpeg fails, or rdla_wedge writes no
            frames.
    """
    video = os.path.join(manifest.image_dir, entry['video'])
    mp4 = os.path.join(tmp, 'out.mp4')
    frames = os.path.join(tmp, 'frames')
    # rdla_wedge's shebang doesn't work on macOS, so run it with this Python,
    # which also has to be able to import scene_rdl2
    cmd = [sys.executable, shutil.which('rdla_wedge'),
           '--animate-parameter', entry['object'], entry['attr'],
           format_value(entry['from']), format_value(entry['to']),
           '--pingpong' if entry.get('pingpong') else '--inclusive']
    cmd += entry['scenes'] + [str(entry['frames']), os.path.join(frames, 'out.*.exr')]
    run_checked(cmd, manifest.scene_dir)
    exrs = sorted(glob.glob(os.path.join(frames, 'out.*.exr')))
    if not exrs:
        raise RuntimeError('rdla_wedge wrote no frames')
    for i, exr in enumerate(exrs):
        to_srgb(exr, os.path.join(frames, 'frame_%04d.ppm' % i), manifest.scene_dir)
    run_checked(['ffmpeg', '-y', '-loglevel', 'error'] + FFMPEG_ARGS[:2] +
        ['-i', os.path.join(frames, 'frame_%04d.ppm')] + FFMPEG_ARGS[2:] + [mp4],
        manifest.scene_dir)
    return update_file(mp4, video, lambda a, b: videos_look_same(a, b, tmp), force)


def animation_problem():
    """Checks whether animations can be rendered.

    Returns:
        str | None: Why animations can't be rendered, or None if they can.
    """
    if shutil.which('ffmpeg') is None:
        return 'ffmpeg not found on PATH (use --skip-animations to render stills only)'
    if subprocess.run([sys.executable, '-c', 'import scene_rdl2'],
                      stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0:
        # On macOS this usually means DYLD_LIBRARY_PATH was lost by running
        # through the shell wrapper
        return '%s can\'t import scene_rdl2, which rdla_wedge needs; see README.md' % sys.executable
    return None


def select(manifest, attrs):
    """Selects the entries of a manifest to render.

    Args:
        manifest (Manifest): The manifest to select from.
        attrs (set[str] | None): The attributes whose entries to render, or None for every
            entry. Image entries without an "attr" are only rendered for None.

    Returns:
        tuple[list[dict], list[dict]]: The image entries and the animation entries.
    """
    if attrs is None:
        return manifest.images, manifest.animations
    return ([e for e in manifest.images if e.get('attr') in attrs],
            [e for e in manifest.animations if e['attr'] in attrs])


def check_scenes(manifest, images, animations):
    """Checks that the scene files of entries exist.

    Args:
        manifest (Manifest): The manifest the entries are from.
        images (list[dict]): Image entries.
        animations (list[dict]): Animation entries.

    Raises:
        ManifestError: If any scene files are missing. The message lists them.
    """
    scenes = [e['scene'] for e in images]
    scenes += [s for e in animations for s in e['scenes']]
    missing = sorted({s for s in scenes if not os.path.isfile(os.path.join(manifest.scene_dir, s))})
    if missing:
        raise ManifestError('%s: missing scene files: %s' % (manifest.name, ', '.join(missing)))


def parse_args():
    """Parses the command line, exiting with a usage error if it's invalid.

    Returns:
        argparse.Namespace: The parsed arguments.
    """
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
    parser.add_argument('--force', action='store_true',
                        help='replace existing images and videos even if the new render looks the '
                             'same, for example after changing encoding settings')
    args = parser.parse_args()
    if args.attr and not args.class_name:
        parser.error('--attr needs -c')
    return args


def main():
    """Runs the tool from the command line.

    Exits with an error message, before rendering anything, if a manifest is invalid or a
    tool is missing. Otherwise renders every selected entry, and exits with status 1 if
    any of them failed.
    """
    args = parse_args()
    docs_dir = os.path.abspath(args.dir)
    try:
        manifests = find_manifests(docs_dir)
    except ManifestError as e:
        sys.exit('Error: %s' % e)

    if args.list:
        for name, manifest in sorted(manifests.items()):
            print('%-30s %-40s %4d images %3d videos'
                  % (name, manifest.rel_dir, len(manifest.images), len(manifest.animations)))
        return

    if args.class_name:
        if args.class_name not in manifests:
            sys.exit('Error: no manifest for %s under %s'
                     % (args.class_name, os.path.join(docs_dir, SCENES_SUBDIR)))
        selected = [manifests[args.class_name]]
    else:
        selected = [manifest for _, manifest in sorted(manifests.items())]

    attrs = set(args.attr.split(',')) if args.attr else None
    if attrs and attrs - selected[0].attrs():
        sys.exit('Error: no %s entries for: %s'
                 % (selected[0].name, ', '.join(sorted(attrs - selected[0].attrs()))))

    jobs = []
    try:
        for manifest in selected:
            images, animations = select(manifest, attrs)
            if args.skip_animations:
                animations = []
            check_scenes(manifest, images, animations)
            jobs.append((manifest, images, animations))
    except ManifestError as e:
        sys.exit('Error: %s' % e)

    if args.dry_run:
        for manifest, images, animations in jobs:
            for e in images:
                print('%s: %s -> %s' % (manifest.name, e['scene'],
                                        os.path.relpath(os.path.join(manifest.image_dir, e['image']))))
            for e in animations:
                print('%s: %s %s %s..%s over %s -> %s'
                      % (manifest.name, e['object'], e['attr'], format_value(e['from']),
                         format_value(e['to']), ' '.join(e['scenes']),
                         os.path.relpath(os.path.join(manifest.image_dir, e['video']))))
        return

    has_animations = any(animations for _, _, animations in jobs)
    tools = ['moonray', 'oiiotool'] + (['rdla_wedge'] if has_animations else [])
    missing = [t for t in tools if shutil.which(t) is None]
    if missing:
        sys.exit('Error: not found on PATH: %s' % ', '.join(missing))
    problem = animation_problem() if has_animations else None

    failures = []
    replaced = []
    for manifest, images, animations in jobs:
        for entry in images + animations:
            is_video = 'video' in entry
            output = os.path.relpath(
                os.path.join(manifest.image_dir, entry['video' if is_video else 'image']), docs_dir)
            # rdla_wedge always works in /tmp/rdla_wedge, so renders run one at a time
            with tempfile.TemporaryDirectory() as tmp:
                try:
                    if is_video and problem:
                        raise RuntimeError(problem)
                    render = render_animation if is_video else render_still
                    replaced.append(render(manifest, entry, tmp, args.force))
                    print('Updated' if replaced[-1] else 'Unchanged', output)
                except RuntimeError as e:
                    failures.append((output, str(e)))
                    print('FAILED', output)

    print('\n%d updated, %d unchanged (no visible difference from the existing file)'
          % (replaced.count(True), replaced.count(False)))
    if failures:
        print('\n%d failed:' % len(failures))
        for output, message in failures:
            print('  %s: %s' % (output, message.replace('\n', '\n    ')))
        sys.exit(1)


if __name__ == '__main__':
    main()
