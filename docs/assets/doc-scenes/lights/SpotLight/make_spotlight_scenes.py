# Copyright 2026 DreamWorks Animation LLC
# SPDX-License-Identifier: Apache-2.0

"""
Generates the SpotLight documentation scenes using the scene_rdl2 Python API.

Writes a base scene (spotlight_base.rdla) plus one scene per wedge image into
wedges/, and writes the attributes section of the SpotLight data file
(docs/_data/.../SpotLight.yml) that puts the images on the reference page.
With --render, each scene is rendered with moonray and converted to a JPEG.

Scenes reference textures/ with a relative path, so run moonray from this
directory. See ../../README.md for environment setup.
"""

import argparse
import glob
import math
import os
import shutil
import subprocess
import sys

import scene_rdl2

HERE = os.path.dirname(os.path.abspath(__file__))
DOCS_ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
IMAGE_DIR = os.path.join(DOCS_ROOT, 'assets', 'images', 'user-reference',
                         'scene-objects', 'lights', 'SpotLight')
DATA_FILE = os.path.join(DOCS_ROOT, '_data', 'user-reference', 'scene-objects',
                         'lights', 'SpotLight.yml')

GOBO_TEXTURE = os.path.join('textures', 'gobo.jpg')
CARD_TEXTURE = os.path.join('textures', 'test_card.tif')
CARD_TEXTURE_LOW = os.path.join('textures', 'test_card_16.tif')

# Where the spotlight sits and what it points at. Entries are
# (position, target, up), as passed to look_at().
SPOT_AIMS = {
    'angled': ([0.0, 7.0, 3.0], [0.0, 0.0, -1.0], [0.0, 1.0, 0.0]),
    'down': ([0.0, 7.0, -1.0], [0.0, 0.0, -1.0], [0.0, 0.0, -1.0]),
    # Start and end of the motion blur wedge's move
    'left': ([-3.0, 7.0, 3.0], [-3.0, 0.0, -1.0], [0.0, 1.0, 0.0]),
    'right': ([3.0, 7.0, 3.0], [3.0, 0.0, -1.0], [0.0, 1.0, 0.0]),
    # Low on the left, so the post casts a long shadow across the floor
    'side': ([-7.0, 4.0, -1.5], [2.0, 0.0, -1.5], [0.0, 1.0, 0.0]),
    # Low behind the props, shining at the backlit camera
    'back': ([0.0, 1.3, -5.0], [0.0, 1.2, 8.0], [0.0, 1.0, 0.0]),
}

# Cameras, as (eye, target, up, focal length):
#   main    -- the default view
#   lens    -- a wider view of the lens from outside the light cone
#   top     -- looking straight down at the floor
#   texture -- looking straight down, framed on the pool of light
#   backlit -- low, looking through the props at the 'back' light
#   shadow  -- looking straight down at the post's shadow
CAMERAS = {
    'main': ([0.0, 9.0, 16.0], [0.0, 0.5, -1.5], [0.0, 1.0, 0.0], 30.0),
    'lens': ([6.7, 3.4, -4.9], [0.0, 4.4, 1.6], [0.0, 1.0, 0.0], 16.0),
    'top': ([0.0, 40.0, -1.0], [0.0, 0.0, -1.0], [0.0, 0.0, -1.0], 28.0),
    'texture': ([0.0, 40.0, -1.0], [0.0, 0.0, -1.0], [0.0, 0.0, -1.0], 48.0),
    'backlit': ([0.0, 1.6, 8.0], [0.0, 1.0, -1.0], [0.0, 1.0, 0.0], 35.0),
    'shadow': ([1.5, 22.0, -1.5], [1.5, 0.0, -1.5], [0.0, 0.0, -1.0], 30.0),
}

# Attribute values for the base scene. SpotLight attributes not listed here
# are left at their defaults.
BASE_SPOT = {
    'intensity': 0.05,
}

# Settings shared by the texture wedges: the color test card projected
# straight down and in focus on the floor, with nothing in the way
TEXTURE_VIEW = {
    'camera': 'texture', 'spot_aim': 'down', 'wall': False, 'props': None,
    'spot': {'texture': CARD_TEXTURE, 'focal_plane_distance': 7.0, 'intensity': 0.15},
}

