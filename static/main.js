let scene, camera, renderer, tooltip, controls;
let mouse = new THREE.Vector2();
let plate;
let edges_scale;
let holes = [];
let raycaster = new THREE.Raycaster();
let selectedHole = null; // Keeps track of the currently locked/selected hole
let highlightedHoleMesh = null;
let highlightedEdge = null; // Keeps track of the currently
let selectedEdges = [];  // Initialize the selectedEdges array
let lockedDropdownItem = null;  // Track the locked dropdown item
let detectedHole = null; // Track the detected hole for selection

function init() {
  const container = document.getElementById('container');
  tooltip = document.getElementById('tooltip');

  // Create the scene
  scene = new THREE.Scene();

  const rect = container.getBoundingClientRect();
  // Set up the renderer with the size of the container
  renderer = new THREE.WebGLRenderer();
  renderer.setSize(rect.width, rect.height);  // Match the container's size
  renderer.setClearColor(0xaaaaaa);  // Set background color
  container.appendChild(renderer.domElement);

  // Adjust the camera's aspect ratio to match the container
  camera = new THREE.PerspectiveCamera(75, rect.width / rect.height, 0.1, 1000);
  camera.position.set(0, 0, 50);

  // Add OrbitControls
  controls = new THREE.OrbitControls(camera, renderer.domElement);
  controls.enableDamping = true;
  controls.dampingFactor = 0.25;
  controls.screenSpacePanning = false;
  controls.maxPolarAngle = Math.PI / 2;

  // Lighting
  const light = new THREE.DirectionalLight(0xffffff, 2);
  light.position.set(100, 100, 100);
  scene.add(light);

  const ambientLight = new THREE.AmbientLight(0x404040, 0.5);
  scene.add(ambientLight);

  // Add axes for debugging
  const axesHelper = new THREE.AxesHelper(10);
  scene.add(axesHelper);


  // File input handler
  const fileInput = document.getElementById('file-input');
  fileInput.addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
      uploadAndLoadFile(file);
    }
  });

  // Raycaster for mouse interactions
  document.addEventListener('mousemove', onMouseMove, false);

  // Handle window resize
  window.addEventListener('resize', onWindowResize, false);

  // Start the animation loop
  animate();
}


function editHoleDiameter(diameter, index) {
    const newDiameter = prompt(`Enter new diameter for hole with current diameter ${diameter} mm:`, diameter);
    if (newDiameter !== null && !isNaN(newDiameter)) {
        // Update the hole's diameter locally
        holes[index].diameter = parseFloat(newDiameter);
       
       // add job to list
        addJob('hole', holes[index], 'Hole diameter changed', newDiameter);
        // Update the hole in the model in real-time
        updateHoleInModel(index, parseFloat(newDiameter));
  
        // Send the updated diameter and hole data to the backend
        const stepFile = document.getElementById('file-input').files[0]?.name;  // Ensure a file is selected
        if (!stepFile) {
            console.error('No STEP file selected for modification.');
            return;
        }
  
        fetch('/api/change_hole_size', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                newSize: parseFloat(newDiameter),
                holeData: holes[index],  // Send the updated hole data
                stepFile: stepFile  // Send the current step file name
            })
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();  // Expect JSON response from the backend
        })
        .then(data => {
            console.log(`Server response:`, data);
  
            // Use the modified STL file URL to reload the model
            const modifiedStlUrl = data.modified_stl_file;
            reloadModifiedModel(modifiedStlUrl);  // Load the updated STL model
        })
        .catch(error => console.error('Error updating hole size:', error));
    }
  }


  function uploadAndLoadFile(file) {
    const formData = new FormData();
    formData.append('file', file);
  
    fetch('http://127.0.0.1:5000/api/upload_file', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('STL URL:', data.stlUrl);
        // console.log('Holes Data:', data.holes);  // Log the holes data
  
        // Load the STL model
        const loader = new THREE.STLLoader();
        loader.load('http://127.0.0.1:5000' + data.stlUrl, function (geometry) {
            const material = new THREE.MeshPhongMaterial({ color: 0x0077ff, specular: 0x111111, shininess: 200 });
            plate = new THREE.Mesh(geometry, material);
            plate.scale.set(0.1, 0.1, 0.1);
            scene.add(plate);

            // Store and process the edges data (calling the createEdgesFromBackend function)
            if (data.edges) {
                createEdgesFromBackend(data.edges);  // Call the function to create edges from backend data
            }
        });
  
        // Store and process the holes data
        holes = data.holes;
        //processHoleData(data.holes);
  
 
  
    })
    .catch(error => console.error('Error loading STL:', error));
  }
  
  document.getElementById('container').addEventListener('click', (event) => {
    let hasHoleHighlighted = highlightedHoleMesh !== null;
    let hasEdgeHighlighted = highlightedEdge !== null;

    // If a hole is highlighted
    if (hasHoleHighlighted) {
        toggleHoleLock(detectedHole);  // Lock or unlock the detected hole
      // Hide "Weld" and "Fold" options when a hole is selected
    }

    // If an edge is highlighted
    if (hasEdgeHighlighted) {
        toggleEdgeLock(highlightedEdge, event);  // Toggle lock for the highlighted edge
    }


    // If neither a hole nor an edge is highlighted, clear selections and hide all options
    if (!hasHoleHighlighted && !hasEdgeHighlighted) {
        selectedEdges.forEach(e => removeHighlightFromEdge(e));
        selectedEdges = [];

        // Hide all options since nothing is highlighted
        hideWeldFoldOptions();
        hideStudUploadOptions();
    }
});


