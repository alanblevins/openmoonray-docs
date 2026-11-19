---
title: SpotLight

# uncomment if you want MathJax formatting available
# maths: 1

# format is YYYY-MM-DD 00:00:00 +0000
# last-modified-date: 2025-02-14 00:00:00 +0000
---
# SpotLight
{%-include overview.html data=site.data.user-reference.scene-objects.lights.SpotLight-%}
{%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.gallery data=site.data.user-reference.scene-objects.lights.SpotLight-%}
{%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.links-%}
---
## Attribute Reference

<div class="scene-class">
<details open>
  <summary>Cone attributes</summary>
  <p>
    <h3>aspect_ratio</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 1.0
      <p class="scene-class-comments">The aspect ratio of the lens - its local x dimension divided by its local y dimension. Values other than 1.0 will give the lens a non-circular elliptical shape.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.aspect_ratio.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.aspect_ratio.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.aspect_ratio.links heading=4-%}
    </p>
    <h3>focal_plane_distance</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 10000000000.0
      <p class="scene-class-comments">The distance from the SpotLight's position, measured in the direction the light is pointing, at which the projected image will be in focus. The default is effectively infinite, so the projection is blurred unless lens_radius is very small. To project a sharp texture, set this to the distance from the light to the surface being lit.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.focal_plane_distance.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.focal_plane_distance.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.focal_plane_distance.links heading=4-%}
    </p>
    <h3>inner_cone_angle</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 30.0
      <p class="scene-class-comments">The apex angle, in degrees, of the bright inner cone of the light emitted by the SpotLight. Full illumination takes place inside this region. This is a full angle, measured from one side to the other. Values greater than outer_cone_angle are clamped to outer_cone_angle. There is a falloff function applied between the outer and inner cones - see the angle_falloff_type attribute.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.inner_cone_angle.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.inner_cone_angle.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.inner_cone_angle.links heading=4-%}
    </p>
    <h3>lens_radius</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 1.0
      <p class="scene-class-comments">The radius of the SpotLight's lens along its local x axis. The radius along its local y axis is lens_radius / aspect_ratio.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.lens_radius.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.lens_radius.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.lens_radius.links heading=4-%}
    </p>
    <h3>outer_cone_angle</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 60.0
      <p class="scene-class-comments">The apex angle, in degrees, of the bounding cone of the light emitted by the SpotLight. No illumination takes place outside this angle. This is a full angle, measured from one side to the other. There is a falloff function applied between the outer and inner cones - see the angle_falloff_type attribute.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.outer_cone_angle.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.outer_cone_angle.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.outer_cone_angle.links heading=4-%}
    </p>
  </p>
</details>
<details open>
  <summary>Falloff attributes</summary>
  <p>
    <h3>angle_falloff_type</h3>
    <p class="scene-class-type">
      <b>Int</b> <i>enum</i>
      <br>
          &nbsp;&nbsp;0 = &ldquo;off&rdquo;<br>
          &nbsp;&nbsp;1 = &ldquo;linear&rdquo;<br>
          &nbsp;&nbsp;2 = &ldquo;ease in&rdquo;<br>
          &nbsp;&nbsp;3 = &ldquo;ease out&rdquo;<br>
          &nbsp;&nbsp;4 = &ldquo;ease in/out&rdquo; (default)<br>
      <p class="scene-class-comments">The falloff function applied between the outer and inner cones. To calculate this, the angle from the cone's axis to the the point being illuminated is measured as seen from the SpotLight's position. This angle is converted into a fractional value representing the fraction from the outer cone angle to the inner cone angle, clamped to the range [0,1]. The resulting value is then fed into one of the following user-selectable functions to determine the final 0-1 scaling value to be applied to thelight's radiance: <br>  0 (off)         - no fallof, a step function at the outer cone boundary is applied<br>  1 (linear)      - a linear ramp, i.e. the fractional parameter is applied as-is<br>  2 (ease in)     - a quadratic ramp with zero gradient at the start point (outer cone)<br>  3 (ease out)    - a quadratic ramp with zero gradient at the end point (inner cone)<br>  4 (ease in/out) - a cubic ramp with zero gradient at both ends (outer and inner cone)<br></p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.angle_falloff_type.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.angle_falloff_type.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.angle_falloff_type.links heading=4-%}
    </p>
    <h3>black_level</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 0.001
      <p class="scene-class-comments">The brightness of the SpotLight lens as seen through the camera via a primary ray, when the true computed radiance would otherwise be black, as a fraction of the light's radiance. This is simply a convenience feature to make the SpotLight lens visible in the camera view, and has no effect on how the light illuminates the scene.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.black_level.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.black_level.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.black_level.links heading=4-%}
    </p>
  </p>