# Settings shared by the shadow distance wedges: a tall post lit from low on
# the left by a small lens, casting a long, crisp shadow
SHADOW_VIEW = {
    'props': 'post', 'spot_aim': 'side',
    'spot': {'lens_radius': 0.2, 'intensity': 0.08},
}


def wedge(attr, values, caption='', **overrides):
    """A wedge renders one image per value of a SpotLight attribute.

    values    -- [(value, label), ...]. A value may have a third element, a
                 dict of build_scene() arguments for that value only, plus an
                 optional 'caption'. Its 'spot' settings are added to the
                 image caption.
    caption   -- text appended to every image caption
    overrides -- build_scene() arguments for every value
    """
    return dict(attr=attr, values=values, caption=caption, overrides=overrides)


def merged(*dicts):
    """Merges build_scene() arguments, combining their 'spot' and 'scene_vars'
    settings."""
    out = {}
    for d in dicts:
        for key, value in d.items():
            if key in ('spot', 'scene_vars'):
                out[key] = dict(out.get(key, {}), **value)
            else:
                out[key] = value
    return out


WEDGES = [
    # Cone
    wedge('inner_cone_angle', [(0.0, '0'), (10.0, '10'), (30.0, '30'), (50.0, '50'),
                               (60.0, '60')],
          caption='outer_cone_angle = 60'),
    wedge('outer_cone_angle', [(30.0, '30'), (45.0, '45'), (60.0, '60'), (90.0, '90')],
          caption='inner_cone_angle = 30'),
    wedge('lens_radius', [(0.25, '0.25'), (1.0, '1'), (3.0, '3')]),
    # Seen from above with the light pointing straight down, aspect_ratio = 1
    # gives a circular pool
    wedge('aspect_ratio', [(0.5, '0.5'), (1.0, '1'), (2.0, '2')],
          caption='seen from above', camera='top', spot_aim='down', wall=False),
    wedge('focal_plane_distance', [(4.0, '4', {'caption': 'nearer than the floor'}),
                                   (8.1, '8.1', {'caption': 'at the floor'}),
                                   (1.0e10, '1e10')],
          caption='projecting a checkerboard texture', spot={'texture': GOBO_TEXTURE}),

    # Falloff. A small inner cone leaves a wide band for the falloff curve.
    wedge('angle_falloff_type', [(0, '0_off'), (1, '1_linear'), (2, '2_ease_in'),
                                 (3, '3_ease_out'), (4, '4_ease_in_out')],
          caption='inner_cone_angle = 10, outer_cone_angle = 60',
          spot={'inner_cone_angle': 10.0}),
    wedge('black_level', [(0.0, '0'), (0.001, '0.001'), (0.01, '0.01')],
          caption='lens seen from outside the cone',
          camera='lens', spot={'visible_in_camera': 1}),

    # Properties
    wedge('on', [(True, 'true'), (False, 'false')],
          caption='a dim EnvLight still lights the scene'),
    wedge('color', [([1.0, 1.0, 1.0], 'white'), ([1.0, 0.6, 0.3], 'orange'),
                    ([0.3, 0.6, 1.0], 'blue')]),
    wedge('intensity', [(0.025, '0.025'), (0.05, '0.05'), (0.1, '0.1')]),
    wedge('exposure', [(-1.0, '-1'), (0.0, '0'), (1.0, '1')], caption='intensity = 0.05'),
    # Normalized lights keep their total energy as the lens changes size. With
    # apply_scene_scale off, the same intensity suits both settings.
    wedge('normalized', [(True, 'true_r0.5', {'spot': {'lens_radius': 0.5}}),
                         (True, 'true_r1', {'spot': {'lens_radius': 1.0}}),
                         (False, 'false_r0.5', {'spot': {'lens_radius': 0.5}}),
                         (False, 'false_r1', {'spot': {'lens_radius': 1.0}})],
          spot={'apply_scene_scale': False, 'intensity': 150.0}),
    wedge('visible_in_camera', [(0, '0_force_off'), (1, '1_force_on'), (2, '2_use_default'),
                                (2, '2_use_default_enabled',
                                 {'scene_vars': {'lights_visible_in_camera': True},
                                  'caption': 'which also shows the dim EnvLight as the background'})],
          caption='lens seen from outside the cone, black_level = 0.01',
          camera='lens', spot={'black_level': 0.01},
          scene_vars={'lights_visible_in_camera': False}),
    wedge('presence_shadows', [(0, '0_force_off'), (1, '1_force_on'), (2, '2_use_default'),
                               (2, '2_use_default_enabled',
                                {'scene_vars': {'enable_presence_shadows': True}})],
          caption='sphere has presence = 0.3', props='presence',
          scene_vars={'enable_presence_shadows': False}),
    # The post spans about 4.8 to 6.6 units from the light
    wedge('min_shadow_distance', [(0.0, '0'), (0.5, '0.5'), (1.5, '1.5'), (3.0, '3')],
          caption='post lit from the left', **SHADOW_VIEW),
    wedge('max_shadow_distance', [(0.0, '0'), (3.0, '3'), (1.5, '1.5'), (0.5, '0.5')],
          caption='post lit from the left', **SHADOW_VIEW),
    wedge('clear_radius', [(0.0, '0'), (5.2, '5.2'), (5.8, '5.8'), (7.0, '7')],
          caption='post lit from the left', **SHADOW_VIEW),
    wedge('clear_radius_falloff_distance', [(0.0, '0'), (2.0, '2'), (5.0, '5')],
          caption='clear_radius = 6.5, post lit from the left',
          **merged(SHADOW_VIEW, {'spot': {'clear_radius': 6.5}})),
    wedge('clear_radius_interpolation_type',
          [(0, '0_linear'), (1, '1_exponential_up'), (2, '2_exponential_down'),
           (3, '3_smoothstep')],
          caption='clear_radius = 6.6, clear_radius_falloff_distance = 5, post lit from the left, '
                  'seen from above',
          **merged(SHADOW_VIEW, {'camera': 'shadow',
                                 'spot': {'clear_radius': 6.6,
                                          'clear_radius_falloff_distance': 5.0}})),
    # The camera's shutter is open for the whole move, so mb = false shows
    # the light where it starts
    wedge('mb', [(False, 'false'), (True, 'true')],
          caption='light moving left to right while the shutter is open',
          spot_aim='left', spot_aim_end='right', shutter=(-1.0, 0.0)),

    # Map
    wedge('texture', [('', 'none'), (CARD_TEXTURE, 'test_card')],
          **merged(TEXTURE_VIEW, {'spot': {'texture': ''}})),
    wedge('texture_filter', [(0, '0_nearest'), (1, '1_bilinear')],
          caption='16 x 16 pixel texture',
          **merged(TEXTURE_VIEW, {'spot': {'texture': CARD_TEXTURE_LOW}})),
    wedge('texture_coverage', [([1.0, 1.0], '1_1'), ([0.5, 0.5], '0.5_0.5'),
                               ([1.0, 0.5], '1_0.5')], **TEXTURE_VIEW),
    wedge('texture_reps_u', [(1.0, '1'), (2.0, '2'), (3.0, '3')], **TEXTURE_VIEW),
    wedge('texture_reps_v', [(1.0, '1'), (2.0, '2'), (3.0, '3')], **TEXTURE_VIEW),
    wedge('texture_mirror_u', [(False, 'false'), (True, 'true')], caption='texture_reps_u = 2',
          **merged(TEXTURE_VIEW, {'spot': {'texture_reps_u': 2.0}})),
    wedge('texture_mirror_v', [(False, 'false'), (True, 'true')], caption='texture_reps_v = 2',
          **merged(TEXTURE_VIEW, {'spot': {'texture_reps_v': 2.0}})),
    wedge('texture_rotation', [(0.0, '0'), (15.0, '15'), (45.0, '45')], **TEXTURE_VIEW),
    wedge('texture_translation', [([0.0, 0.0], '0_0'), ([0.25, 0.0], '0.25_0'),
                                  ([0.25, 0.5], '0.25_0.5')], **TEXTURE_VIEW),
    wedge('texture_border_color', [([1.0, 1.0, 1.0], 'white'), ([0.0, 0.0, 0.0], 'black'),
                                   ([1.0, 0.0, 1.0], 'magenta')],
          caption='texture_coverage = (0.5, 0.5)',
          **merged(TEXTURE_VIEW, {'spot': {'texture_coverage': [0.5, 0.5]}})),
    wedge('saturation', [([1.0, 1.0, 1.0], '1'), ([0.0, 0.0, 0.0], '0'),
                         ([2.0, 2.0, 2.0], '2')], **TEXTURE_VIEW),
    wedge('contrast', [([1.0, 1.0, 1.0], '1'), ([0.5, 0.5, 0.5], '0.5'),
                       ([2.0, 2.0, 2.0], '2')], **TEXTURE_VIEW),
    wedge('gamma', [([1.0, 1.0, 1.0], '1'), ([0.5, 0.5, 0.5], '0.5'),
                    ([2.0, 2.0, 2.0], '2')], **TEXTURE_VIEW),
    wedge('gain', [([1.0, 1.0, 1.0], '1'), ([0.5, 0.5, 0.5], '0.5'),
                   ([1.0, 0.5, 0.5], 'red')], **TEXTURE_VIEW),
    wedge('offset', [([0.0, 0.0, 0.0], '0'), ([0.2, 0.2, 0.2], '0.2'),
                     ([0.0, 0.0, 0.3], 'blue')], **TEXTURE_VIEW),
    wedge('temperature', [([0.0, 0.0, 0.0], '0_0_0'), ([-1.0, 0.0, 0.0], 'warm'),
                          ([1.0, 0.0, 0.0], 'cool'), ([0.0, 1.0, 0.0], 'magenta'),
                          ([0.0, 0.0, 1.0], 'brighter')], **TEXTURE_VIEW),

    # Visibility flags. The reflection flags use a glossy metal sphere and a
    # chrome sphere. The transmission flags each use one object lit from
    # behind, seen by a camera looking through it at the light.
    wedge('visible_diffuse_reflection', [(True, 'true'), (False, 'false')],
          caption='glossy and chrome spheres', props='reflect'),
    wedge('visible_glossy_reflection', [(True, 'true'), (False, 'false')],
          caption='glossy and chrome spheres', props='reflect'),
    wedge('visible_mirror_reflection', [(True, 'true'), (False, 'false')],
          caption='glossy and chrome spheres', props='reflect'),
    wedge('visible_diffuse_transmission', [(True, 'true'), (False, 'false')],
          caption='translucent card lit from behind',
          props='card', camera='backlit', spot_aim='back', wall=False),
    wedge('visible_glossy_transmission', [(True, 'true'), (False, 'false')],
          caption='frosted glass sphere lit from behind',
          props='frosted', camera='backlit', spot_aim='back', wall=False),
    wedge('visible_mirror_transmission', [(True, 'true'), (False, 'false')],
          caption='clear glass sphere lit from behind',
          props='clear', camera='backlit', spot_aim='back', wall=False),
]

