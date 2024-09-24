let scene, camera, renderer, tooltip, controls;
let mouse = new THREE.Vector2();
let plate;
let holes = [];
let raycaster = new THREE.Raycaster();

function init() {
  const container = document.getElementById('container');
  tooltip = document.getElementById('tooltip');

  // Create the scene
  scene = new THREE.Scene();

  // Set up the camera
  camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
  camera.position.set(0, 0, 50);

  // Set up the renderer
  renderer = new THREE.WebGLRenderer();
  renderer.setSize(window.innerWidth, window.innerHeight);
  renderer.setClearColor(0xaaaaaa);  // Set background color
  container.appendChild(renderer.domElement);

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

  // Make sure the tooltip is hidden initially
  hideTooltip();

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
      });

      // Store the holes data for further use (e.g., displaying tooltips)
      holes = data.holes;
      
      // Process and display the holes in the UI categorized by diameter
      processHoleData(data.holes);
  })
  .catch(error => console.error('Error loading STL:', error));
}

function onMouseMove(event) {
  // Convert mouse position to normalized device coordinates (-1 to +1) for raycasting
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  // Perform raycasting only if the plate is defined
  if (plate) {
      raycaster.setFromCamera(mouse, camera);

      // Check if the ray intersects with the 3D object (plate)
      let intersects = raycaster.intersectObject(plate, true);

      if (intersects.length > 0) {
          // Find the nearest hole to the intersection point
          let closestHole = findClosestHole(intersects[0].point);

          if (closestHole) {
              // Display tooltip with hole data
              showTooltip(event, closestHole);
          } else {
              hideTooltip();
          }
      } else {
          hideTooltip();
      }
  } else {
      hideTooltip(); // Ensure the tooltip is hidden if the plate isn't ready
  }
}


// Find the closest hole to the given point
function findClosestHole(point) {
  let closestHole = null;
  let minDistance = Infinity;

  holes.forEach(hole => {
      let holePosition = new THREE.Vector3(hole.position.x, hole.position.y, hole.position.z);
      let distance = holePosition.distanceTo(point);

      if (distance < 0.1 && distance < minDistance) {  // Adjust distance threshold as needed
          closestHole = hole;
          minDistance = distance;
      }
  });

  return closestHole;
}

// Show the tooltip with hole data
function showTooltip(event, hole) {
  const x = event.clientX;
  const y = event.clientY;

  tooltip.style.left = `${x + 10}px`;  // Position the tooltip near the mouse
  tooltip.style.top = `${y + 10}px`;
  tooltip.textContent = `Hole Diameter: ${hole.diameter.toFixed(2)} mm
                         Position: (${hole.position.x.toFixed(2)}, ${hole.position.y.toFixed(2)}, ${hole.position.z.toFixed(2)})
                         Depth: ${hole.depth.toFixed(2)} mm`;
  tooltip.style.display = 'block';
}

// Hide the tooltip when the mouse is not near a hole
function hideTooltip() {
  tooltip.style.display = 'none';
}



function changeHoleSize(newSize) {
  // Send API request to backend to resize holes
  fetch('/api/change_hole_size', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ newSize })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error(`Error: ${response.statusText}`);
    }
    return response.json();
  })
  .then(data => {
    console.log('Hole size updated to:', newSize);
  })
  .catch(error => console.error('Error changing hole size:', error));
}

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
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
  holes.forEach(hole => {
      const diameter = Math.round(hole.diameter);
      if (!categorizedHoles[diameter]) {
          categorizedHoles[diameter] = [];
      }
      categorizedHoles[diameter].push(hole);
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
      holeGroup.forEach(hole => {
          const holeItem = document.createElement('li');
          holeItem.textContent = `Position: (${hole.position.x.toFixed(2)}, ${hole.position.y.toFixed(2)}, ${hole.position.z.toFixed(2)}), Depth: ${hole.depth.toFixed(2)} mm`;
          holeList.appendChild(holeItem);
      });

      dropdownContent.appendChild(holeList);
      dropdownSection.appendChild(dropdownHeader);
      dropdownSection.appendChild(dropdownContent);
      holeDataContainer.appendChild(dropdownSection);

      // Log each section as it gets appended
      console.log("Appended dropdown section for diameter:", diameter);
  }
}



function displayHoleData(categorizedHoles) {
  const holeDataContainer = document.getElementById('hole-data');
  if (!holeDataContainer) {
      console.error("Hole data container not found!");
      return;
  }

  holeDataContainer.innerHTML = '';  // Clear existing data

  for (const diameter in categorizedHoles) {
      const holeGroup = categorizedHoles[diameter];

      // Create a dropdown section for each diameter
      const dropdownSection = document.createElement('div');
      dropdownSection.className = 'dropdown-section';

      const dropdownHeader = document.createElement('div');
      dropdownHeader.className = 'dropdown-header';
      dropdownHeader.textContent = `Holes with Diameter: ${diameter} mm`;

      const dropdownContent = document.createElement('div');
      dropdownContent.className = 'dropdown-content';

      const holeList = document.createElement('ul');
      holeGroup.forEach((hole, index) => {
          const holeItem = document.createElement('li');
          holeItem.innerHTML = `
              Position: (${hole.position.x.toFixed(2)}, ${hole.position.y.toFixed(2)}, ${hole.position.z.toFixed(2)}), 
              Depth: ${hole.depth.toFixed(2)} mm 
              <button onclick="editHoleDiameter(${diameter}, ${index})">Edit Diameter</button>
          `;
          holeList.appendChild(holeItem);
      });

      dropdownContent.appendChild(holeList);
      dropdownSection.appendChild(dropdownHeader);
      dropdownSection.appendChild(dropdownContent);
      holeDataContainer.appendChild(dropdownSection);

      // Add click event to toggle dropdown visibility
      dropdownHeader.addEventListener('click', () => {
          dropdownContent.style.display = dropdownContent.style.display === 'none' ? 'block' : 'none';
      });
  }
}

// Function to handle diameter editing (for future implementation)
function editHoleDiameter(diameter, index) {
  console.log(`Editing hole with diameter ${diameter} mm, index: ${index}`);
  // Placeholder for future diameter editing logic
}


function animate() {
  requestAnimationFrame(animate);
  controls.update();  // Update OrbitControls for smooth interactions
  renderer.render(scene, camera);
}

init();
