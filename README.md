TODO:
have to clean imports in server.py
f the file is already an STL file, it’s directly returned without hole extraction. Have to change it.
Need to check for non circular holes.
Need to check depth calculations. 
Need to write code for welding line identification.
Need option to select step file, run preprocessing code and displaying options to select hole and line catagory from browser  instead of hardcoding.
Need to auto position camera based on scaling.
scaling factor variable used to map holes and rendering should be global setting.
Files are working with absolute addressing only.


Suggested Next Steps:

    Integrate Slider Functionality:
        Make sure the hole size slider sends values to the backend API and dynamically updates the 3D model in real time.

    Unify Hole Recognition Logic:
        Consider combining the preprocessing logic from preprocess.py with the API calls in server.py to avoid redundancy and make the system more robust.

    Improve Error Handling:
        Add more detailed error handling on both the frontend and backend to improve user experience and feedback during processing failures.

    Add Loading Indicators:
        On the frontend, add visual cues like spinners or progress bars while files are uploading or being processed.