# Links for attributes that are better explained elsewhere, as
# {attribute: [(url, text), ...]}
LINKS = {
    'label': [('/user-reference/how-to-guides/writing-efficient-lpes/',
               'Writing efficient LPEs')],
    'light_filters': [('/user-reference/scene-objects/light-filters/', 'Light filters')],
    'presence_shadows': [('/user-reference/how-to-guides/look-dev-transparent-surfaces/',
                          'Look dev for transparent surfaces')],
    'ray_termination': [('/user-reference/how-to-guides/ray-depth/', 'Ray depth')],
}


def normalize(v):
    length = math.sqrt(sum(c * c for c in v))
    return [c / length for c in v]


def cross(a, b):
    return [a[1] * b[2] - a[2] * b[1],
            a[2] * b[0] - a[0] * b[2],
            a[0] * b[1] - a[1] * b[0]]


def look_at(eye, target, up):
    """Row-major 4x4 transform (as a flat list) placing an object at eye with
    its local -z axis pointing at target and its local y axis towards up.
    Cameras and SpotLights both look down their local -z axis."""
    z = normalize([e - t for e, t in zip(eye, target)])
    x = normalize(cross(up, z))
    y = cross(z, x)
    return x + [0.0] + y + [0.0] + z + [0.0] + list(eye) + [1.0]


