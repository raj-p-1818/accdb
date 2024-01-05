FROM mcr.microsoft.com/windows:ltsc2019
# Create a directory for the application
RUN mkdir C:\app
# Set the working directory to C:
WORKDIR C:\\app
# Copy the current directory contents into the container at C:\app
COPY . .
COPY accessdatabaseengine_X64.exe C:\\app\\
RUN C:\app\accessdatabaseengine_X64.exe
ARG INPUT_BUCKET_PATH
ARG OUTPUT_BUCKET_PATH

SHELL ["powershell", "-Command", "$ErrorActionPreference = 'Stop'; $ProgressPreference = 'SilentlyContinue';"]
# Install Python
RUN Invoke-WebRequest -Uri "https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe" -OutFile "python-installer.exe"; \
    Start-Process python-installer.exe -ArgumentList '/quiet InstallAllUsers=1 PrependPath=1' -Wait; \
    Remove-Item python-installer.exe
# Test Python installation
RUN python --version
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
# Expose the port on which the Flask application will run
EXPOSE 5000
# Run the application
CMD ["python", "main.py"]