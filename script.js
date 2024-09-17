// script.js

const svgNS = "http://www.w3.org/2000/svg";
const svg = document.createElementNS(svgNS, "svg");

svg.setAttribute("width", "800");
svg.setAttribute("height", "600");
svg.setAttribute("viewBox", "-150 -50 500 350");

// Set the background to black
svg.setAttribute("style", "background-color: black;");

document.getElementById("svg-container").appendChild(svg);

// Variable to keep track of selected element
let selectedElement = null;

// Fetch the JSON data from the file
fetch('output.json')
    .then(response => response.json())
    .then(jsonData => {
        // Process the JSON data
        jsonData.forEach(item => {
            const { type, properties, geometry } = item;

            if (type === "path") {
                renderPath(properties, geometry);
            } else if (type === "lines") {
                renderLines(properties, geometry);
            }
        });
    })
    .catch(error => console.error('Error loading JSON data:', error));

function renderPath(properties, geometry) {
    const pathElement = document.createElementNS(svgNS, "path");

    const d = geometry.map(segment => {
        const [command, ...coords] = segment;
        return `${command} ${coords.join(' ')}`;
    }).join(' ');

    pathElement.setAttribute("d", d);

    // Determine if the path is a circle (hole)
    let isCircle = properties.layer === "INTERIOR_PROFILES";

    // Set fill and pointer-events for circles
    if (isCircle) {
        pathElement.setAttribute("fill", "transparent");
        pathElement.setAttribute("pointer-events", "fill"); // Capture events over the fill area
    } else {
        pathElement.setAttribute("fill", properties.fill || "none");
        pathElement.setAttribute("pointer-events", "visiblePainted"); // Default behavior
    }

    // Set stroke color
    let strokeColor = properties.color || "#000";
    if (isCircle) {
        strokeColor = "#00ff00"; // Green color for circles
    }
    pathElement.setAttribute("stroke", strokeColor);

    // Set stroke width
    const originalStrokeWidth = properties["stroke-width"] || 1;
    pathElement.setAttribute("stroke-width", originalStrokeWidth);
    pathElement.originalStrokeColor = strokeColor;
    pathElement.setAttribute('data-original-stroke-width', originalStrokeWidth);

    // Add event listeners for hover and selection
    pathElement.addEventListener('mouseover', function() {
        if (this !== selectedElement) {
            this.setAttribute('stroke-width', parseFloat(originalStrokeWidth) + 1);
            this.setAttribute('stroke', '#ff0000'); // Red color on hover
        }
    });

    pathElement.addEventListener('mouseout', function() {
        if (this !== selectedElement) {
            this.setAttribute('stroke-width', originalStrokeWidth);
            this.setAttribute('stroke', strokeColor);
        }
    });

    pathElement.addEventListener('click', function(event) {
        event.stopPropagation(); // Prevent click event from bubbling up
        // Deselect previously selected element
        if (selectedElement && selectedElement !== this) {
            const prevStrokeWidth = selectedElement.getAttribute('data-original-stroke-width');
            selectedElement.setAttribute('stroke-width', prevStrokeWidth);
            selectedElement.setAttribute('stroke', selectedElement.originalStrokeColor);
        }
        // Select the clicked element
        selectedElement = this;
        this.setAttribute('stroke-width', parseFloat(originalStrokeWidth) + 2);
        this.setAttribute('stroke', '#00ffff'); // Cyan color when selected
    });

    svg.appendChild(pathElement);
}

function renderLines(properties, geometry) {
    geometry.forEach(coords => {
        const [x1, y1, x2, y2] = coords;

        const lineElement = document.createElementNS(svgNS, "line");
        lineElement.setAttribute("x1", x1);
        lineElement.setAttribute("y1", y1);
        lineElement.setAttribute("x2", x2);
        lineElement.setAttribute("y2", y2);

        // Override color for bend lines
        let strokeColor = properties.color || "#000";
        if (properties.layer === "BEND") {
            strokeColor = "#ffff00"; // Yellow color for bend lines
        }
        lineElement.setAttribute("stroke", strokeColor);

        const originalStrokeWidth = properties["stroke-width"] || 1;
        lineElement.setAttribute("stroke-width", originalStrokeWidth);
        lineElement.originalStrokeColor = strokeColor;
        lineElement.setAttribute('data-original-stroke-width', originalStrokeWidth);

        // Add event listeners for hover and selection
        lineElement.addEventListener('mouseover', function() {
            if (this !== selectedElement) {
                this.setAttribute('stroke-width', parseFloat(originalStrokeWidth) + 1);
                this.setAttribute('stroke', '#ff0000'); // Red color on hover
            }
        });

        lineElement.addEventListener('mouseout', function() {
            if (this !== selectedElement) {
                this.setAttribute('stroke-width', originalStrokeWidth);
                this.setAttribute('stroke', strokeColor);
            }
        });

        lineElement.addEventListener('click', function(event) {
            event.stopPropagation(); // Prevent click event from bubbling up
            // Deselect previously selected element
            if (selectedElement && selectedElement !== this) {
                const prevStrokeWidth = selectedElement.getAttribute('data-original-stroke-width');
                selectedElement.setAttribute('stroke-width', prevStrokeWidth);
                selectedElement.setAttribute('stroke', selectedElement.originalStrokeColor);
            }
            // Select the clicked element
            selectedElement = this;
            this.setAttribute('stroke-width', parseFloat(originalStrokeWidth) + 2);
            this.setAttribute('stroke', '#00ffff'); // Cyan color when selected
        });

        svg.appendChild(lineElement);
    });
}

// Deselect element when clicking on the background
svg.addEventListener('click', function() {
    if (selectedElement) {
        const originalStrokeWidth = selectedElement.getAttribute('data-original-stroke-width');
        selectedElement.setAttribute('stroke-width', originalStrokeWidth);
        selectedElement.setAttribute('stroke', selectedElement.originalStrokeColor);
        selectedElement = null;
    }
});
