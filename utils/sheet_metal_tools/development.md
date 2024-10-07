/sheet_metal_unfolding_project
│
├── /src                        # Main source code folder
│   ├── __init__.py              # Package initialization
│   ├── main.py                  # Main application entry point
│   ├── file_loader.py           # STEP file loading and geometry extraction
│   ├── sheet_tree.py            # Tree structure and node management
│   ├── face_operations.py       # Face extraction, transformation logic (rotation/translation)
│   ├── bend_analysis.py         # Bend detection and unfolding logic
│   ├── export_handler.py        # Unfolded face exporting (STEP/DXF)
│   └── utils.py                 # Utility functions (e.g., logging, helper functions)
│
├── /tests                      # Folder for unit tests
│   ├── test_file_loader.py      # Tests for STEP file loading and face extraction
│   ├── test_sheet_tree.py       # Tests for tree structure and node creation
│   ├── test_face_operations.py  # Tests for face transformations (rotation/translation)
│   ├── test_bend_analysis.py    # Tests for bend detection and unfolding logic
│   ├── test_export_handler.py   # Tests for exporting unfolded parts
│
├── /data                       # Sample STEP/DXF files for testing
│   ├── example_1.step           # Example STEP file for testing unfolding
│   ├── example_2.step           # Another test file for complex shapes
│
├── /scripts                    # Folder for helper scripts
│   ├── run_tests.sh             # Script to run all tests
│   ├── run_unfold_example.py    # Script to run a sample unfolding operation
│
├── README.md                   # Project documentation
├── requirements.txt            # Dependencies (PythonOCC, pytest, etc.)
└── .gitignore                  # Git ignore file for version control