// Prevent deselection when interacting with file input
document.getElementById('stud-file-input').addEventListener('click', function(event) {
    event.stopPropagation();  // Prevent triggering the container click logic when selecting stud file
});


function onMouseMove(event) {
  if (selectedHole) {
    // Do not allow hover highlighting if a hole is selected
    return;
  }
  // Get the CAD viewer (container) size and position
  const container = document.getElementById('container');
  const rect = container.getBoundingClientRect();
  
  // Convert mouse position to normalized device coordinates (-1 to +1) relative to the CAD viewer
  mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
  mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;


  // Perform raycasting only if the plate is defined
  if (plate) {

    raycaster.setFromCamera(mouse, camera);
    //visualizeRaycasting();  // Visualize the raycaster's direction

    // Check if the ray intersects with the 3D object (plate)
    let intersects = raycaster.intersectObject(plate, true);
    // console.log("Raycaster Intersects:", intersects);
    if (intersects.length > 0) {
        // Find the nearest hole to the intersection point
        let closestHole = findClosestHole(intersects[0].point);
        
        if (closestHole) {
            // Highlight corresponding hole in dropdown
          highlightHoleInModel(closestHole);
         // highlightHoleInDropdown(closestHole);
         // displayHoleInfo(closestHole);
         showTooltip(event, closestHole);
        } else {
          removeHighlightFromModel();
          //removeHighlightFromDropdown();  // Remove highlight if no hole is detected
          //clearHoleInfo();  // Clear hole info if no hole is detected
          hideTooltip();
        }

        // Find the nearest edge to the intersection point
        const closestEdge = findNearestEdge(intersects[0].point);
        if (closestEdge) {
        highlightEdge(closestEdge);  // Highlight the found edge
        } else {
          removeHighlightFromEdge();  // Remove highlight if no edge is detected
        } 
    } else {
      removeHighlightFromModel();
      //removeHighlightFromDropdown();
      removeHighlightFromEdge();  // Remove highlight if no edge is detected
      hideTooltip();
    }
  } else {
    removeHighlightFromModel();
    //removeHighlightFromDropdown();
    removeHighlightFromEdge();  // Remove highlight if no edge is detected
    hideTooltip();
  }

}
function visualizeRaycasting() {
  // Remove existing arrow helper to avoid stacking
  if (window.arrowHelper) {
      scene.remove(window.arrowHelper);
  }

  // Adjust the length of the arrow to something smaller, e.g., 5 units instead of 20
  window.arrowHelper = new THREE.ArrowHelper(raycaster.ray.direction, raycaster.ray.origin, 5, 0xff0000);  // Length of 5
  scene.add(window.arrowHelper);
}



function findClosestHole(point) {
  let closestHole = null;
  let minDistance = Infinity;  // Minimum "effective" distance


  // Scale the intersection point back to the original model size
  const unscaledIntersectionPoint = new THREE.Vector3(
      point.x / plate.scale.x,  // Scale up by inverse of the scaling factor
      point.y / plate.scale.y,
      point.z / plate.scale.z
  );


  // Iterate over all holes in the original unscaled space
  holes.forEach(function (hole, index) {
      const holePosition = new THREE.Vector3(hole.position.x, hole.position.y, hole.position.z);

      // Calculate the distance between the intersection point (scaled up) and the hole center
      const distanceToCenter = holePosition.distanceTo(unscaledIntersectionPoint);

      // Calculate the hole's radius (no scaling required, since we're comparing in unscaled space)
      const holeRadius = hole.diameter / 2;

      // Effective distance: how close the point is to the edge of the hole
      const effectiveDistance = distanceToCenter - holeRadius;

      // If the effective distance is smaller than both the threshold and the minimum effective distance
      if (effectiveDistance < 10 && Math.abs(effectiveDistance) < minDistance) {  // Point is within the hole's radius
          closestHole = hole;  // Update the closest hole
          minDistance = Math.abs(effectiveDistance);  // Update the minimum distance

      }
  });
  detectedHole = closestHole;
  return closestHole;
}