</details>
<details open>
  <summary>Map attributes</summary>
  <p>
    <h3>contrast</h3>
    <p class="scene-class-type">
      <b>Rgb</b>
      <br>
      default: [ 1, 1, 1 ]
      <p class="scene-class-comments">Per-channel contrast used in color-correcting the light's texture, if one is present. The operation mimics Nuke's ColorCorrect node's contrast function:<br>  For input &gt;  0, output = 0.18 * pow(inputCompnent/0.18, contrast).<br>  For input &lt;= 0, output = 0.18 * input * pow(1/0.18, contrast).</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.contrast.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.contrast.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.contrast.links heading=4-%}
    </p>
    <h3>gain</h3>
    <p class="scene-class-type">
      <b>Rgb</b>
      <br>
      default: [ 1, 1, 1 ]
      <p class="scene-class-comments">Per-channel gain used in tandem with a per-channel offset for color-correcting the light's texture, if one is present. This is achieved by applying the following formula for each channel:<br>  output = input * gain + offset</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.gain.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.gain.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.gain.links heading=4-%}
    </p>
    <h3>gamma</h3>
    <p class="scene-class-type">
      <b>Rgb</b>
      <br>
      default: [ 1, 1, 1 ]
      <p class="scene-class-comments">Per-channel gamma used in color-correcting the light's texture, if one is present. This is achieved by applying the following formula for each channel:<br>  For input &gt;  0, output = pow(input, 1 / gamma)<br>  For input &lt;= 0, output = input</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.gamma.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.gamma.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.gamma.links heading=4-%}
    </p>
    <h3>offset</h3>
    <p class="scene-class-type">
      <b>Rgb</b>
      <br>
      default: [ 0, 0, 0 ]
      <p class="scene-class-comments">Per-channel offset used in tandem with a per-channel gain for color-correcting the light's texture, if one is present. This is achieved by applying the following formula for each channel:<br>  output = input * gain + offset</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.offset.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.offset.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.offset.links heading=4-%}
    </p>
    <h3>saturation</h3>
    <p class="scene-class-type">
      <b>Rgb</b>
      <br>
      default: [ 1, 1, 1 ]
      <p class="scene-class-comments">Per-channel saturation used in color-correcting the light's texture, if one is present. This is achieved by applying the following formula for each channel:<br>  output = lerp(luminance(inputRGB), input, saturation).</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.saturation.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.saturation.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.saturation.links heading=4-%}
    </p>
    <h3>temperature</h3>
    <p class="scene-class-type">
      <b>Vec3f</b>
      <br>
      default: [ 0, 0, 0 ]
      <p class="scene-class-comments">Color temperature using Nuke-style T/M/I settings (T = temperature, M = magenta/green, I = intensity). This is achieved as follows:<br>The 3-channel temperature is interpreted as the vector (T,M,I). The followiong scale values are then applied to the RGB components:<br>  outputR = inputR * (pow(2,I) + M/3 - T/2)<br>  outputG = inputG * (pow(2,I) - 2*M/3<br>  outputB = inputB * (pow(2,I) + M/3 + T/2)</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.temperature.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.temperature.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.temperature.links heading=4-%}
    </p>
    <h3>texture</h3>
    <p class="scene-class-type">
      <b>String</b> <i>filename</i>
      <br>
      default: 
      <p class="scene-class-comments">File name of the texture applied to the light. If set to the empty string, no texture is applied. Any file format supported by OpenImageIO can be used. The texture is used in 2 ways - for looking up the texture value at the intersection point when a ray hits the light, and for building a lookup-table-based auxilliary data structure used for distributing light samples over the texture.<br>Color correction is applied to the texture in this order: saturation, contrast, gamma, gain and offset, then temperature, after which negative values are clamped to 0.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture.links heading=4-%}
    </p>
    <h3>texture_border_color</h3>
    <p class="scene-class-type">
      <b>Rgb</b>
      <br>
      default: [ 1, 1, 1 ]
      <p class="scene-class-comments">RGB value used when a texture lookup occurs outside the texture.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_border_color.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_border_color.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_border_color.links heading=4-%}
    </p>
    <h3>texture_coverage</h3>
    <p class="scene-class-type">
      <b>Vec2f</b>
      <br>
      default: [ 1, 1 ]
      <p class="scene-class-comments">The fraction of the light, in u and v, that the texture covers. Values less than 1 shrink the texture towards its (0, 0) corner, and the rest of the light shows texture_border_color.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_coverage.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_coverage.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_coverage.links heading=4-%}
    </p>
    <h3>texture_mirror_u</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: False
      <p class="scene-class-comments">Whether to mirror the texture in the u-direction. If set to false, the texture is repeated in the u-direction.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_mirror_u.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_mirror_u.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_mirror_u.links heading=4-%}
    </p>
    <h3>texture_mirror_v</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: False
      <p class="scene-class-comments">Whether to mirror the texture in the v-direction. If set to false, the texture is repeated in the v-direction.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_mirror_v.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_mirror_v.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_mirror_v.links heading=4-%}
    </p>
    <h3>texture_reps_u</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 1.0
      <p class="scene-class-comments">Number of times texture repeats in u over the scaled texture space.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_reps_u.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_reps_u.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_reps_u.links heading=4-%}
    </p>
    <h3>texture_reps_v</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 1.0
      <p class="scene-class-comments">Number of times texture repeats in v over the scaled texture space.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_reps_v.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_reps_v.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_reps_v.links heading=4-%}
    </p>
    <h3>texture_rotation</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 0.0
      <p class="scene-class-comments">Clockwise rotation angle in degrees. The texture rotates about its (0, 0) corner, not its center.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_rotation.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_rotation.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_rotation.links heading=4-%}
    </p>
    <h3>texture_translation</h3>
    <p class="scene-class-type">
      <b>Vec2f</b>
      <br>
      default: [ 0, 0 ]
      <p class="scene-class-comments">Translation of the texture in (u,v)-space, in units of the texture size. For example, a translation of (0.25, 0.5) will translate the texture one-quarter of its width in the u-direction and one-half of its height in the v-direction.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_translation.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_translation.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_translation.links heading=4-%}
    </p>
  </p>
