# Project: Interactive 3D STL Viewer with Hole Detection

## Overview
This project allows you to view a 3D metal plate with holes and interactively display information such as hole diameter and depth when hovering over them. The project consists of two parts:
1. **Python Preprocessing**: This preprocesses the STEP file to recognize holes and calculates their properties (e.g., diameter, depth).
2. **Web Visualization**: The 3D model is rendered in a web browser using Three.js, and hole information is displayed when the user hovers over the holes.

## Project Structure
- `models/`: Contains the STEP file `Plate_1.step`.
- `output/`: Stores the JSON file `hole_data.json` containing the preprocessed hole information.
- `renderer/`: Contains the custom renderer script (if needed).
- `app/`: Contains the web viewer files (`index.html`, `main.js`, and `style.css`).
- `scripts/`: Contains the Python preprocessing script `preprocess.py`.

## Requirements

### Python Environment
- `pythonocc-core`
- `json`

Install dependencies:
