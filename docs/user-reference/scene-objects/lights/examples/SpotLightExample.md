```lua
SpotLight("/lights/spot") {
    ["node_xform"] = Mat4(0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0, 10, 10, 10, 1),
    ["on"] = true,
    ["color"] = Rgb(3, 2, 1),
    ["black_level"] = 0.01,
    ["intensity"] = 0.02,
    ["lens_radius"] = 1.4,
    ["inner_cone_angle"] = 30,
    ["outer_cone_angle"] = 60,
    ["focal_plane_distance"] = 100,
    ["angle_falloff_type"] = "ease out",
}
```