// Function to show the tooltip
function showTooltip(event, hole) {
    const tooltip = document.getElementById('tooltip');
  
    // Set the content of the tooltip (diameter and position)
    tooltip.innerHTML = `
      <strong>Hole Diameter:</strong> ${hole.diameter.toFixed(2)} mm<br>
      <strong>Position:</strong> (${hole.position.x.toFixed(2)}, ${hole.position.y.toFixed(2)}, ${hole.position.z.toFixed(2)})
    `;
  
    // Position the tooltip near the mouse pointer
    tooltip.style.left = event.pageX + 15 + 'px';
    tooltip.style.top = event.pageY + 15 + 'px';
  
    // Show the tooltip
    tooltip.style.display = 'block';
  }
  
  // Function to hide the tooltip
  function hideTooltip() {
    const tooltip = document.getElementById('tooltip');
    tooltip.style.display = 'none';
  }


// Function to highlight the corresponding hole in the dropdown
function highlightHoleInDropdown(hole) {
    const holeDataContainer = document.getElementById('hole-data');
    const dropdownSections = holeDataContainer.getElementsByClassName('dropdown-section');

    // Remove existing highlights
    removeHighlightFromDropdown();

    // Loop through dropdown sections and highlight the matching hole
    Array.from(dropdownSections).forEach((section) => {
        const holeItems = section.getElementsByTagName('li');
        Array.from(holeItems).forEach((item) => {
            if (item.textContent.includes(`(${hole.position.x.toFixed(2)}, ${hole.position.y.toFixed(2)}, ${hole.position.z.toFixed(2)})`)) {
                item.style.backgroundColor = 'yellow';  // Highlight the corresponding hole
                lockedDropdownItem = item;  // Lock this item
            }
        });
    });
}

// Function to remove the highlight from the dropdown
function removeHighlightFromDropdown() {
    const holeDataContainer = document.getElementById('hole-data');
    const highlightedItems = holeDataContainer.querySelectorAll('li[style*="background-color"]');

    // Remove the background color from all highlighted items
    Array.from(highlightedItems).forEach(item => {
        item.style.backgroundColor = '';
    });
}

// Function to highlight the hole in the 3D model
function highlightHoleInModel(hole) {
  // Remove previous highlight if it exists
  if (highlightedHoleMesh) {
      scene.remove(highlightedHoleMesh);
  }

  // Create a small sphere to highlight the hole
  const geometry = new THREE.SphereGeometry(0.2, 16, 16);  // Adjust size if necessary
  const material = new THREE.MeshBasicMaterial({ color: 0xffff00 });
  highlightedHoleMesh = new THREE.Mesh(geometry, material);

  // Set the position to the hole's position, but account for the scaling of the model
  highlightedHoleMesh.position.set(
      hole.position.x * plate.scale.x,  // Scale the x-coordinate
      hole.position.y * plate.scale.y,  // Scale the y-coordinate
      hole.position.z * plate.scale.z   // Scale the z-coordinate
  );

  // Add the highlight to the scene
  scene.add(highlightedHoleMesh);
}

// Function to remove the highlight from the model
function removeHighlightFromModel() {
  // Remove the highlighted mesh if it exists
  if (highlightedHoleMesh) {
      scene.remove(highlightedHoleMesh);
      highlightedHoleMesh = null;
  }
}

// Function to toggle the lock when clicking a hole
function toggleHoleLock(hole) {
    if (selectedHole === hole) {
        // Unlock the hole if it was already selected
        selectedHole = null;
        removeHighlightFromModel();
        //removeHighlightFromDropdown();
        hideStudUploadOptions();       // Show "Stud Upload" and "Edit Diameter" when a hole is selected
        //hideWeldFoldOptions();  

        // Hide the stud file input when no hole is selected
        document.getElementById('stud-file-input').style.display = 'none';
        document.getElementById('edit-diameter-input').style.display = 'none';
        document.getElementById('edit-diameter-label').style.display = 'none';

    
      } else {
        
        selectedHole = hole;
        highlightHoleInModel(hole);
        showStudUploadOptions();       // Show "Stud Upload" and "Edit Diameter" when a hole is selected

    }
}

// Add event listener for Edit Diameter button
document.getElementById('edit-diameter-input').addEventListener('click', function () {
  if (selectedHole) {
      const index = holes.findIndex(hole => hole === selectedHole);
      if (index !== -1) {
          editHoleDiameter(selectedHole.diameter, index);
      } else {
          console.error('Selected hole not found in the holes array.');
      }
  } else {
      console.error('No hole selected.');
  }
});


