# Use the official ContinuumIO miniconda3 image as the base image
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Copy the environment.yml file to the container
COPY environment.yml .

# Create the conda environment
RUN conda env create -f environment.yml

# Activate the environment and install pip dependencies
SHELL ["conda", "run", "-n", "myenv", "/bin/bash", "-c"]

# Copy the requirements.txt file to the container
COPY requirements.txt .

# Install pip dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . .

# Expose the port that the Flask app runs on
EXPOSE 5000

# Command to run the Flask app
CMD ["conda", "run", "--no-capture-output", "-n", "myenv", "gunicorn", "-b", "0.0.0.0:5000", "server:app"]