</details>
<details open>
  <summary>Properties attributes</summary>
  <p>
    <h3>apply_scene_scale</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: True
      <p class="scene-class-comments">Only used when normalized is true. When set to true, the normalized radiance is also divided by pi * scene_scale * scene_scale, where scene_scale is the SceneVariables attribute (0.01 by default). At the default scene scale this makes the light about 3183 times brighter.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.apply_scene_scale.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.apply_scene_scale.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.apply_scene_scale.links heading=4-%}
    </p>
    <h3>clear_radius</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 0.0
      <p class="scene-class-comments">Surfaces closer than this distance to the light don't block it, so they cast no shadows from it. An object partly inside this distance casts shadows only from its parts outside it. Setting this value to 0.0 or less effectively disables this feature. When clear_radius_falloff_distance is greater than 0, it is instead the distance of the light-receiving point from the light that is used: points closer than clear_radius receive no shadows from the light.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.clear_radius.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.clear_radius.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.clear_radius.links heading=4-%}
    </p>
    <h3>clear_radius_falloff_distance</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 0.0
      <p class="scene-class-comments">Distance over which the shadows fall off. Shadows are fully visible at a distance clear_radius + clear_radius_falloff_distance from the light, and fully invisble at a distance clear_radius from the light.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.clear_radius_falloff_distance.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.clear_radius_falloff_distance.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.clear_radius_falloff_distance.links heading=4-%}
    </p>
    <h3>clear_radius_interpolation_type</h3>
    <p class="scene-class-type">
      <b>Int</b> <i>enum</i>
      <br>
          &nbsp;&nbsp;0 = &ldquo;linear&rdquo; (default)<br>
          &nbsp;&nbsp;1 = &ldquo;exponential_up&rdquo;<br>
          &nbsp;&nbsp;2 = &ldquo;exponential_down&rdquo;<br>
          &nbsp;&nbsp;3 = &ldquo;smoothstep&rdquo;<br>
      <p class="scene-class-comments">Interpolation type to use for the clear radius shadow falloff.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.clear_radius_interpolation_type.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.clear_radius_interpolation_type.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.clear_radius_interpolation_type.links heading=4-%}
    </p>
    <h3>color</h3>
    <p class="scene-class-type">
      <b>Rgb</b>
      <br>
      default: [ 1, 1, 1 ]
      <p class="scene-class-comments">The light's RGB values.<br>These are combined multiplicatively with the intensity and other attributes in determining the light's 3-channel radiance.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.color.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.color.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.color.links heading=4-%}
    </p>
    <h3>exposure</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 0.0
      <p class="scene-class-comments">The light's exposure value.<br>This value provides an alternative to the intensity value as a mechanism for controlling the light's overall brightness, and is inspired by the corresponding photographic term but is generalised to apply independently to each light. To calculate its effect, pow(2, exposure) is combined multiplicatively with the color and other attributes in determining the light's 3-channel radiance.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.exposure.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.exposure.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.exposure.links heading=4-%}
    </p>
    <h3>intensity</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 1.0
      <p class="scene-class-comments">The light's intensity.<br>This is combined multiplicatively with the color and other attributes in determining the light's 3-channel radiance.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.intensity.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.intensity.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.intensity.links heading=4-%}
    </p>
    <h3>label</h3>
    <p class="scene-class-type">
      <b>String</b>
      <br>
      default: 
      <p class="scene-class-comments">Label used in light aov expressions.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.label.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.label.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.label.links heading=4-%}
    </p>
    <h3>max_shadow_distance</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 0.0
      <p class="scene-class-comments">The distance from a light-receiving point, measured along the shadow ray towards the light, beyond which objects no longer cast shadows from that light onto the point. 0 means no limit.<br>Note that the distance is thresholded for each occlusion ray cast for this light, it is possible for a receiving point to lie at an intermediate distance such that some parts of the light are closer than the threshold distance and other parts beyond it, in which case the point will appearto be in partial shadow.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.max_shadow_distance.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.max_shadow_distance.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.max_shadow_distance.links heading=4-%}
    </p>
    <h3>mb</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: False
      <p class="scene-class-comments">Whether motion-blur is active for this light. When set to true, the scene's illumination will correctly account for any blur() applied to the light's transformation matrix. Motion blur must also be enabled with the SceneVariables attribute enable_motion_blur.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.mb.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.mb.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.mb.links heading=4-%}
    </p>
    <h3>min_shadow_distance</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 0.0
      <p class="scene-class-comments">The distance from a light-receiving point, measured along the shadow ray towards the light, within which objects do not cast shadows from that light onto the point.<br>Note that the distance is thresholded for each occlusion ray cast for this light, it is possible for a receiving point to lie at an intermediate distance such that some parts of the light are closer than the threshold distance and other parts beyond it, in which case the point will appearto be in partial shadow.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.min_shadow_distance.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.min_shadow_distance.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.min_shadow_distance.links heading=4-%}
    </p>
    <h3>normalized</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: True
      <p class="scene-class-comments">When set to true, the size of the light can be changed without altering the amount of total energy cast into the scene. This is achieved via scaling the light's radiance by the reciprocal of its surface area. When set to false, the radiance is used as-is, regardless of surface area.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.normalized.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.normalized.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.normalized.links heading=4-%}
    </p>
    <h3>on</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: True
      <p class="scene-class-comments">Whether the light is switched on.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.on.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.on.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.on.links heading=4-%}
    </p>
    <h3>presence_shadows</h3>
    <p class="scene-class-type">
      <b>Int</b> <i>enum</i>
      <br>
          &nbsp;&nbsp;0 = &ldquo;force off&rdquo;<br>
          &nbsp;&nbsp;1 = &ldquo;force on&rdquo;<br>
          &nbsp;&nbsp;2 = &ldquo;use default&rdquo; (default)<br>
      <p class="scene-class-comments">Switch this attribute on for shadows cast from this light to correctly respect presence values. When off, surfaces with a material with presence less than 1.0 will cast opaque shadows from this light. This is an optimization - when the attribute is off, occlusion rays (fast) are used for testing for shadows. When it is on, regular rays (slower) are used, and the material's presence is evaluated to determine how much shadowing should occur. When set to "use default" it reads from the value of SceneVariable enable_presence_shadows.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.presence_shadows.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.presence_shadows.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.presence_shadows.links heading=4-%}
    </p>
    <h3>ray_termination</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: False
      <p class="scene-class-comments">Whether the light is used for ray termination color. Ray termination color is used for filling in falsely dark areas where ray paths have been terminated too early by the depth controls. Such a ray path immediately exits to any ray termination light(s) present in the light set being applied to the lobe, ignoring occlusion by scene geometry. Any light can either be a regular light or a ray termination light (but not both). Thus they can be freely assigned to light sets, which provides a mechanism for applying specific ray termination lights to specific materials, parts or objects. Ray termination color is only applied to non-hair transmission lobes.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.ray_termination.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.ray_termination.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.ray_termination.links heading=4-%}
    </p>
    <h3>texture_filter</h3>
    <p class="scene-class-type">
      <b>Int</b> <i>enum</i>
      <br>
          &nbsp;&nbsp;0 = &ldquo;nearest neighbor&rdquo; (default)<br>
          &nbsp;&nbsp;1 = &ldquo;bilinear&rdquo;<br>
          &nbsp;&nbsp;2 = &ldquo;nearest neighbor with nearest mip&rdquo;<br>
          &nbsp;&nbsp;3 = &ldquo;bilinear with nearest mip&rdquo;<br>
      <p class="scene-class-comments">The filtering mode to apply to the texture. Nearest neighbor is the cheapest filtering mode but produces a blocky result. Switch linear filtering on for a smoother result. Additionally, mip-mapping can be switched on with either nearest neighbor or linear filtering. Only EnvLight and DistantLight use mip-mapping; on other lights the mip options have no effect.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_filter.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_filter.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_filter.links heading=4-%}
    </p>
    <h3>visible_in_camera</h3>
    <p class="scene-class-type">
      <b>Int</b> <i>enum</i>
      <br>
          &nbsp;&nbsp;0 = &ldquo;force off&rdquo;<br>
          &nbsp;&nbsp;1 = &ldquo;force on&rdquo;<br>
          &nbsp;&nbsp;2 = &ldquo;use default&rdquo; (default)<br>
      <p class="scene-class-comments">Whether the light is directly visible in the scene's active camera. When set to "use default" it reads from the value of SceneVariable lights_visible_in_camera.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_in_camera.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_in_camera.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_in_camera.links heading=4-%}
    </p>
  </p>
