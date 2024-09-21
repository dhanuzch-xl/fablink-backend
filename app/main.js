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
  controls.enableDamping = true;  // Smooth control
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

  // Load STL model
  const loader = new THREE.STLLoader();
  loader.load('http://localhost:5000/convert_step_to_stl/WP-2', function (geometry) {
    const material = new THREE.MeshPhongMaterial({ color: 0x0077ff, specular: 0x111111, shininess: 200 });
    plate = new THREE.Mesh(geometry, material);
    plate.scale.set(0.1, 0.1, 0.1);
    scene.add(plate);
  });

  // Raycaster for mouse interactions
  raycaster = new THREE.Raycaster();
  document.addEventListener('mousemove', onMouseMove, false);

  // Load hole data from JSON
    fetch('hole_data.json')
    .then(response => response.json())
    .then(data => {
      // Apply the same scale factor to the hole positions
      const scaleFactor = 0.1;  // Use the same scale factor as the STL model
      data.forEach(hole => {
        hole.position.x *= scaleFactor;
        hole.position.y *= scaleFactor;
        hole.position.z *= scaleFactor;
      });
      holes = data;
    });
  
  // Handle window resize
  window.addEventListener('resize', onWindowResize, false);

  // Start the animation loop
  animate();
}

function onMouseMove(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;

  raycaster.setFromCamera(mouse, camera);
  if (plate) {
    const intersects = raycaster.intersectObject(plate);

    if (intersects.length > 0) {
      const hole = findNearestHole(intersects[0].point);
      if (hole) {
        tooltip.style.display = 'block';
        tooltip.style.left = `${event.clientX + 5}px`;
        tooltip.style.top = `${event.clientY + 5}px`;
        tooltip.innerHTML = `
          Diameter: ${hole.diameter} mm<br>
          Depth: ${hole.depth} mm<br>
          Coordinates: (${hole.position.x.toFixed(2)}, ${hole.position.y.toFixed(2)}, ${hole.position.z.toFixed(2)})
        `
      } else {
        tooltip.style.display = 'none';
      }
    } else {
      tooltip.style.display = 'none';
    }
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

function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
  requestAnimationFrame(animate);
  controls.update();  // Update OrbitControls for smooth interactions
  renderer.render(scene, camera);
}

init();
