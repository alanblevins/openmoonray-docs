SpotLight models a physically plausible spotlight mechanism that works like a projector, with an imaginary lens,
and a focal plane at which the projected image (a texture, if assigned, otherwise a pool of light) will be
in focus.

The position of the SpotLight corresponds to the center of the lens, and the orientation is such that the
light is projected out along the SpotLight's negative local z-axis, the same direction a camera looks.

The extent of the light cone is controlled by two attributes, _inner_cone_angle_ and _outer_cone_angle_, which
describe the full side-to-side angular extents, in degrees, of the inner and outer regions of the beam of
light. The inner region is the portion where the projected light is at full strength (as set by _color_,
_intensity_ and _exposure_), and the outer cone is the boundary beyond which no light is cast. Interpolation
between the inner and outer regions is controlled by the _angle_falloff_type_ attribute.

The lens has a size, set by _lens_radius_ and _aspect_ratio_, and behaves like an area light: a larger lens gives
softer shadows and a softer edge to the pool of light. It also means a projected texture is only sharp on
surfaces at _focal_plane_distance_, which by default is effectively infinite.

Note that the above description implies that when viewing the lens itself from outside the cone, assuming the
light is made visible using the _visible_in_camera_ attribute, the lens will appear black. To better mimic the
slight glow that would be visible for a real spotlight lens under such conditions, the _black_level_ attribute
can be set to a small non-zero value. This attribute is merely provided as a convenience for visualization,
however, and has no effect on the illumination of the scene.

The images in the attribute reference below were rendered from small example scenes, which you can download
from the _scene_ link under each image or from [Example scenes](#example-scenes).