// When the user selects a file for the stud
document.getElementById('stud-file-input').addEventListener('change', function () {
    const studFile = document.getElementById('stud-file-input').files[0]; // Get the selected stud STEP file
    if (!studFile) {
        alert('Please select a STEP file for the stud.');
        return;
    }

    // Send the STEP file to the server for conversion
    const formData = new FormData();
    formData.append('file', studFile);

    fetch('http://127.0.0.1:5000/api/upload_stud', {
        method: 'POST',
        body: formData,
        headers: {
            'Accept': 'application/json', // No 'Content-Type', it will be set automatically.
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`Error: ${response.statusText}`);
        }
        return response.json();
    })
    .then(data => {
        console.log('STL URL for Stud:', data.stlUrl);

        // Load the STL model of the stud
        const loader = new THREE.STLLoader();
        loader.load('http://127.0.0.1:5000' + data.stlUrl, function (geometry) {
            placeStudInHole(geometry, selectedHole);  // Place the stud in the selected hole
        });
    })
    .catch(error => console.error('Error uploading and loading the stud STL:', error));
});

function placeStudInHole(studGeometry, hole) {
  // Create a material for the stud mesh
  const studMesh = new THREE.Mesh(studGeometry, new THREE.MeshPhongMaterial({ color: 0xff0000 }));

  // Recompute the bounding box of the stud to get its dimensions
  studGeometry.computeBoundingBox(); // Ensure bounding box is computed
  studGeometry.center(); // Center the geometry before scaling

  // Calculate the bounding box of the stud to determine its diameter
  const boundingBox = studGeometry.boundingBox; // Use geometry bounding box instead of fromObject
  const studDiameter = boundingBox.max.x - boundingBox.min.x;  // Assuming the stud is cylindrical in the X direction

  console.log('Detected stud diameter:', studDiameter);  // Debugging

  // Get the hole diameter
  const holeDiameter = hole.diameter;

  // Calculate the scale factor to match the hole diameter, accounting for plate scaling
  const scale = (holeDiameter / studDiameter) * plate.scale.x; // Include plate's scale in calculation

  console.log('Calculated scale:', scale);

  // Apply the scale uniformly to the stud mesh, considering the plate's scale
  studMesh.scale.set(scale, scale, scale);

  // Set the scaled stud position to the selected hole's position
  studMesh.position.set(
      hole.position.x * plate.scale.x,
      hole.position.y * plate.scale.y,
      hole.position.z * plate.scale.z
  );

  // Ensure the holeAxis is a THREE.Vector3 object
  const holeAxis = new THREE.Vector3(hole.axis.x, hole.axis.y, hole.axis.z);
  const defaultAxis = new THREE.Vector3(0, 0, 1); // Assuming the stud is aligned along the Z-axis by default

  // Normalize the axis vectors
  holeAxis.normalize();
  defaultAxis.normalize();

  // Calculate the quaternion for rotation to align the stud with the hole's axis
  const quaternion = new THREE.Quaternion().setFromUnitVectors(defaultAxis, holeAxis);
  studMesh.quaternion.copy(quaternion);

  // Add the scaled stud to the scene
  scene.add(studMesh);

  // Ensure the scene is rendered after adding the stud
  renderer.render(scene, camera);

  // Add the job to the job list, including the studMesh so we can remove it later
  addJob('stud', hole, 'Placed stud in the selected hole', { studMesh });
}


function removeStudFromHole(jobId) {
  // Find the job using its ID
  console.log('called to remove stud from hole');
  const job = jobs.find(j => j.id === jobId);

  // Ensure that the job is of type 'stud'
  if (!job || job.type !== 'stud') {
      console.error('The job is not related to a stud or was not found.');
      return;
  }

  // Get the stud mesh associated with the job
  const studMesh = job.additionalInfo?.studMesh;

  // Remove the stud mesh from the scene
  if (studMesh) {
      scene.remove(studMesh);
      renderer.render(scene, camera);  // Re-render the scene after removing the stud
      console.log('Stud removed from the selected hole.');
  } else {
      console.error('No stud mesh found to remove or stud mesh not provided in additionalInfo.');
  }

  // No need to remove the job from the jobs array here as it's already handled in handleUndo.
}

function reloadModifiedModel(stlUrl) {
  // Remove the current plate from the scene, if it exists
  if (plate) {
      scene.remove(plate);
      plate.geometry.dispose();  // Clean up resources
      plate.material.dispose();  // Clean up resources
  }

  // Load the updated STL model from the modified STEP file
  const loader = new THREE.STLLoader();
  loader.load(stlUrl, function (geometry) {
      const material = new THREE.MeshPhongMaterial({ color: 0x0077ff, specular: 0x111111, shininess: 200 });
      plate = new THREE.Mesh(geometry, material);
      plate.scale.set(0.1, 0.1, 0.1);  // Adjust scaling if necessary
      scene.add(plate);
      console.log('Updated STL model loaded and added to the scene.');
  }, 
  function (xhr) {
      console.log((xhr.loaded / xhr.total * 100) + '% loaded');
  },
  function (error) {
      console.error('An error occurred while loading the STL model:', error);
  });
}

