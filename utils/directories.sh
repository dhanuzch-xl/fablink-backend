#!/bin/bash

# Base project directory
mkdir -p sheet_metal_unfolding_project

# Create /src directory and Python files
mkdir -p sheet_metal_unfolding_project/src
touch sheet_metal_unfolding_project/src/__init__.py
touch sheet_metal_unfolding_project/src/main.py
touch sheet_metal_unfolding_project/src/file_loader.py
touch sheet_metal_unfolding_project/src/sheet_tree.py
touch sheet_metal_unfolding_project/src/face_operations.py
touch sheet_metal_unfolding_project/src/bend_analysis.py
touch sheet_metal_unfolding_project/src/export_handler.py
touch sheet_metal_unfolding_project/src/utils.py

# Create /tests directory and test files
mkdir -p sheet_metal_unfolding_project/tests
touch sheet_metal_unfolding_project/tests/test_file_loader.py
touch sheet_metal_unfolding_project/tests/test_sheet_tree.py
touch sheet_metal_unfolding_project/tests/test_face_operations.py
touch sheet_metal_unfolding_project/tests/test_bend_analysis.py
touch sheet_metal_unfolding_project/tests/test_export_handler.py

# Create /data directory and example STEP files
mkdir -p sheet_metal_unfolding_project/data
touch sheet_metal_unfolding_project/data/example_1.step
touch sheet_metal_unfolding_project/data/example_2.step

# Create /scripts directory and script files
mkdir -p sheet_metal_unfolding_project/scripts
touch sheet_metal_unfolding_project/scripts/run_tests.sh
touch sheet_metal_unfolding_project/scripts/run_unfold_example.py

# Create root-level project files
touch sheet_metal_unfolding_project/README.md
touch sheet_metal_unfolding_project/requirements.txt

# Give executable permission to run_tests.sh script
chmod +x sheet_metal_unfolding_project/scripts/run_tests.sh

echo "Project directory structure created successfully!"
