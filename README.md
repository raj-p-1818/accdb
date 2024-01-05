# This project converts Microsoft Access databases to Parquet files within a Docker container

- Microsoft Access Database Engine 2016 Redistributable
   you must have the Microsoft Access Database.exe file and install the .exe in you system and should be included in the Docker file
link tect : https://www.microsoft.com/en-us/download/details.aspx?id=54920

## Explanation of Dockerfile

- FROM mcr.microsoft.com/windows:ltsc2019 --------> Uses a Windows base image.
  
- RUN mkdir C:\app --------> This step creates a directory named "app" within the container to house the application's files.

- WORKDIR C:\\app --------> Sets the working directory to C:\\app.

- COPY . .    --------> Copies the current directory contents into the container's C:\\app directory.
  
- COPY accessdatabaseengine_X64.exe C:\\app\\ --------> This line specifically copies the "accessdatabaseengine_X64.exe" file into the "app" directory.
  
- RUN C:\app\accessdatabaseengine_X64.exe --------> Installs the Access Database Engine.
  
- ARG INPUT_BUCKET_PATH --------> Declares a build-time argument named "INPUT_BUCKET_PATH" that can be set during the image building process to specify input data storage.
  
- ARG OUTPUT_BUCKET_PATH --------> Similarly, this defines a build-time argument named "OUTPUT_BUCKET_PATH" for configuring output data storage.
  
- SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"] --------> Sets the default shell to PowerShell for subsequent commands.
  
- RUN ... --------> Installs Python and required packages.
  
- CMD ["python", "main.py"] --------> Specifies the default command to be executed when the container starts, which is to initiate a Python script named "main.py".

## Explanation of Python Script (main.py)

- from flask import Flask, jsonify --------> Imports the Flask framework for creating web applications and the jsonify function for returning JSON responses.
- import pyodbc as pyo --------> Imports the pyodbc library for connecting to databases.
- import pandas as pd --------> Imports the pandas library for data manipulation and analysis.
- import pyarrow.parquet as pq --------> Imports the pyarrow library for working with Parquet files, a columnar file format.
- import os --------> Imports the os library for interacting with the operating system, such as accessing environment variables.
  
Function Definition:

- def save_to_parquet(df, file_path): -------->  Defines a function to save a DataFrame to a Parquet file, handling potential duplicate column names.
- Initial Print Statement:

- print(pyo.drivers()) --------> Prints a list of available ODBC drivers, which can be helpful for troubleshooting connection issues.
  
Flask Application Setup:

- app = Flask(__name__) --------> Creates a Flask application instance.
  
Route Definition:

- @app.route('/', methods=['GET']) --------> Defines a route that responds to GET requests at the root URL (/) and calls the process_accdb function.
  
- Function for Processing ACCDB Database:

Function for Processing ACCDB Database:

-def process_accdb():

- Retrieves input and output paths from environment variables.
- Extracts the database name from the input path.
- Constructs a connection string for the Access database.
- Tries to connect to the database, raising an error if not found.
- Creates a cursor object for executing SQL statements.
- Sets the output directory for Parquet files.
- Iterates through tables in the database:
            - Retrieves table names.
            - Excludes system tables starting with "msys".
            - Selects all data from each table (except "Orders By Date").
            - Reads the data into a DataFrame using pandas.
- Handles duplicate column names.
- Saves the DataFrame to a Parquet file.
- Concatenates all DataFrames into a single DataFrame.
- Saves the combined DataFrame to a Parquet file.
- Returns a JSON response indicating success or an error message if appropriate.
  
Main Execution:
        - if __name__ == '__main__': --------> Runs the Flask application if the script is executed directly.

## Commands to Run

## 1. docker build -t (tag_name) .

- Purpose -------->  Builds a Docker image from the current directory's Dockerfile.
- Breakdown:
  docker build --------> Initiates the image building process.
  -t dev --------> Tags the image with the name dev.
  .(dot) --------> Specifies the context directory (current directory) containing the Dockerfile and project files.

## 2. docker images

- Purpose --------> Lists all Docker images available on your system.
- Breakdown:
  docker images--------> Displays a table of images, including their IDs, names, tags, sizes, and creation dates.

## 3. docker tag

- Purpose --------> Retags an existing image with a new name and registry location.
- Syntax --------> "docker tag SOURCE-IMAGE LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/IMAGE:TAG"
- Command --------> "docker tag 9dee2f447d4b us-central1-docker.pkg.dev/sbox-ujjal-ci-cd-capabilities/local-to-artifactrepo/9dee2f447d4b:dev"
- Breakdown:
           - docker tag: Assigns a new tag to an image.
           - 9dee2f447d4b: Original image ID.
           - us-central1-docker.pkg.dev/sbox-ujjal-ci-cd-capabilities/local-to-artifactrepo/9dee2f447d4b:dev: New name and registry path for the image.

## Before pushing the image to the artifact registry

- Authenticating to a repository -------->
You must authenticate to repositories whenever you use Docker or another third-party client with a Docker repository.
one way is that by "Using a credential helper"
- command --------> gcloud auth configure-docker
- If a host you want to use is not in the list, run the credential helper again to add the host. For example, the following command adds us-east1-docker.pkg.dev.
- command --------> gcloud auth configure-docker us-east1-docker.pkg.dev
  
## 4. docker push

- Purpose --------> Pushes a tagged image to a registry.
- Syntax --------> docker push LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/IMAGE:TAG
- Command --------> "docker push us-central1-docker.pkg.dev/sbox-ujjal-ci-cd-capabilities local-to-artifactrepo/9dee2f447d4b:dev"
- Breakdown:
            - docker push: Uploads an image to a registry.
            - us-central1-docker.pkg.dev/sbox-ujjal-ci-cd-capabilities/local-to-artifactrepo
            - 9dee2f447d4b:dev: Full name and tag of the image to push.

## 5. docker run

- Purpose --------> Runs a container from an image and sets environment variables.
- Command --------> "docker run -e INPUT_BUCKET_PATH=gs://accdb1/input_folder/GardenCompany01.accdb -e OUTPUT_BUCKET_PATH=accdb1/output_folder 9dee2f447d4b"
- Breakdown:
docker run --------> Starts a container from an image.
            - -e INPUT_BUCKET_PATH=gs://accdb1/input_folder/GardenCompany01.accdb:  Sets the INPUT_BUCKET_PATH environment variable to the specified path.
            - -e OUTPUT_BUCKET_PATH=accdb1/output_folder: Sets the OUTPUT_BUCKET_PATH environment variable.
            - 9dee2f447d4b: Image ID or name to run.

## IMPORTANT POINTS

- Make sure that you are authenticated to the repository.
- Determine the name of the image. The format of a full image name.
- Tag the local image with the repository name.
- Push the tagged image with the command.