function updateHoleInModel(holeIndex, newDiameter) {
  const hole = holes[holeIndex];

  // Remove the old hole highlight (if any)
  if (highlightedHoleMesh) {
      scene.remove(highlightedHoleMesh);
      highlightedHoleMesh = null;
  }

  // Create a new hole with the updated diameter
  const geometry = new THREE.SphereGeometry(newDiameter / 2, 16, 16);  // Adjust the geometry to the new diameter
  const material = new THREE.MeshBasicMaterial({ color: 0xffff00 });  // You can change the color as needed
  highlightedHoleMesh = new THREE.Mesh(geometry, material);

  // Set the position of the new hole (considering the scale)
  highlightedHoleMesh.position.set(
      hole.position.x * plate.scale.x,
      hole.position.y * plate.scale.y,
      hole.position.z * plate.scale.z
  );

  // Add the updated hole to the scene
  scene.add(highlightedHoleMesh);
}



function onWindowResize() {
  const container = document.getElementById('container');
  const rect = container.getBoundingClientRect();

  camera.aspect = rect.width / rect.height;  // Set aspect ratio to container's dimensions
  camera.updateProjectionMatrix();
  renderer.setSize(rect.width, rect.height);  // Resize the renderer to match the container
}

function processHoleData(holes) {
  console.log("Processing hole data: ", holes);  // Debugging log
  const holeDataContainer = document.getElementById('hole-data');
  if (!holeDataContainer) {
      console.error("Hole data container not found!");
      return;
  }

  holeDataContainer.innerHTML = '';  // Clear existing data

  // Log hole data insertion
  console.log("Hole data container found, inserting data...");

  const categorizedHoles = {};
  holes.forEach((hole, index) => {
      const diameter = Math.round(hole.diameter);
      if (!categorizedHoles[diameter]) {
          categorizedHoles[diameter] = [];
      }
      categorizedHoles[diameter].push({ hole, index });  // Include the index for future editing
  });

  for (const diameter in categorizedHoles) {
      const holeGroup = categorizedHoles[diameter];

      const dropdownSection = document.createElement('div');
      dropdownSection.className = 'dropdown-section';

      const dropdownHeader = document.createElement('div');
      dropdownHeader.className = 'dropdown-header';
      dropdownHeader.textContent = `Holes with Diameter: ${diameter} mm`;

      const dropdownContent = document.createElement('div');
      dropdownContent.className = 'dropdown-content';

      const holeList = document.createElement('ul');
      holeGroup.forEach(({ hole, index }) => {
          const holeItem = document.createElement('li');
          holeItem.innerHTML = `
          Position: (${hole.position.x.toFixed(2)}, ${hole.position.y.toFixed(2)}, ${hole.position.z.toFixed(2)})
      `;
          holeList.appendChild(holeItem);
      });

      dropdownContent.appendChild(holeList);
      dropdownSection.appendChild(dropdownHeader);
      dropdownSection.appendChild(dropdownContent);
      holeDataContainer.appendChild(dropdownSection);

      // Add click event to toggle dropdown visibility
      dropdownHeader.addEventListener('click', () => {
        if (dropdownContent.style.display === 'none') {
            dropdownContent.style.display = 'block';
        } else {
            dropdownContent.style.display = 'none';
        }
      });
  }
}
// Function to display hole information in the hole-data container
function displayHoleInfo(hole) {
    const holeDataContainer = document.getElementById('hole-data');
    
    // Create hole info text with position and diameter
    const holeInfo = `
      <div class="hole-info">
        <strong>Hole Diameter:</strong> ${hole.diameter.toFixed(2)} mm<br>
        <strong>Position:</strong> (${hole.position.x.toFixed(2)}, ${hole.position.y.toFixed(2)}, ${hole.position.z.toFixed(2)})
      </div>
    `;
    
    // Update the hole-data container with the hole information
    holeDataContainer.innerHTML = holeInfo;
  }
  
  // Function to clear hole information when no hole is hovered
  function clearHoleInfo() {
    const holeDataContainer = document.getElementById('hole-data');
    holeDataContainer.innerHTML = '<h2>Hole Data</h2>';  // Reset to default header
  }