def translate(t, scale=(1.0, 1.0, 1.0)):
    return [scale[0], 0.0, 0.0, 0.0,
            0.0, scale[1], 0.0, 0.0,
            0.0, 0.0, scale[2], 0.0,
            t[0], t[1], t[2], 1.0]


def material(ctx, name, **attrs):
    """A DwaBaseMaterial, with no specular unless asked for."""
    mtl = ctx.createSceneObject('DwaBaseMaterial', name)
    mtl.set('specular', 0.0)
    for attr, value in attrs.items():
        mtl.set(attr, value)
    return mtl


def sphere(ctx, name, position, radius=1.0):
    geo = ctx.createSceneObject('SphereGeometry', name)
    geo.set('radius', radius)
    geo.set('node_xform', translate(position))
    return geo


def box(ctx, name, position, size):
    # Unit boxes are scaled with node_xform rather than BoxGeometry's size
    # attribute, whose y and z components are swapped.
    geo = ctx.createSceneObject('BoxGeometry', name)
    geo.set('node_xform', translate(position, size))
    return geo


def make_props(ctx, props):
    """Creates the objects standing on the floor. Returns [(geometry, material)]."""
    if props is None:
        return []
    if props in ('shadow', 'presence'):
        # Diffuse sphere and box; for 'presence' the sphere is mostly transparent
        sphere_mtl = material(ctx, '/materials/prop', albedo=[0.7, 0.7, 0.7])
        box_mtl = sphere_mtl
        if props == 'presence':
            sphere_mtl = material(ctx, '/materials/transparent_prop', albedo=[0.7, 0.7, 0.7],
                                  presence=0.3)
        return [(sphere(ctx, '/geometry/sphere', [-1.4, 1.0, -1.5]), sphere_mtl),
                (box(ctx, '/geometry/box', [1.5, 0.75, -0.8], (1.5, 1.5, 1.5)), box_mtl)]
    if props == 'post':
        # A tall post, for long shadows
        post_mtl = material(ctx, '/materials/prop', albedo=[0.7, 0.7, 0.7])
        return [(box(ctx, '/geometry/post', [-2.0, 1.5, -1.5], (0.6, 3.0, 0.6)), post_mtl)]
    if props == 'reflect':
        glossy = material(ctx, '/materials/glossy_metal', specular=1.0, metallic=1.0,
                          roughness=0.35)
        chrome = material(ctx, '/materials/chrome', specular=1.0, metallic=1.0,
                          roughness=0.0)
        return [(sphere(ctx, '/geometry/glossy_sphere', [-1.4, 1.0, -1.5]), glossy),
                (sphere(ctx, '/geometry/chrome_sphere', [1.5, 1.0, -0.8]), chrome)]
    # Single objects for the transmission flags, between the 'back' light and
    # the backlit camera
    if props == 'card':
        translucent = material(ctx, '/materials/translucent', albedo=[0.8, 0.8, 0.8],
                               diffuse_transmission=1.0,
                               diffuse_transmission_color=[1.0, 0.9, 0.7],
                               thin_geometry=True)
        return [(box(ctx, '/geometry/card', [0.0, 1.25, -1.0], (1.6, 2.5, 0.02)), translucent)]
    if props in ('frosted', 'clear'):
        glass = material(ctx, '/materials/%s_glass' % props, specular=1.0, transmission=1.0,
                         refractive_index=1.5, roughness=0.3 if props == 'frosted' else 0.0)
        return [(sphere(ctx, '/geometry/%s_sphere' % props, [0.0, 1.0, -1.0]), glass)]
    raise ValueError('unknown props %r' % props)


