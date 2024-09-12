1. you can do set camera projections and then use it to export images
2. activate manipulator can be used to move objects in a space (probably not useful tho)
3. material compound subshape can be used to display materials such as aluminium steel, etc. (part of metals) shape can be use to display meta level, for example glass.
4. Erase shape will delete a shape
5. core_display_callbacks helps you select a shape, and then it will give the bounding box.
6. Core dimensions will give dimensions
7. offscreen renderer can be used when taking images.
8. Change quality of display based on specs of the PC
9. Add raytracing
10. Change color of the edge
11. 	core_display_signal_slots.py
12. we can add textured shape. i.e. change texture based on our needs. can use for different materials and finished
13. Built in exception handler is available
14. can export to gltf, ply, step, stl
15. geometry_bounding_box,test in depth
16. step file face recognition is helpful (can be used to insert thread and stuff). geometry_face_recognition_from_stepfile
17. geomplate thing can be used to solve for diemaking and stuff? idk
18. 	core_geometry_make_pipe_shell.py check what this does, might be helpful
19. maybe creating medial axis can be helpful
20. minimal distance between two shapes can be used to do something probably
21. oriented bounding boxes are available
22. face selection mode is there, which can be used to set angles for bending and stuff, also the same thing can be used to detect ciecles and stuff. core_geometry_recognize_feature.py
23. core_hlr_outliner.py - might be helpful, check out what this is.
24. json_serializer, see what this is. might be helpful.
25.it can load brep, gltf_ocaf, iges, step_ap203, step_ap203_ocaf, step_ap214 with materials, step with colots, stl files.
26. it offers a bunch of mesh related tools, if working with stl and stuff, one can use this.
27. can we perhaps use a splicer to estimate how a file looks in every layer, to accurately estimate the area and volume, and then use it to calculate pricing? topology Boolean operations can be used to enhance/complement?
28. shape_properties can be used to get properties of a shape
29. 3d to 2d screen coordinates can be used to find 3d coordinate of a point and then get the 2d screen coordinates, test the demo to understand. might be useful.
30. Make a cool animation using visualization_camera_2.py
31. usecase sounds cool, but have to explore more core_visualization_overpaint_viewer.py
32. step to x3d conversion is there
33. mesh quality can be adjusted in webgl, maybe to make it look like it's loading fast or for low bandwidth connections, this can be used to load a dummy model first and then load completely.
34. ifc clip plane can be used to "clip plane"
35. use intersections to create weld lines. also maybe build an algorithm to automatically detect if a weld will be fillet or groove
36. MUST SEE: core_display_callbacks.py, core_dimensions, core_geometry_recognize_feature.py