function visualizeHolePositions() {
  holes.forEach(hole => {
      const geometry = new THREE.SphereGeometry(0.5, 16, 16);  // Adjust size if necessary
      const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });  // Green color for the hole markers
      const sphere = new THREE.Mesh(geometry, material);
      
      sphere.position.set(
          hole.position.x * plate.scale.x,
          hole.position.y * plate.scale.y,
          hole.position.z * plate.scale.z
      );
      scene.add(sphere);
  });
}

const edgesArray = [];  // Array to store dynamically created edge objects

    // Function to create edge objects from backend data
function createEdgesFromBackend(edgeData) {
  edgeData.forEach(edge => {
    const start = new THREE.Vector3(edge.start.x, edge.start.y, edge.start.z);
    const end = new THREE.Vector3(edge.end.x, edge.end.y, edge.end.z);

    // Apply the scale to the start and end points
    start.multiply(plate.scale);  
    end.multiply(plate.scale);

    // Create buffer geometry for the edge
    const geometry = new THREE.BufferGeometry().setFromPoints([start, end]);

    const material = new THREE.LineBasicMaterial({
      color: 0xff0000,  // Default red color
      //depthTest: false  // Disable depth testing
      });
  
  
      
    // Create a line (edge) object
    const edgeLine = new THREE.LineSegments(geometry, material);

    // Add the edge to the scene
    scene.add(edgeLine);

    // Log the material for debugging
    console.log('Edge material cloned:', material);

    // Store the edge in the edgesArray for raycasting
    edgesArray.push(edgeLine);
  });
}


function findNearestEdge(point) {
  let closestEdge = null;
  let minEffectiveDistance = Infinity;  // Minimum "effective" distance

  // Iterate over all edges
  edgesArray.forEach(function (edge) {
      // Get the start and end points of the edge
      const start = edge.geometry.attributes.position.array.slice(0, 3); // First 3 values
      const end = edge.geometry.attributes.position.array.slice(3, 6); // Next 3 values
      const edgeStart = new THREE.Vector3(start[0], start[1], start[2]);
      const edgeEnd = new THREE.Vector3(end[0], end[1], end[2]);

      // Calculate the distance from the intersection point to the edge
      const distanceToEdge = pointToLineDistance(point, edgeStart, edgeEnd);

      // Check if the distance is less than 0.1
      if (distanceToEdge < 0.1) {
          // Update the closest edge if the distance is less than the current minimum effective distance
          // if (distanceToEdge < minEffectiveDistance) {
          minEffectiveDistance = distanceToEdge;
          closestEdge = edge;  // Update the closest edge
          // }
      }
  });

  // Return the closest edge found, or null if no edges were within the specified distance
  return closestEdge;
}

// Helper function to calculate the distance from a point to a line segment
function pointToLineDistance(point, start, end) {
  const lineVector = new THREE.Vector3().subVectors(end, start);
  const lineLengthSquared = lineVector.lengthSq();
  if (lineLengthSquared === 0) return point.distanceTo(start); // Start and end points are the same

  const t = Math.max(0, Math.min(1, lineVector.dot(new THREE.Vector3().subVectors(point, start)) / lineLengthSquared));
  const closestPoint = new THREE.Vector3().copy(start).add(lineVector.multiplyScalar(t));
  return point.distanceTo(closestPoint);
}


// Function to highlight an edge in the 3D scene (using positional offset)
function highlightEdge(edge) {
  if (highlightedEdge) {
    // Reset the previously highlighted edge to its default color
    highlightedEdge.material.color.set(0xff0000);
    highlightedEdge.material.needsUpdate = true;

    // Reset the edge's position offset
    highlightedEdge.position.set(0, 0, 0);
  }


  // Highlight the new edge with a color change
  edge.material.color.set(0x000000);  // Set to black for highlighting
  //edge.material.depthTest = false;    // Ensure the line appears on top
  edge.material.needsUpdate = true;

  // Offset the position slightly to bring the edge "in front" of the plate
  edge.position.y += 0.05;  // Small offset along the Z-axis
  edge.geometry.needsUpdate = true;

  highlightedEdge = edge;
}

// Function to remove highlight from the current edge
function removeHighlightFromEdge() {
  if (highlightedEdge) {
    highlightedEdge.material.color.set(0xff0000);  // Reset to red
    highlightedEdge.material.needsUpdate = true;

    // Reset the edge's position offset
    highlightedEdge.position.set(0, 0, 0);
    highlightedEdge = null;
  }
}

