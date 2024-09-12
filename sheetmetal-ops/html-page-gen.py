import pandas as pd
import os

# Path to the CSV file
csv_file_path = 'xlogic-sheet-ops/materials.csv'  # Update this with the actual path to your CSV file
output_dir = 'xlogic-sheet-ops/'  # Directory to store HTML files

# Ensure the output directory exists
os.makedirs(output_dir, exist_ok=True)

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

# HTML template for each material's detail page
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{Material} Details</title>
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            background-color: #f4f4f4;
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }}
        .content {{
            background: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            width: 80%;
            max-width: 600px;
        }}
        h1 {{
            color: #333;
        }}
        ul {{
            list-style: none;
            padding: 0;
        }}
        li {{
            padding: 5px 0;
            border-bottom: 1px solid #eee;
        }}
        a {{
            color: #06c;
            text-decoration: none;
        }}
        a:hover {{
            text-decoration: underline;
        }}
    </style>
</head>
<body>
    <div class="content">
        <h1>{Material}</h1>
        <p><strong>Available Thicknesses:</strong> {Available_Thicknesses}</p>
        <p><strong>Available Services:</strong></p>
        <ul>
            {services_list}
        </ul>
        <p><strong>Description:</strong> {Description}</p>
        <p><a href="index.html">Back to Materials List</a></p>
    </div>
</body>
</html>
"""

# List of all services for filtering
services = [
    'Laser Cutting', 'CNC Routing', 'Waterjet Cutting', 'Bending', 'Anodizing', 'Deburring',
    'Countersinking', 'Hardware Insertion', 'Plating', 'Powder Coating',
    'Tapping', 'Tumbling', 'Dimple Forming'
]

# Generate HTML files for each material
for index, row in df.iterrows():
    # Generate the services list in HTML format
    services_html = ''.join(
        f"<li>{service}: {'Yes' if row[service] == 'Yes' else 'No'}</li>" for service in services if service in row
    )

    # Format the HTML content
    html_content = html_template.format(
        Material=row['Material'],
        Available_Thicknesses=row['Available Thicknesses'],
        services_list=services_html,
        Description=row['Description']
    )

    # Define the file path for this material's HTML page
    filename = f"{row['Material'].replace(' ', '-').lower()}.html"
    file_path = os.path.join(output_dir, filename)

    # Write the HTML content to the file
    with open(file_path, 'w') as file:
        file.write(html_content)

    print(f"Generated HTML page for {row['Material']} at {file_path}")
