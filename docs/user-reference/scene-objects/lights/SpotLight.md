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
      <p class="scene-class-comments">The aspect ratio of the lens: its local x dimension divided by its local y dimension. Values other than 1.0 give the lens, and the pool of light it projects, an elliptical shape: values greater than 1.0 make it wider along the local x axis, and values less than 1.0 make it longer along the local y axis.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.aspect_ratio.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.aspect_ratio.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.aspect_ratio.links heading=4-%}
    </p>
    <h3>focal_plane_distance</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 10000000000.0
      <p class="scene-class-comments">The distance from the SpotLight's position, measured along the direction the light is pointing, at which the projected image is in focus. Surfaces at this distance receive the sharpest projection of the light's texture and of the edges of the cone; nearer and farther surfaces receive a blurred projection, and the blur increases with lens_radius. The default is effectively infinite, which gives a soft projection unless lens_radius is very small. To project a sharp texture, set this to the distance from the light to the surface being lit.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.focal_plane_distance.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.focal_plane_distance.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.focal_plane_distance.links heading=4-%}
    </p>
    <h3>inner_cone_angle</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 30.0
      <p class="scene-class-comments">The apex angle, in degrees, of the bright inner cone of the light emitted by the SpotLight. Full illumination takes place inside this cone. This is a full angle, measured from one side to the other, not a half angle. Values greater than outer_cone_angle are clamped to outer_cone_angle. The light falls off between the outer and inner cones - see the angle_falloff_type attribute.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.inner_cone_angle.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.inner_cone_angle.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.inner_cone_angle.links heading=4-%}
    </p>
    <h3>lens_radius</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 1.0
      <p class="scene-class-comments">The radius of the SpotLight's lens along its local x axis, in local units. The radius along the local y axis is lens_radius / aspect_ratio. A larger lens produces softer shadows and a softer, slightly wider edge to the pool of light, in the same way as a larger area light. When normalized is true, changing the lens radius does not change the total energy cast into the scene.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.lens_radius.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.lens_radius.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.lens_radius.links heading=4-%}
    </p>
    <h3>outer_cone_angle</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 60.0
      <p class="scene-class-comments">The apex angle, in degrees, of the bounding cone of the light emitted by the SpotLight. No illumination takes place outside this cone. This is a full angle, measured from one side to the other, not a half angle. The light falls off between the outer and inner cones - see the angle_falloff_type attribute.</p>
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
      <p class="scene-class-comments">The falloff function applied between the outer and inner cones. To calculate this, the angle from the cone's axis to the point being illuminated is measured as seen from the SpotLight's position. This angle is converted into a fractional value representing the fraction from the outer cone angle to the inner cone angle, clamped to the range [0,1]. The resulting value is then fed into one of the following user-selectable functions to determine the final 0-1 scaling value to be applied to the light's radiance: <br>  0 (off)         - no falloff; full illumination extends to the outer cone, with a hard edge there<br>  1 (linear)      - a linear ramp, i.e. the fractional parameter is applied as-is<br>  2 (ease in)     - a quadratic ramp with zero gradient at the start point (outer cone)<br>  3 (ease out)    - a quadratic ramp with zero gradient at the end point (inner cone)<br>  4 (ease in/out) - a cubic ramp with zero gradient at both ends (outer and inner cone)<br></p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.angle_falloff_type.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.angle_falloff_type.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.angle_falloff_type.links heading=4-%}
    </p>
    <h3>black_level</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 0.001
      <p class="scene-class-comments">The brightness of the SpotLight's lens when it is seen directly by the camera from outside the light's cone, where it would otherwise appear black. It is expressed as a fraction of the light's radiance, so 0 leaves the lens black and 1 makes it as bright as when seen from inside the cone. This only affects how the lens looks to camera rays - it has no effect on how the light illuminates the scene. The lens is only seen by the camera if the light is visible in camera - see visible_in_camera.</p>
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
      <p class="scene-class-comments">Per-channel contrast of the light's texture, pivoting around 0.18 (mid grey) like the contrast control of Nuke's ColorCorrect node. Values below 1 flatten the texture and values above 1 increase its contrast. For each channel:<br>  For input &gt;  0, output = 0.18 * pow(input / 0.18, contrast)<br>  For input &lt;= 0, output = 0.18 * input * pow(1 / 0.18, contrast)</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.contrast.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.contrast.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.contrast.links heading=4-%}
    </p>
    <h3>gain</h3>
    <p class="scene-class-type">
      <b>Rgb</b>
      <br>
      default: [ 1, 1, 1 ]
      <p class="scene-class-comments">Per-channel multiplier for the light's texture, applied together with offset. For each channel:<br>  output = input * gain + offset</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.gain.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.gain.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.gain.links heading=4-%}
    </p>
    <h3>gamma</h3>
    <p class="scene-class-type">
      <b>Rgb</b>
      <br>
      default: [ 1, 1, 1 ]
      <p class="scene-class-comments">Per-channel gamma of the light's texture. Values above 1 brighten its mid-tones and values below 1 darken them, while 0 and 1 are unchanged. For each channel:<br>  For input &gt;  0, output = pow(input, 1 / gamma)<br>  For input &lt;= 0, output = input</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.gamma.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.gamma.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.gamma.links heading=4-%}
    </p>
    <h3>offset</h3>
    <p class="scene-class-type">
      <b>Rgb</b>
      <br>
      default: [ 0, 0, 0 ]
      <p class="scene-class-comments">Per-channel value added to the light's texture, applied together with gain. Positive values lift the darker parts of the texture. For each channel:<br>  output = input * gain + offset</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.offset.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.offset.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.offset.links heading=4-%}
    </p>
    <h3>saturation</h3>
    <p class="scene-class-type">
      <b>Rgb</b>
      <br>
      default: [ 1, 1, 1 ]
      <p class="scene-class-comments">Per-channel saturation of the light's texture. 0 removes all color, 1 leaves the texture unchanged, and values above 1 increase saturation. For each channel:<br>  output = lerp(luminance(inputRGB), input, saturation)</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.saturation.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.saturation.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.saturation.links heading=4-%}
    </p>
    <h3>temperature</h3>
    <p class="scene-class-type">
      <b>Vec3f</b>
      <br>
      default: [ 0, 0, 0 ]
      <p class="scene-class-comments">Nuke-style color temperature controls for the light's texture, as a vector (T, M, I). T shifts the color between warm (negative) and cool (positive), M between green (negative) and magenta (positive), and I scales the brightness in stops. The RGB channels are scaled as follows:<br>  outputR = inputR * (pow(2, I) + M/3 - T/2)<br>  outputG = inputG * (pow(2, I) - 2*M/3)<br>  outputB = inputB * (pow(2, I) + M/3 + T/2)</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.temperature.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.temperature.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.temperature.links heading=4-%}
    </p>
    <h3>texture</h3>
    <p class="scene-class-type">
      <b>String</b> <i>filename</i>
      <br>
      default: 
      <p class="scene-class-comments">File name of a texture to apply to the light. If empty, no texture is applied. Any image format that OpenImageIO can read may be used. How the texture is mapped onto the light depends on the light type. The texture is multiplied by the light's color, and is also used to sample the light efficiently, by concentrating samples on its brighter areas.<br>The other attributes in this group transform and color-correct the texture, and have no effect without one. Color correction is applied in this order: saturation, contrast, gamma, gain and offset, then temperature, after which negative values are clamped to 0.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture.links heading=4-%}
    </p>
    <h3>texture_border_color</h3>
    <p class="scene-class-type">
      <b>Rgb</b>
      <br>
      default: [ 1, 1, 1 ]
      <p class="scene-class-comments">The color of any part of the light the texture doesn't cover, for example when texture_coverage is less than 1, or when the texture is translated or rotated.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_border_color.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_border_color.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_border_color.links heading=4-%}
    </p>
    <h3>texture_coverage</h3>
    <p class="scene-class-type">
      <b>Vec2f</b>
      <br>
      default: [ 1, 1 ]
      <p class="scene-class-comments">The fraction of the light, in u and v, that the texture covers. The default, (1, 1), fits the texture to the light. Smaller values shrink the texture towards its (0, 0) corner; for example (0.5, 0.5) covers a quarter of the light, and the rest shows texture_border_color. texture_reps_u and texture_reps_v repeat the texture within the covered area.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_coverage.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_coverage.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_coverage.links heading=4-%}
    </p>
    <h3>texture_mirror_u</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: False
      <p class="scene-class-comments">Whether alternate repeats of the texture in u are mirrored, so that neighboring copies meet seamlessly. When false, each repeat is an identical copy. Only has an effect when texture_reps_u is greater than 1.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_mirror_u.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_mirror_u.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_mirror_u.links heading=4-%}
    </p>
    <h3>texture_mirror_v</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: False
      <p class="scene-class-comments">Whether alternate repeats of the texture in v are mirrored, so that neighboring copies meet seamlessly. When false, each repeat is an identical copy. Only has an effect when texture_reps_v is greater than 1.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_mirror_v.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_mirror_v.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_mirror_v.links heading=4-%}
    </p>
    <h3>texture_reps_u</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 1.0
      <p class="scene-class-comments">How many times the texture repeats in u, within the area set by texture_coverage.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_reps_u.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_reps_u.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_reps_u.links heading=4-%}
    </p>
    <h3>texture_reps_v</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 1.0
      <p class="scene-class-comments">How many times the texture repeats in v, within the area set by texture_coverage.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_reps_v.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_reps_v.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_reps_v.links heading=4-%}
    </p>
    <h3>texture_rotation</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 0.0
      <p class="scene-class-comments">Clockwise rotation of the light's texture, in degrees. The texture rotates about its (0, 0) corner, not its center, so rotating it moves part of the texture off the light and shows texture_border_color in its place.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_rotation.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_rotation.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.texture_rotation.links heading=4-%}
    </p>
    <h3>texture_translation</h3>
    <p class="scene-class-type">
      <b>Vec2f</b>
      <br>
      default: [ 0, 0 ]
      <p class="scene-class-comments">Translation of the light's texture in (u, v), in units of the texture size. For example, a translation of (0.25, 0.5) moves the texture one quarter of its width in u and half its height in v. Parts of the light the texture no longer covers show texture_border_color.</p>
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
      <p class="scene-class-comments">Only used when normalized is true. When set to true, the normalized radiance is also divided by pi * scene_scale * scene_scale, where scene_scale is the SceneVariables attribute (0.01 by default). At the default scene scale this makes the light about 3183 times brighter. This preserves the behavior of older scenes; set it to false for normalization that matches other renderers.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.apply_scene_scale.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.apply_scene_scale.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.apply_scene_scale.links heading=4-%}
    </p>
    <h3>clear_radius</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 0.0
      <p class="scene-class-comments">Objects closer than this distance to the light don't cast shadows from it, for example so that the light's own fixture or nearby geometry doesn't block it. 0 or less disables this.<br>When clear_radius_falloff_distance is greater than 0, this works differently: it is the distance of the lit point from the light that matters, not the distance of the object casting the shadow. Points closer than clear_radius to the light receive no shadows from it - see clear_radius_falloff_distance.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.clear_radius.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.clear_radius.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.clear_radius.links heading=4-%}
    </p>
    <h3>clear_radius_falloff_distance</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 0.0
      <p class="scene-class-comments">When greater than 0, shadows from this light fade in with the lit point's distance from the light: points closer than clear_radius receive no shadows, points farther than clear_radius + clear_radius_falloff_distance receive full shadows, and shadows fade in between, following clear_radius_interpolation_type. Unlike clear_radius on its own, objects close to the light still cast shadows on points farther away. 0 (the default) turns the falloff off.</p>
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
      <p class="scene-class-comments">The curve used to fade shadows in over clear_radius_falloff_distance, where t goes from 0 to 1 across the falloff:<br>  linear           - shadow strength t<br>  exponential_up   - t*t: shadows fade in slowly at first<br>  exponential_down - 1 - (1-t)*(1-t): shadows fade in quickly at first<br>  smoothstep       - t*t*(3 - 2*t): eased at both ends<br>Only used when clear_radius_falloff_distance is greater than 0.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.clear_radius_interpolation_type.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.clear_radius_interpolation_type.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.clear_radius_interpolation_type.links heading=4-%}
    </p>
    <h3>color</h3>
    <p class="scene-class-type">
      <b>Rgb</b>
      <br>
      default: [ 1, 1, 1 ]
      <p class="scene-class-comments">The light's color. It is multiplied by intensity and by pow(2, exposure) to give the light's brightness.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.color.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.color.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.color.links heading=4-%}
    </p>
    <h3>exposure</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 0.0
      <p class="scene-class-comments">The light's brightness in photographic stops, as an alternative to intensity. The light's brightness is multiplied by pow(2, exposure), so +1 doubles it and -1 halves it. Combined with color and intensity.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.exposure.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.exposure.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.exposure.links heading=4-%}
    </p>
    <h3>intensity</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 1.0
      <p class="scene-class-comments">A multiplier for the light's brightness, combined with color and exposure. Doubling the intensity doubles the light's contribution to the scene.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.intensity.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.intensity.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.intensity.links heading=4-%}
    </p>
    <h3>label</h3>
    <p class="scene-class-type">
      <b>String</b>
      <br>
      default: 
      <p class="scene-class-comments">A label for this light, used to select it in light path expressions (LPEs), for example to output its contribution to a separate AOV.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.label.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.label.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.label.links heading=4-%}
    </p>
    <h3>max_shadow_distance</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 0.0
      <p class="scene-class-comments">The maximum distance from a lit point at which an object can shadow that point from this light. Objects farther away than this, along the path towards the light, are ignored. This shortens long shadows so that only the part near the object casting them remains. 0 (the default) means no limit.<br>The distance is tested separately for each sample on the light, so a point near the limit can be partly shadowed.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.max_shadow_distance.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.max_shadow_distance.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.max_shadow_distance.links heading=4-%}
    </p>
    <h3>mb</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: False
      <p class="scene-class-comments">Whether the light is motion blurred. When true, and the light's node_xform is given different values at the start and end of the motion blur interval with blur(), the light moves while the camera's shutter is open, blurring its illumination and the shadows it casts. When false, the light stays where it is at the moment the shutter opens. Motion blur must also be enabled with the SceneVariables attribute enable_motion_blur.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.mb.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.mb.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.mb.links heading=4-%}
    </p>
    <h3>min_shadow_distance</h3>
    <p class="scene-class-type">
      <b>Float</b>
      <br>
      default: 0.0
      <p class="scene-class-comments">The minimum distance from a lit point at which an object can shadow that point from this light. Objects closer than this, along the path towards the light, are ignored. This removes the part of a shadow next to the object casting it, so the shadow appears to start away from the object. 0 (the default) means no minimum.<br>The distance is tested separately for each sample on the light, so a point near the limit can be partly shadowed.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.min_shadow_distance.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.min_shadow_distance.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.min_shadow_distance.links heading=4-%}
    </p>
    <h3>normalized</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: True
      <p class="scene-class-comments">When set to true, the size of the lens (lens_radius and aspect_ratio) can be changed without altering the amount of total energy cast into the scene. This is achieved by scaling the light's radiance by the reciprocal of the lens area. When set to false, color, intensity and exposure set the radiance directly, so a larger lens casts more light in total.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.normalized.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.normalized.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.normalized.links heading=4-%}
    </p>
    <h3>on</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: True
      <p class="scene-class-comments">Whether the light is switched on. When off, the light contributes nothing to the scene.</p>
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
      <p class="scene-class-comments">Whether shadows cast from this light take material presence (partial transparency) into account. When off, objects whose material has presence less than 1.0 cast fully opaque shadows from this light. When on, their shadows are lightened according to their presence. Off is faster: shadows are tested with occlusion rays, whereas on uses regular rays and evaluates each material's presence. When set to "use default", it uses the SceneVariables attribute enable_presence_shadows, which is false by default.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.presence_shadows.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.presence_shadows.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.presence_shadows.links heading=4-%}
    </p>
    <h3>ray_termination</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: False
      <p class="scene-class-comments">Whether the light is used for ray termination color. Ray termination color fills in areas that would otherwise be falsely dark because ray paths were ended too early by the ray depth controls. Such a ray path immediately takes its color from any ray termination light(s) in the light set applied to the lobe, ignoring occlusion by scene geometry. A light is either a regular light or a ray termination light, not both, so ray termination lights can be assigned to light sets to apply them to specific materials, parts or objects. Ray termination color is only applied to non-hair transmission lobes.</p>
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
      <p class="scene-class-comments">How the light's texture is filtered when it is looked up. Nearest neighbor (the default) is the cheapest, but shows individual texels as blocks when the texture is magnified. Bilinear blends neighboring texels for a smooth result. The "with nearest mip" options also choose a lower-resolution mipmap level according to the ray's footprint, which avoids aliasing when the texture is minified. Only EnvLight and DistantLight use mipmap levels; on other lights, the "with nearest mip" options look the same as nearest neighbor and bilinear.</p>
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
      <p class="scene-class-comments">Whether the light itself can be seen when the camera looks directly at it. This only affects camera rays - it doesn't change how the light illuminates the scene. When set to "use default", it uses the SceneVariables attribute lights_visible_in_camera, which is false by default.</p>
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
      <p class="scene-class-comments">Whether this light lights diffuse reflection lobes. When false, diffuse surfaces receive no direct light from it.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_diffuse_reflection.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_diffuse_reflection.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_diffuse_reflection.links heading=4-%}
    </p>
    <h3>visible_diffuse_transmission</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: True
      <p class="scene-class-comments">Whether this light lights diffuse transmission lobes. When false, translucent surfaces don't glow when it lights them from behind.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_diffuse_transmission.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_diffuse_transmission.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_diffuse_transmission.links heading=4-%}
    </p>
    <h3>visible_glossy_reflection</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: True
      <p class="scene-class-comments">Whether this light lights glossy reflection lobes. When false, glossy surfaces show no highlight or reflection of it.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_glossy_reflection.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_glossy_reflection.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_glossy_reflection.links heading=4-%}
    </p>
    <h3>visible_glossy_transmission</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: True
      <p class="scene-class-comments">Whether this light lights glossy transmission lobes. When false, it can't be seen, and gives no light, through rough refractive surfaces such as frosted glass.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_glossy_transmission.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_glossy_transmission.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_glossy_transmission.links heading=4-%}
    </p>
    <h3>visible_mirror_reflection</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: True
      <p class="scene-class-comments">Whether this light can be seen in mirror reflections. When false, it doesn't appear in mirror-like surfaces such as chrome.</p>
      {%-include image-gallery.html images=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_mirror_reflection.images data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include video-gallery.html videos=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_mirror_reflection.videos data=site.data.user-reference.scene-objects.lights.SpotLight-%}
      {%-include see-also.html links=site.data.user-reference.scene-objects.lights.SpotLight.attributes.visible_mirror_reflection.links heading=4-%}
    </p>
    <h3>visible_mirror_transmission</h3>
    <p class="scene-class-type">
      <b>Bool</b>
      <br>
      default: True
      <p class="scene-class-comments">Whether this light can be seen through mirror transmission (refraction). When false, it can't be seen through clear refractive surfaces such as glass.</p>
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
      <p class="scene-class-comments">The LightFilters that modify this light's illumination, for example to shape it with barn doors or a cookie, or to change how it falls off with distance.</p>
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