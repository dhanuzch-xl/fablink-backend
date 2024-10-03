    
1. **Item Details**:
   - **item_id**: A unique identifier for the part.

2. **Material Specifications**:
   - **type**: The material to be used (e.g., Aluminum).
   - **grade**: The material grade (e.g., 5052).
   - **thickness**: The thickness of the material in millimeters.
   - **hardness**: Optional field for the hardness rating (e.g., Rockwell).
   - **temper**: Optional field for temper condition (e.g., H32).
   - **grain_direction**: Optional field indicating the direction of the material's grain (e.g., longitudinal).

3. **Dimensions after Flattening**:
   - **length**: Length of the raw material after flattening.
   - **width**: Width of the raw material after flattening.

4. **Cutting Specifications**:
   - **type**: The type of cutting process (e.g., Laser).
   - **perimeter_length**: Total length of the cut perimeter in millimeters.
   - **number_of_piercings**: Number of piercings needed.
   - **edge_quality**: Internal setting for edge finish quality (e.g., High).
   - **tolerance**: Tolerance in millimeters.
   - **kerf_width**: The width of the cut produced by the laser or tool.
   - **special_instructions**: Any special instructions for cutting.

5. **Hardware Insertions**:
   - **hardware**: Contains a list of hardware insertion operations.
     - **insertion_type**: The type of hardware to be inserted (e.g., standoff, nut).
     - **hardware**: Part details like part number.
     - **insertion_method**: Method of insertion (e.g., press-fit, threaded).
     - **quantity**: Number of hardware items.
     - **coordinates**: Specifies the exact x, y, z location for the insertions.
   - **special_instructions**: Any special instructions for hardware insertion.

6. **Finish Specifications**:
   - **type**: Type of finish (e.g., Powder Coating).
   - **color**: Desired color (e.g., Black).
   - **thickness**: Thickness of the coating in microns.
   - **surface_prep**: Pre-treatment method (e.g., Sandblasting).
   - **masking**: Details masking areas for the finish if required.
     - **required**: Boolean indicating if masking is needed.
     - **areas**: Specifies the areas to be masked.
   - **coating_specification**: Coating specification, such as RAL standards.
   - **gloss_level**: Desired gloss level (e.g., Matte).
   - **texture**: Texture of the finish (e.g., Smooth).
   - **special_instructions**: Any special finish-related instructions.

7. **Services**:
   - **tapping**: Details about tapping operations (threading holes).
     - **taps**: List of tapping operations.
       - **quantity**: Number of holes to tap.
       - **thread_size**: Size of the thread (e.g., M4).
       - **thread_type**: Type of thread (e.g., Metric Coarse).
       - **hole_depth**: Depth of the hole.
       - **coordinates**: x, y, z coordinates of the hole.
       - **hole_id**: Unique identifier for the hole.
   - **bending**: Describes bending operations.
     - **bends**: List of bends to be performed.
       - **bend_radius**: The radius of each bend.
       - **bend_direction**: Direction of the bend (e.g., Up, Down).
       - **sequence**: Order in which bends are made.
       - **bend_angles**: Each bend's angle, length, and start/end coordinates.
   - **welding**: Describes welding operations.
     - **welds**: List of welding details.
       - **weld_type**: The type of welding (e.g., MIG, TIG).
       - **location**: Start and end points of the weld.
       - **weld_size**: The size of the weld in millimeters.
       - **post_weld_treatment**: Post-weld treatment like grinding.
   
8. **Quantity**: Specifies the quantity of items to manufacture.

9. **Custom Instructions**: Field to provide any special custom instructions for the entire job.
