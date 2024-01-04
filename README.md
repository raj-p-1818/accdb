# This project converts Microsoft Access databases to Parquet files within a Docker container.

## Prerequisites

- Docker installed on your system

## Explanation of Dockerfile

- FROM mcr.microsoft.com/windows:ltsc2019: Uses a Windows base image.
- RUN mkdir C:\app: Creates an application directory.
- WORKDIR C:\\app: Sets the working directory to C:\\app.
- COPY . .: Copies the current directory contents into the container's C:\\app directory.
- COPY accessdatabaseengine_X64.exe C:\\app\\: Copies the Access Database Engine installer into the container.
- RUN C:\app\accessdatabaseengine_X64.exe: Installs the Access Database Engine.
- ARG INPUT_BUCKET_PATH and ARG OUTPUT_BUCKET_PATH: Defines build-time arguments for input and output paths.
- SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]: Sets the default shell to PowerShell for subsequent commands.
- RUN ...: Installs Python and required packages.
- CMD ["python", "main.py"]: Sets the default command to run the Python script.

## Explanation of Python Script (main.py)

- Imports necessary libraries.
- Defines a function save_to_parquet to save DataFrames to Parquet files.
- Retrieves input and output paths from environment variables.
- Connects to the Access database.
- Iterates through tables, reads data, and saves as Parquet files.
- Combines all Parquet files into a single file.

# Commands to Run

## 1. docker build -t dev .

- Purpose: Builds a Docker image from the current directory's Dockerfile.
- Breakdown:
docker build: Initiates the image building process.
-t dev: Tags the image with the name dev.
.: Specifies the context directory (current directory) containing the Dockerfile and project files.

## 2. docker images

- Purpose: Lists all Docker images available on your system.
- Breakdown:
docker images: Displays a table of images, including their IDs, names, tags, sizes, and creation dates.

## 3. docker tag

- Purpose: Retags an existing image with a new name and registry location.
- Syntax : "docker tag SOURCE-IMAGE LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/IMAGE:TAG"
- Command : "docker tag 9dee2f447d4b us-central1-docker.pkg.dev/sbox-ujjal-ci-cd-capabilities/local-to-artifactrepo/9dee2f447d4b:dev"
- Breakdown:
docker tag: Assigns a new tag to an image.
9dee2f447d4b: Original image ID.
us-central1-docker.pkg.dev/sbox-ujjal-ci-cd-capabilities/local-to-artifactrepo/9dee2f447d4b:dev: New name and registry path for the image.

## 4. docker push

- Purpose: Pushes a tagged image to a registry.
- Syntax : docker push LOCATION-docker.pkg.dev/PROJECT-ID/REPOSITORY/IMAGE:TAG
- Command : "docker push us-central1-docker.pkg.dev/sbox-ujjal-ci-cd-capabilities local-to-artifactrepo/9dee2f447d4b:dev"
- Breakdown:
docker push: Uploads an image to a registry.
us-central1-docker.pkg.dev/sbox-ujjal-ci-cd-capabilities/local-to-artifactrepo/9dee2f447d4b:dev: Full name and tag of the image to push.

## 5. docker run

- Purpose: Runs a container from an image and sets environment variables.
- Command : "docker run -e INPUT_BUCKET_PATH=gs://accdb1/input_folder/GardenCompany01.accdb -e OUTPUT_BUCKET_PATH=accdb1/output_folder 9dee2f447d4b"
- Breakdown:
docker run: Starts a container from an image.
-e INPUT_BUCKET_PATH=gs://accdb1/input_folder/GardenCompany01.accdb: Sets the INPUT_BUCKET_PATH environment variable to the specified path.
-e OUTPUT_BUCKET_PATH=accdb1/output_folder: Sets the OUTPUT_BUCKET_PATH environment variable.
9dee2f447d4b: Image ID or name to run.

## Before pushing the image to the artifact registry

- Authenticating to a repository :
You must authenticate to repositories whenever you use Docker or another third-party client with a Docker repository.
one way is that by "Using a credential helper"
- command : gcloud auth configure-docker
- If a host you want to use is not in the list, run the credential helper again to add the host. For example, the following command adds us-east1-docker.pkg.dev.
- command : gcloud auth configure-docker us-east1-docker.pkg.dev

# IMPORTANT POINTS

- Make sure that you are authenticated to the repository.
- Determine the name of the image. The format of a full image name.
- Tag the local image with the repository name.
- Push the tagged image with the command.
