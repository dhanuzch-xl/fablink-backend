let scene, camera, renderer, raycaster, tooltip, controls;
let mouse = new THREE.Vector2();
let plate;
let holes = [];

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

  // File input handler
  const fileInput = document.getElementById('file-input');
  fileInput.addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
      uploadAndLoadFile(file);
    }
  });

  // Raycaster for mouse interactions
  raycaster = new THREE.Raycaster();
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
      console.log('Holes Data:', data.holes);  // Log the holes data

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
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  
  // Check if 'plate' is defined and is a mesh object
  if (!plate || !plate.isMesh) {
    return;  // Prevent further execution if 'plate' is not ready
  }

  const intersects = raycaster.intersectObject(plate);
  if (intersects.length > 0) {
    const hole = findNearestHole(intersects[0].point);
    if (hole) {
      tooltip.style.display = 'block';
      tooltip.style.left = `${event.clientX + 5}px`;
      tooltip.style.top = `${event.clientY + 5}px`;
      tooltip.innerHTML = `
        Diameter: ${hole.diameter} mm<br>
        Coordinates: (${hole.position.x.toFixed(2)}, ${hole.position.y.toFixed(2)}, ${hole.position.z.toFixed(2)})
      `;
    } else {
      tooltip.style.display = 'none';
    }
  } else {
    tooltip.style.display = 'none';
  }
}

function findNearestHole(point) {
  let minDist = Infinity;
  let nearestHole = null;

  holes.forEach(hole => {
    const dist = Math.sqrt(
      Math.pow(point.x - hole.position.x, 2) +
      Math.pow(point.y - hole.position.y, 2) +
      Math.pow(point.z - hole.position.z, 2)
    );
    if (dist < minDist) {
      minDist = dist;
      nearestHole = hole;
    }
  });

  return (minDist < 1) ? nearestHole : null;
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

// Helper function to categorize and display hole data
function processHoleData(holes) {
  const categorizedHoles = {};

  // Categorize holes by diameter
  holes.forEach(hole => {
      const diameter = Math.round(hole.diameter);  // Round the diameter for easier categorization
      if (!categorizedHoles[diameter]) {
          categorizedHoles[diameter] = [];
      }
      categorizedHoles[diameter].push(hole);
  });

  // Display hole data in the UI
  displayHoleData(categorizedHoles);
}

// Helper function to display hole data on the webpage
function displayHoleData(categorizedHoles) {
  const holeDataContainer = document.getElementById('hole-data');
  holeDataContainer.innerHTML = '';  // Clear existing data

  for (const diameter in categorizedHoles) {
      const holeGroup = categorizedHoles[diameter];

      // Create a section for each diameter
      const diameterSection = document.createElement('div');
      diameterSection.innerHTML = `<h3>Holes with Diameter: ${diameter} mm</h3>`;

      const holeList = document.createElement('ul');
      holeGroup.forEach(hole => {
          const holeItem = document.createElement('li');
          holeItem.textContent = `Position: (${hole.position.x.toFixed(2)}, ${hole.position.y.toFixed(2)}, ${hole.position.z.toFixed(2)}), Depth: ${hole.depth.toFixed(2)} mm`;
          holeList.appendChild(holeItem);
      });

      diameterSection.appendChild(holeList);
      holeDataContainer.appendChild(diameterSection);
  }
}


function animate() {
  requestAnimationFrame(animate);
  controls.update();  // Update OrbitControls for smooth interactions
  renderer.render(scene, camera);
}

init();