def build_scene(camera='main', spot=None, spot_aim='angled', spot_aim_end=None,
                wall=True, props='shadow', shutter=None, scene_vars=None):
    """Builds the doc scene and returns its SceneContext.

    camera       -- key into CAMERAS
    spot         -- SpotLight attribute values applied on top of BASE_SPOT
    spot_aim     -- key into SPOT_AIMS
    spot_aim_end -- key into SPOT_AIMS for the end of a motion-blurred move
    wall         -- whether to include the back wall
    props        -- which objects stand on the floor; see make_props()
    shutter      -- the camera's (mb_shutter_open, mb_shutter_close), in frames
    scene_vars   -- SceneVariables attribute values
    """
    ctx = scene_rdl2.SceneContext()

    cam = ctx.createSceneObject('PerspectiveCamera', '/camera')
    eye, target, up, focal = CAMERAS[camera]
    cam.set('node_xform', look_at(eye, target, up))
    cam.set('focal', focal)
    if shutter:
        cam.set('mb_shutter_open', shutter[0])
        cam.set('mb_shutter_close', shutter[1])

    # Floor and back wall in plain diffuse grey so the light pattern is easy to
    # read. The floor is a thick box: a very thin one shows ring artifacts
    # where the camera looks straight down at it.
    set_mtl = material(ctx, '/materials/set', albedo=[0.5, 0.5, 0.5])
    assignments = [(box(ctx, '/geometry/floor', [0.0, -1.0, 0.0], (40.0, 2.0, 40.0)), set_mtl)]
    if wall:
        assignments.append(
            (box(ctx, '/geometry/wall', [0.0, 10.0, -6.0], (40.0, 20.0, 0.2)), set_mtl))
    assignments += make_props(ctx, props)

    # Geometry must be in a GeometrySet to be rendered
    geo_set = ctx.createSceneObject('GeometrySet', '/geometry_set').toGeometrySet()
    geo_set.beginUpdate()
    for geo, _ in assignments:
        geo_set.add(geo.toGeometry())
    geo_set.endUpdate()

    # The SpotLight, plus a very dim EnvLight so unlit areas aren't pure black
    spot_light = ctx.createSceneObject('SpotLight', '/lights/spot')
    if spot_aim_end is None:
        spot_light.set('node_xform', look_at(*SPOT_AIMS[spot_aim]))
    else:
        spot_light.set('node_xform', look_at(*SPOT_AIMS[spot_aim]), 0)
        spot_light.set('node_xform', look_at(*SPOT_AIMS[spot_aim_end]), 1)
    for name, value in dict(BASE_SPOT, **(spot or {})).items():
        spot_light.set(name, value)
    fill_light = ctx.createSceneObject('EnvLight', '/lights/fill')
    fill_light.set('intensity', 0.01)

    light_set = ctx.createSceneObject('LightSet', '/light_set').toLightSet()
    light_set.beginUpdate()
    light_set.add(spot_light.toLight())
    light_set.add(fill_light.toLight())
    light_set.endUpdate()

    # The Python bindings can't set Layer assignments directly, so the Layer
    # is declared in RDLA and read into the same SceneContext
    rows = ',\n'.join(
        '    {%s("%s"), "", %s("%s"), LightSet("%s")}' % (
            geo.getSceneClass().getName(), geo.getName(),
            mtl.getSceneClass().getName(), mtl.getName(),
            light_set.getName())
        for geo, mtl in assignments)
    scene_rdl2.AsciiReader(ctx).fromString('Layer("/layer") {\n%s\n}' % rows,
                                           'layer')

    sv = ctx.getSceneVariables()
    sv.set('camera', cam)
    sv.set('layer', ctx.getSceneObject('/layer'))
    sv.set('image_width', 640)
    sv.set('image_height', 360)
    for name, value in (scene_vars or {}).items():
        sv.set(name, value)

    return ctx