// Function to toggle the lock on an edge when clicked
function toggleEdgeLock(edge, event) {
  // Check if the Control key (Ctrl) is pressed
  const isCtrlPressed = event.ctrlKey || event.metaKey;  // 'metaKey' for Mac (Command key)

    if (!isCtrlPressed) {
      // If Ctrl is not pressed, clear all previously selected edges
      selectedEdges.forEach(e => removeHighlightFromEdge(e));
      selectedEdges = [];
    }

  // If Ctrl is pressed or no edges are selected, continue the selection process
    else {
      // If selecting a third edge (when Ctrl is pressed), reset selection
      if (selectedEdges.length >= 2) {
          // Clear all previous selections
          selectedEdges.forEach(e => removeHighlightFromEdge(e));
          selectedEdges = [];
          console.log("reset selection")
      }
    }  
    if (!selectedEdges.includes(edge)) {  // Ensure the same edge is not added multiple times
  // Add the new edge to the selection and highlight it
      selectedEdges.push(edge);
      highlightEdge(edge);
    }
    // If exactly two edges are selected, show the weld/fold options
    if (selectedEdges.length === 2) {
        showWeldFoldOptions();
    }
    else{
        hideWeldFoldOptions();     // Hide "Weld" and "Fold" options if fewer or more than two edges are selected
    }
  }


  function showWeldFoldOptions() {
    const weldFoldOptions = document.getElementById('weld-fold-options');
    const weldFoldLabel = document.getElementById('weld-fold-label');

    // Show the fold/weld options
    weldFoldOptions.style.display = 'block';
    weldFoldLabel.style.display = 'block';

    // Optionally, handle further behavior based on user selection
    document.getElementById('weld-option').addEventListener('change', function() {
        if (this.checked) {
            console.log('Weld option selected');
            addJob('weld', selectedEdges[0].geometry.attributes.position, 'Welding two edges');

            // Call a function or perform logic specific to welding
        }
    });

    document.getElementById('fold-option').addEventListener('change', function() {
        if (this.checked) {
            console.log('Fold option selected');
            addJob('fold', selectedEdges[0].geometry.attributes.position, 'folding two edges');
            // Call a function or perform logic specific to folding
        }
    });
}

// Function to hide the weld/fold options (if needed)
function hideWeldFoldOptions() {
    const weldFoldOptions = document.getElementById('weld-fold-options');
    const weldFoldLabel = document.getElementById('weld-fold-label');
    weldFoldOptions.style.display = 'none';
    weldFoldLabel.style.display = 'none';
}

// Function to show "Stud Upload" and "Edit Diameter" options
function showStudUploadOptions() {
    document.getElementById('stud-file-label').style.display = 'block';
    document.getElementById('stud-file-input').style.display = 'block';
    document.getElementById('edit-diameter-label').style.display = 'block';
    document.getElementById('edit-diameter-input').style.display = 'block';
}

// Function to hide "Stud Upload" and "Edit Diameter" options
function hideStudUploadOptions() {
    document.getElementById('stud-file-label').style.display = 'none';
    document.getElementById('stud-file-input').style.display = 'none';
    document.getElementById('edit-diameter-label').style.display = 'none';
    document.getElementById('edit-diameter-input').style.display = 'none';
}


function animate() {
  requestAnimationFrame(animate);
  controls.update();  // Update OrbitControls for smooth interactions
  renderer.render(scene, camera);
}


let jobs = [];

// Generate a unique job ID for each job
function generateJobId() {
  return 'job-' + Math.random().toString(36).substr(2, 9);
}

  // Centralized undo handler function
  function handleUndo(jobId) {
    console.log('handleUndo is called');
    // Find the job using its ID

    const job = jobs.find(j => j.id === jobId);
    console.log('jobs',jobs);
    console.log('jobId',jobId);
    console.log('job',job);
    // Call the appropriate undo function depending on the job type
    if (job && job.type === 'stud') {
        removeStudFromHole(jobId);  // Call the function to undo the stud placement
    } else if (job && (job.type === 'weld' || job.type === 'fold')) {
        undoEdgeOperation(jobId);  // Assuming you have a function to undo weld or fold
    } else if (job && job.type === 'Edithole') {
        undoHoleEdit(jobId);  // Assuming you have a function to undo hole edits
    }

    // Remove the job from the jobs array by filtering it out
    jobs = jobs.filter(j => j.id !== jobId);  // Keep only jobs with a different ID
  }

