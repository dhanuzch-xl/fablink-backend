import os
import re

def collect_index_and_documentation(file_path):
    index = []
    documentation = []
    descriptions = {}

    with open(file_path, 'r') as file:
        doc = file.read()
        documentation.append(doc)
        
        # Collect file names prefixed by ## and their descriptions
        lines = doc.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('## ') and not line.startswith('###'):
                header = line[3:].strip()  # Remove the '## ' prefix and any leading/trailing spaces
                index.append(header)
                # Assume the description is the next non-empty line
                description = ""
                for j in range(i + 1, len(lines)):
                    if lines[j].strip():
                        description = lines[j].strip()
                        break
                descriptions[header] = description

    return index, documentation, descriptions

def generate_index(index, descriptions):
    def create_link(text):
        # Convert to lowercase, replace spaces with hyphens, and remove special characters
        link = re.sub(r'[^a-z0-9_\-]', '', text.lower().replace(' ', '-'))
        # Remove hyphen if it appears at the start
        if link.startswith('-'):
            link = link[1:]
        return link

    index.sort()  # Sort the index alphabetically
    index_content = "# Index\n\n"
    index_content += "| No. | File | Description |\n"
    index_content += "| --- | ---- | ----------- |\n"
    for i, item in enumerate(index, 1):  # Start enumeration at 1
        link = create_link(item)
        description = descriptions.get(item, "")
        index_content += f"| {i} | [{item}](#{link}) | {description} |\n"
    return index_content

def main():
    file_path = "/home/dhanuzch/workspace/xlogic/dfm-gui/documentation/documentation.md"
    index, documentation, descriptions = collect_index_and_documentation(file_path)
    
    index_content = generate_index(index, descriptions)
    
    with open("documentation/indexed_documentation.md", "w") as doc_file:
        doc_file.write(index_content + "\n\n")
        for doc in documentation:
            doc_file.write(doc + "\n\n")

if __name__ == "__main__":
    main()