</details>
<details open>
  <summary>Visibility Flags attributes</summary>
  <p>
    <h3>visible_diffuse_reflection</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: True
      <p class="scene-class-comments">Whether the light is visible in diffuse reflection.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_diffuse_reflection.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_diffuse_reflection.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_diffuse_reflection.links heading=4-%}
    </p>
    <h3>visible_diffuse_transmission</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: True
      <p class="scene-class-comments">Whether the light is visible in diffuse transmission.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_diffuse_transmission.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_diffuse_transmission.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_diffuse_transmission.links heading=4-%}
    </p>
    <h3>visible_glossy_reflection</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: True
      <p class="scene-class-comments">Whether the light is visible in glossy reflection.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_glossy_reflection.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_glossy_reflection.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_glossy_reflection.links heading=4-%}
    </p>
    <h3>visible_glossy_transmission</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: True
      <p class="scene-class-comments">Whether the light is visible in glossy transmission (refraction).</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_glossy_transmission.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_glossy_transmission.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_glossy_transmission.links heading=4-%}
    </p>
    <h3>visible_mirror_reflection</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: True
      <p class="scene-class-comments">Whether the light is visible in miror reflection.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_mirror_reflection.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_mirror_reflection.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_mirror_reflection.links heading=4-%}
    </p>
    <h3>visible_mirror_transmission</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: True
      <p class="scene-class-comments">Whether the light is visible in miror transmission (refraction).</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_mirror_transmission.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_mirror_transmission.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_mirror_transmission.links heading=4-%}
    </p>
  </p>
</details>
<details open>
  <summary>General attributes</summary>
  <p>
    <h3>light_filters</h3>
    <p class="scene-class-type">
      <b>SceneObject Vector</b>
      <br>
      default: {}
      <p class="scene-class-comments">Vector of LightFilters associated with the light.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.light_filters.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.light_filters.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.light_filters.links heading=4-%}
    </p>
    <h3>node_xform</h3>
    <p class="scene-class-type">
      <b>Mat4d</b> <i>blurrable</i>
      <br>
      default: [ [ 1, 0, 0, 0 ], [ 0, 1, 0, 0 ], [ 0, 0, 1, 0 ], [ 0, 0, 0, 1 ] ]
      <p class="scene-class-comments">The 4x4 matrix describing the transformation from local space to world space.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.node_xform.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.node_xform.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.node_xform.links heading=4-%}
    </p>
  </p>
</details>
</div>
{%-include example.html data=site.data.user-reference.scene-objects.lights.SpotLight-%}