// Add job to the list and display it in the UI
function addJob(type, data, description, additionalInfo = null) {
  let jobEntry;

  if (type === 'weld' || type === 'fold') {
      const start = new THREE.Vector3(
          data.getX(0), // x1
          data.getY(0), // y1
          data.getZ(0)  // z1
      );

      const end = new THREE.Vector3(
          data.getX(1), // x2
          data.getY(1), // y2
          data.getZ(1)  // z2
      );

      jobEntry = `Type: ${type}, Start: (${start.x.toFixed(2)}, ${start.y.toFixed(2)}, ${start.z.toFixed(2)}), ` +
                 `End: (${end.x.toFixed(2)}, ${end.y.toFixed(2)}, ${end.z.toFixed(2)}) - ${description}`;
  } else if (type === 'Edithole') {
      const position = data.position;  // Assuming data is an object that has a position property (THREE.Vector3)
      jobEntry = `Type: ${type}, Position: (${position.x.toFixed(2)}, ${position.y.toFixed(2)}, ${position.z.toFixed(2)}), ` +
                 `New Diameter: ${additionalInfo}mm - ${description}`;
  } else if (type === 'stud') {
      const position = data.position;  // Assuming data is the hole where the stud is placed
      jobEntry = `Type: ${type}, Stud Placed at: (${position.x.toFixed(2)}, ${position.y.toFixed(2)}, ${position.z.toFixed(2)}) - ${description}`;
  }

  console.log(jobEntry);  // For debugging

  // Generate a unique job ID
  const jobId = generateJobId();

  // Add job to the jobs array with a unique ID
  jobs.push({ id: jobId, type, data, description, additionalInfo });

  // Add job to the job list (DOM manipulation)
  const jobList = document.getElementById('jobs-list');
  const jobItem = document.createElement('div');
  jobItem.classList.add('job-entry');
  jobItem.setAttribute('data-job-id', jobId);
  jobItem.innerHTML = `<h3>${type}</h3><p>${jobEntry}</p>`;

  // Add the close button
  const closeButton = document.createElement('button');
  closeButton.textContent = 'Undo';
  closeButton.classList.add('close-button');
  
  // Attach job ID to the close button using a data-* attribute
  closeButton.setAttribute('data-job-id', jobId);  // Ensure this is correctly set

  // Attach the event listener for undoing the job
  closeButton.addEventListener('click', function(event) {
    // Get the job ID from the button's data attribute
    const jobId = event.target.getAttribute('data-job-id');
    // Call the centralized undo handler
    handleUndo(jobId);

    // Remove the job entry from the DOM
    jobItem.remove();
  });

  jobItem.appendChild(closeButton);
  jobList.appendChild(jobItem);
}


let reportTemplate = {};

// Function to fetch the report template
async function fetchReportTemplate() {
  try {
    const response = await fetch('/static/report_template.json'); // Ensure the correct path to the JSON file
    reportTemplate = await response.json();
    console.log("Template fetched: ", reportTemplate);
  } catch (error) {
    console.error("Error fetching report template: ", error);
  }
}

// Function to generate the report based on the template and jobs
function generateReport() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, '0');
  const day = String(now.getDate()).padStart(2, '0');
  const hours = String(now.getHours()).padStart(2, '0');
  const minutes = String(now.getMinutes()).padStart(2, '0');
  const seconds = String(now.getSeconds()).padStart(2, '0');
  const reportId = `${year}${month}${day}${hours}${minutes}${seconds}`;

  // Clone the template object so we don't modify the original template
  const report = JSON.parse(JSON.stringify(reportTemplate));
  report.item_id = reportId;  // Set the report ID

  // Iterate through the jobs array and fill in the report fields based on job types
  jobs.forEach(job => {
    switch (job.type) {
      case 'weld':
      case 'fold':
        report.services.welding.welds.push({
          weld_type: job.type,
          location: {
            start_point: job.data.start,
            end_point: job.data.end
          },
          weld_size: 5,
          weld_length: 100,
          weld_symbol: "AWS Symbol",
          post_weld_treatment: "Grinding",
          special_requirements: job.description
        });
        break;

      case 'Edithole':
        report.services.tapping.taps.push({
          quantity: 1,
          thread_size: "M4",
          thread_type: "Metric Coarse",
          hole_depth: 10,
          coordinates: [{ x: job.data.position.x, y: job.data.position.y, z: job.data.position.z }],
          hole_id: "hole1",
          special_instructions: `Hole edited, new diameter: ${job.additionalInfo}`
        });
        break;

      case 'stud':
        report.hardware_insertions.hardware.push({
          insertion_type: "standoff",
          hardware: {
            part_number: "ST123"
          },
          insertion_method: "Press-fit",
          quantity: 1,
          coordinates: [{ x: job.data.position.x, y: job.data.position.y, z: job.data.position.z }]
        });
        report.hardware_insertions.special_instructions = "Insert standoffs evenly";
        break;

      default:
        console.log(`Unrecognized job type: ${job.type}`);
    }
  });

  // Display the final report in the console (you can also display it on the page)
  console.log(JSON.stringify(report, null, 2));

  // Optionally, display the report in an alert or a DOM element
  alert("Report generated with ID: " + reportId + "\nCheck the console for details.");
}

// Attach the event listener to the submit button
document.getElementById('submit-report').addEventListener('click', generateReport);

// Fetch the report template when the script loads
fetchReportTemplate();

init();
