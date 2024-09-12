import os
from openai import AzureOpenAI
import markdown

# Set up your OpenAI API credentials
client = AzureOpenAI(
    api_key="ca20e42c96814883b37449d073695709",  
    api_version="2024-02-01",
    azure_endpoint="https://xlogiccursor.openai.azure.com/"
)

deployment_name = 'xLogicCursorgpt-4o'  # Ensure this is the correct deployment name

def analyze_code(file_content):
    # Prepare the messages for the API call
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": f"Analyze the following Python code and provide a clear, concise description of its purpose and functionality:\n\n{file_content}"}
    ]
    
    # Make the API call
    response = client.chat.completions.create(
        model=deployment_name,
        messages=messages,
        max_tokens=4096,
        temperature=0.5
    )
    
    # Print the response to inspect its structure
    print(response.choices[0])
    return response.choices[0].message.content.strip()

def process_files_in_folder(folder_path):
    documentation = "# Project Documentation\n\n"
    documentation += "This documentation provides an overview of the functionality of each Python file in the folder.\n\n"

    for filename in os.listdir(folder_path):
        if filename.endswith(".py"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r') as file:
                file_content = file.read()
                print(3)
                doc = analyze_code(file_content)
                print(4)
                documentation += f"## {filename}\n\n"
                documentation += f"{doc}\n\n"

    return documentation

def write_markdown(output_path, documentation):
    # Write the documentation to a markdown file
    with open(output_path, 'w') as markdown_file:
        markdown_file.write(documentation)

def main():
    folder_path = "./pythonocc-demos/examples"
    output_path = "./documentation.md"
    print(1)
    # Process the folder and generate documentation
    documentation = process_files_in_folder(folder_path)
    print(2)

    # Write the generated documentation to the markdown file
    write_markdown(output_path, documentation)

    print(f"Documentation successfully generated in {output_path}")

if __name__ == "__main__":
    main()
