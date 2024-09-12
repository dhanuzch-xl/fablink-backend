import * as THREE from 'https://unpkg.com/three@0.126.1/build/three.module.js';
import { OBJLoader } from 'https://unpkg.com/three@0.126.1/examples/jsm/loaders/OBJLoader.js';
import { STLLoader } from 'https://unpkg.com/three@0.126.1/examples/jsm/loaders/STLLoader.js';
import { OrbitControls } from 'https://unpkg.com/three@0.126.1/examples/jsm/controls/OrbitControls.js';

let scene, camera, renderer, controls, raycaster, mouse;
let selectedObject = null;
const hoverColor = 0x00ff00;
const defaultColor = 0xff0000;

function init() {
    const container = document.getElementById('viewer');
    const width = container.clientWidth;
    const height = container.clientHeight;

    scene = new THREE.Scene();

    camera = new THREE.PerspectiveCamera(60, width / height, 0.1, 1000);
    camera.position.set(0, 0, 10);

    renderer = new THREE.WebGLRenderer({ antialias: true });
    renderer.setSize(width, height);
    renderer.setClearColor(0xffffff, 1);
    container.appendChild(renderer.domElement);

    controls = new OrbitControls(camera, renderer.domElement);
    controls.enableDamping = true;
    controls.minDistance = 0.1;
    controls.maxDistance = 100;
    controls.zoomSpeed = 1.2;
    controls.enablePan = true;
    controls.target.set(0, 0, 0);

    const ambientLight = new THREE.AmbientLight(0x404040, 2);
    scene.add(ambientLight);

    const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
    directionalLight.position.set(1, 1, 1).normalize();
    scene.add(directionalLight);

    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();

    window.addEventListener('resize', onWindowResize, false);
    window.addEventListener('mousemove', onMouseMove, false);
    window.addEventListener('click', onMouseClick, false);
    animate();
}

function onWindowResize() {
    const container = document.getElementById('viewer');
    const width = container.clientWidth;
    const height = container.clientHeight;
    
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
}

function onMouseMove(event) {
    mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
    mouse.y = -(event.clientY / window.innerHeight) * 2 + 1; // Invert the y-axis

    raycaster.setFromCamera(mouse, camera);

    const intersects = raycaster.intersectObjects(scene.children, true);

    if (intersects.length > 0) {
        if (selectedObject) {
            selectedObject.material.color.set(defaultColor);
        }
        selectedObject = intersects[0].object;
        selectedObject.material.color.set(hoverColor);
    } else {
        if (selectedObject) {
            selectedObject.material.color.set(defaultColor);
            selectedObject = null;
        }
    }
}

function onMouseClick(event) {
    if (selectedObject) {
        console.log('Selected line:', selectedObject);

        if (selectedObject.isLineSegments) {
            const positions = selectedObject.geometry.attributes.position;
            for (let i = 0; i < positions.count; i += 2) {
                const v1 = new THREE.Vector3().fromBufferAttribute(positions, i);
                const v2 = new THREE.Vector3().fromBufferAttribute(positions, i + 1);
                const length = v1.distanceTo(v2);

                console.log(`Line length: ${length.toFixed(2)}`);
            }
        }
    }
}

function animate() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene, camera);
}

function loadModel(filePath) {
    const extension = filePath.split('.').pop().toLowerCase();

    switch (extension) {
        case 'stl':
            loadSTL(filePath);
            break;
        case 'obj':
            loadOBJ(filePath);
            break;
        default:
            console.error('Unsupported file type:', extension);
            document.getElementById('feedback-message').textContent = 'Unsupported file format.';
    }
}

function loadSTL(filePath) {
    const loader = new STLLoader();
    loader.load(filePath, geometry => {
        const material = new THREE.MeshPhongMaterial({ color: defaultColor, wireframe: false });
        const mesh = new THREE.Mesh(geometry, material);

        const box = new THREE.Box3().setFromObject(mesh);
        const center = box.getCenter(new THREE.Vector3());
        mesh.position.sub(center);

        scene.add(mesh);
        extractEdges(mesh);

        const size = box.getSize(new THREE.Vector3());
        console.log(`Dimensions: Width = ${size.x.toFixed(2)}, Height = ${size.y.toFixed(2)}, Depth = ${size.z.toFixed(2)}`);
    }, onProgress, onError);
}

function loadOBJ(filePath) {
    const loader = new OBJLoader();
    loader.load(filePath, function (object) {
        const box = new THREE.Box3().setFromObject(object);
        const center = box.getCenter(new THREE.Vector3());
        object.position.sub(center);

        scene.add(object);
        extractEdges(object);

        const size = box.getSize(new THREE.Vector3());
        console.log(`Dimensions: Width = ${size.x.toFixed(2)}, Height = ${size.y.toFixed(2)}, Depth = ${size.z.toFixed(2)}`);
    }, onProgress, onError);
}

function extractEdges(object) {
    object.traverse(child => {
        if (child.isMesh) {
            const edgesGeometry = new THREE.EdgesGeometry(child.geometry);
            const edgesMaterial = new THREE.LineBasicMaterial({ color: defaultColor });
            const edges = new THREE.LineSegments(edgesGeometry, edgesMaterial);
            
            edges.position.copy(child.position);
            edges.rotation.copy(child.rotation);
            edges.scale.copy(child.scale);

            scene.add(edges);
        }
    });
}

function onProgress(xhr) {
    const feedbackMessage = document.getElementById('feedback-message');
    if (xhr.lengthComputable) {
        const percentComplete = Math.round((xhr.loaded / xhr.total) * 100);
        feedbackMessage.textContent = `Loading model: ${percentComplete}% complete`;
    }
}

function onError(error) {
    console.error('An error occurred while loading the model:', error);
    document.getElementById('feedback-message').textContent = 'Failed to load model. Please check the console for details.';
}

document.addEventListener('DOMContentLoaded', () => {
    init();

    document.getElementById('upload-button').addEventListener('click', function () {
        const input = document.getElementById('file-input');
        const file = input.files[0];
        const feedbackMessage = document.getElementById('feedback-message');

        if (!file) {
            feedbackMessage.textContent = 'Please select a file to upload.';
            return;
        }

        feedbackMessage.textContent = 'Uploading...';

        const formData = new FormData();
        formData.append('file', file);

        fetch('http://0.0.0.0:5000/upload', {  // Ensure your server is correctly set up to handle the upload
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.path) {
                feedbackMessage.textContent = 'Upload successful, loading model...';
                loadModel(data.path); // Load the correct file based on extension
            } else {
                feedbackMessage.textContent = 'Upload failed. Please try again.';
            }
        })
        .catch(error => {
            console.error('Error uploading file:', error);
            feedbackMessage.textContent = 'Error uploading file. Please check the console for more details.';
        });
    });
});