def write_scene(ctx, path, note):
    """Writes ctx to path (skipping default values) under a comment header."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    scene_rdl2.writeSceneToFile(ctx, path, False, True)
    with open(path) as f:
        body = f.read()
    with open(path, 'w') as f:
        f.write('-- Generated by make_spotlight_scenes.py; edit the script, not this file.\n')
        f.write('-- %s\n\n' % note)
        f.write(body)
    print('Wrote', os.path.relpath(path, HERE))


def test_card_pixel(x, y, size):
    """The color test card: four colored quadrants, each ramping from dark
    (bottom) to full color (top), with a white "F" in the center so that
    rotation and mirroring are easy to see."""
    s = size / 256.0
    for x0, y0, x1, y1 in [(100, 64, 124, 192), (124, 64, 172, 88), (124, 116, 160, 140)]:
        if x0 * s <= x < x1 * s and y0 * s <= y < y1 * s:
            return (1.0, 1.0, 1.0)
    half = size // 2
    color = {(0, 0): (1.0, 0.15, 0.1), (1, 0): (0.1, 0.8, 0.15),
             (0, 1): (0.15, 0.3, 1.0), (1, 1): (1.0, 0.85, 0.1)}[(x // half, y // half)]
    brightness = 1.0 - 0.8 * (y % half) / (half - 1)
    return tuple(c * brightness for c in color)


def make_textures(oiiotool):
    """Creates the textures used by the scenes, if they don't exist."""
    gobo = os.path.join(HERE, GOBO_TEXTURE)
    if not os.path.exists(gobo):
        os.makedirs(os.path.dirname(gobo), exist_ok=True)
        subprocess.run([oiiotool, '--pattern', 'checker:width=32:height=32', '256x256', '3',
                        '-d', 'uint8', '-o', gobo], check=True)
        print('Wrote', GOBO_TEXTURE)
    for texture, size in [(CARD_TEXTURE, 256), (CARD_TEXTURE_LOW, 16)]:
        path = os.path.join(HERE, texture)
        if os.path.exists(path):
            continue
        ppm = os.path.splitext(path)[0] + '.ppm'
        with open(ppm, 'wb') as f:
            f.write(b'P6\n%d %d\n255\n' % (size, size))
            for y in range(size):
                f.write(bytes(int(round(255 * c))
                              for x in range(size) for c in test_card_pixel(x, y, size)))
        subprocess.run([oiiotool, ppm, '-d', 'uint8', '--compression', 'lzw', '-o', path],
                       check=True)
        os.remove(ppm)
        print('Wrote', texture)


