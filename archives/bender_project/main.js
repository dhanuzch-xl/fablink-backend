// Initialize Three.js scene, camera, and renderer
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(4, 4, 6);

const renderer = new THREE.WebGLRenderer({ canvas: document.querySelector('#threejs-canvas') });
renderer.setSize(window.innerWidth, window.innerHeight);

// Add orbit controls
const controls = new THREE.OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;

// Define material and mesh (empty initially)
const material = new THREE.MeshBasicMaterial({ color: 0x00ff00, wireframe: true });
let geometry = new THREE.BoxGeometry(5, 5, 5, 10, 10, 10);
let mesh = new THREE.Mesh(geometry, material);
scene.add(mesh);
class Bender {
    // Store original vertex positions for potential resets
    constructor() {
        this.originalPositions = null;
    }

    storeOriginalPositions(geometry) {
        if (!this.originalPositions) {
            this.originalPositions = new Float32Array(geometry.attributes.position.array);
        }
    }

    resetGeometry(geometry) {
        if (this.originalPositions) {
            geometry.attributes.position.array.set(this.originalPositions);
            geometry.attributes.position.needsUpdate = true;
        }
    }

    bend(geometry, axis, angle) {
        let theta = 0;
        this.storeOriginalPositions(geometry);

        if (angle !== 0) {
            const v = geometry.attributes.position.array;
            for (let i = 0; i < v.length; i += 3) {
                let x = v[i];
                let y = v[i + 1];
                let z = v[i + 2];

                switch (axis) {
                    case "x":
                        theta = z * angle;
                        break;
                    case "y":
                        theta = x * angle;
                        break;
                    default: // z-axis
                        theta = x * angle;
                        break;
                }

                let sinTheta = Math.sin(theta);
                let cosTheta = Math.cos(theta);

                // Ensure we don't bend vertices too much or they may collide
                switch (axis) {
                    case "x":
                        v[i + 1] = (y - 1.0 / angle) * cosTheta + 1.0 / angle;
                        v[i + 2] = -(y - 1.0 / angle) * sinTheta;
                        break;
                    case "y":
                        v[i] = -(z - 1.0 / angle) * sinTheta;
                        v[i + 2] = (z - 1.0 / angle) * cosTheta + 1.0 / angle;
                        break;
                    default: // z-axis
                        v[i] = -(y - 1.0 / angle) * sinTheta;
                        v[i + 1] = (y - 1.0 / angle) * cosTheta + 1.0 / angle;
                        break;
                }
            }
            geometry.attributes.position.needsUpdate = true;
        }
    }
}


// Instantiate Bender
const bender = new Bender();

// Apply bending to the cube geometry initially
bender.bend(mesh.geometry, 'x', Math.PI / 16);

// Handle file upload for OBJ models
document.getElementById('fileInput').addEventListener('change', handleFileUpload);

function handleFileUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = function(e) {
        const contents = e.target.result;
        const objLoader = new THREE.OBJLoader();
        const obj = objLoader.parse(contents);

        obj.traverse(function(child) {
            if (child.isMesh) {
                scene.add(child);
                bender.bend(child.geometry, 'x', Math.PI / 16);  // Apply bending to OBJ
            }
        });
    };
    reader.readAsText(file);
}

// Setup dat.GUI
const gui = new dat.GUI({ autoPlace: false });
document.getElementById('gui-container').appendChild(gui.domElement);

// Store the original geometry before any transformation
let originalGeometry = mesh.geometry.clone();

const data = {
  axis: 'x',
  angle: Math.PI / 16,  // Set a reasonable default
  model: 'Cube',
};

// Add axis selection
gui.add(data, 'axis', ['x', 'y', 'z']).onChange(function(value) {
  resetGeometry(mesh);
  bender.bend(mesh.geometry, value, data.angle);
});

// Add angle slider with a reasonable range
gui.add(data, 'angle', -Math.PI / 2, Math.PI / 2, 0.01).onChange(function(value) {
  resetGeometry(mesh);
  bender.bend(mesh.geometry, data.axis, value);
});

// Function to reset geometry to its original state before each new bend
function resetGeometry(mesh) {
  mesh.geometry.copy(originalGeometry);
  mesh.geometry.attributes.position.needsUpdate = true;
}

// Resize handler
window.addEventListener('resize', onWindowResize);
function onWindowResize() {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
}

// Render loop
function animate() {
  requestAnimationFrame(animate);
  controls.update();
  renderer.render(scene, camera);
}

animate();