def render(scene, image, oiiotool):
    """Renders scene with moonray and writes an sRGB JPEG to image."""
    exr = os.path.splitext(image)[0] + '.exr'
    subprocess.run(['moonray', '-in', scene, '-out', exr], cwd=HERE, check=True,
                   stdout=subprocess.DEVNULL)
    os.makedirs(os.path.dirname(image), exist_ok=True)
    subprocess.run([oiiotool, exr, '--ch', 'R,G,B', '--colorconvert', 'linear', 'sRGB',
                    '-d', 'uint8', '--quality', '90', '-o', image], check=True)
    os.remove(exr)
    print('Rendered', os.path.relpath(image, DOCS_ROOT))


def fmt(value):
    """Formats an attribute value for captions and scene comments."""
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, float):
        return ('%g' % value).replace('e+', 'e')
    if isinstance(value, (list, tuple)):
        return '(%s)' % ', '.join(fmt(float(v)) for v in value)
    if isinstance(value, str) and value.startswith('textures'):
        return os.path.basename(value)
    return str(value)


def is_default(value, default):
    if isinstance(value, str):
        return value == str(default)
    if isinstance(value, (list, tuple)):
        default = [float(v) for v in str(default).strip('[] ').split(',')]
        return all(math.isclose(a, b, rel_tol=1e-6) for a, b in zip(value, default))
    return math.isclose(float(value), float(default), rel_tol=1e-6)


def describe(attr, value, scene_class, defaults):
    """'attr = value', or for an enum 'value = name', marked if it's the default."""
    attribute = scene_class.getAttribute(attr)
    if attribute.isEnumerable():
        text = '%d = %s' % (value, attribute.getEnumDescription(value))
    else:
        text = '%s = %s' % (attr, fmt(value) if value != '' else '""')
    if is_default(value, defaults.get(attr)):
        text += ' (default)'
    return text


def wedge_jobs(defaults):
    """Returns [(attribute, scene path, image name, build_scene() arguments,
    note, caption)] for every wedge value."""
    scene_class = defaults.getSceneClass()
    jobs = []
    for w in WEDGES:
        attr = w['attr']
        for entry in w['values']:
            value, label = entry[:2]
            extra = dict(entry[2]) if len(entry) > 2 else {}
            value_caption = extra.pop('caption', '')
            args = merged(w['overrides'], extra, {'spot': {attr: value}})
            name = '%s_%s' % (attr, label)

            caption = describe(attr, value, scene_class, defaults)
            parts = ['%s = %s' % (k, fmt(v)) for k, v in extra.get('spot', {}).items()]
            parts += ['SceneVariables %s = %s' % (k, fmt(v))
                      for k, v in args.get('scene_vars', {}).items()]
            parts += [p for p in (value_caption, w['caption']) if p]
            if parts:
                caption += ', ' + ', '.join(parts)

            note = 'Base scene with SpotLight %s = %s' % (attr, fmt(value))
            others = ['%s = %s' % (k, fmt(v)) for k, v in args.get('spot', {}).items()
                      if k != attr]
            others += ['SceneVariables %s = %s' % (k, fmt(v))
                       for k, v in args.get('scene_vars', {}).items()]
            others += ['%s = %s' % (k, fmt(v)) for k, v in args.items()
                       if k not in ('spot', 'scene_vars')]
            if others:
                note += '; ' + ', '.join(others)

            jobs.append((attr, os.path.join('wedges', name + '.rdla'), name + '.jpg',
                         args, note, caption))
    return jobs


def yaml_string(text):
    return '"%s"' % text.replace('\\', '\\\\').replace('"', '\\"')


DATA_MARKER = '# Attribute images and links below are generated'


def write_data_file(jobs):
    """Rewrites the end of the SpotLight data file, from DATA_MARKER (or the
    attributes: key, the first time) onwards."""
    with open(DATA_FILE) as f:
        text = f.read()
    start = text.find(DATA_MARKER)
    if start < 0:
        start = text.index('attributes:')
    lines = [DATA_MARKER + ' by',
             '# assets/doc-scenes/lights/SpotLight/make_spotlight_scenes.py;',
             '# edit the script, not this section.',
             'attributes:']
    images = {}
    for attr, scene, image, _, _, caption in jobs:
        images.setdefault(attr, []).append((image, caption, scene))
    for attr in sorted(set(images) | set(LINKS)):
        # Quoted, since YAML would read some names (such as "on") as booleans
        lines.append('  %s:' % yaml_string(attr))
        if attr in images:
            lines.append('    images:')
            for image, caption, scene in images[attr]:
                lines += ['      - image: %s' % image,
                          '        text: %s' % yaml_string(caption),
                          '        scene: %s' % scene]
        if attr in LINKS:
            lines.append('    links:')
            for url, link_text in LINKS[attr]:
                lines += ['      - url: %s' % url,
                          '        text: %s' % yaml_string(link_text)]
    with open(DATA_FILE, 'w') as f:
        f.write(text[:start] + '\n'.join(lines) + '\n')
    print('Wrote', os.path.relpath(DATA_FILE, DOCS_ROOT))


def remove_stale(jobs):
    """Removes wedge scenes and images that are no longer generated. Only
    images named after a wedged attribute are touched."""
    keep = {os.path.join(HERE, scene) for _, scene, _, _, _, _ in jobs}
    keep |= {os.path.join(IMAGE_DIR, image) for _, _, image, _, _, _ in jobs}
    stale = glob.glob(os.path.join(HERE, 'wedges', '*.rdla'))
    for w in WEDGES:
        stale += glob.glob(os.path.join(IMAGE_DIR, w['attr'] + '_*.jpg'))
    for path in sorted(set(stale) - keep):
        os.remove(path)
        print('Removed', os.path.relpath(path, DOCS_ROOT))


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--render', action='store_true',
                        help='render each scene and write JPEGs for the docs')
    parser.add_argument('--only', metavar='ATTRS',
                        help='only write/render the base scene and the wedges for these '
                             'comma-separated attributes')
    args = parser.parse_args()
    only = set(args.only.split(',')) if args.only else None
    if only and only - {w['attr'] for w in WEDGES}:
        sys.exit('No wedges for: %s' % ', '.join(sorted(only - {w['attr'] for w in WEDGES})))

    oiiotool = shutil.which('oiiotool')
    if oiiotool is None:
        sys.exit('oiiotool not found on PATH')
    make_textures(oiiotool)

    defaults = scene_rdl2.SceneContext().createSceneObject('SpotLight', '/defaults')
    jobs = wedge_jobs(defaults)
    write_data_file(jobs)

    scenes = [('spotlight_base.rdla', 'spotlight_base.jpg', {},
               'Base SpotLight documentation scene')]
    scenes += [(scene, image, build_args, note)
               for attr, scene, image, build_args, note, _ in jobs
               if not only or attr in only]
    for scene, image, build_args, note in scenes:
        write_scene(build_scene(**build_args), os.path.join(HERE, scene), note)
        if args.render:
            render(scene, os.path.join(IMAGE_DIR, image), oiiotool)

    if not only:
        remove_stale(jobs)


if __name__ == '__main__':
    main()
