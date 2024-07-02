# File Manager with Flask
This project is a simple web application developed using Flask to manage files. It allows users to upload files to the server, download existing files, and view the list of available files.

## Features
- **File Upload:** Users can upload files to the server, which are stored in the download folder.
- **File Download:** Files stored in the file folder can be downloaded by users.
- **Web Interface:** Uses Flask to generate a web interface where users can interact with the files.
- **User administration:** Uses a configurable users file for only authorized sessions

## Prerequisites
- Python 3.x
- Flask (`pip install Flask`)

## Project Structure
├── app.py
├── classes.py
├── constants.py
├── download # folder for files to be downloaded
├── logs     # folder for system logs
├── upload   # folder for files to be uploaded
├── users.example.json
├── users.json # users allowed in the system
├── utils.py

## Configuration
1. **Directory Setup:**
   - The application uses the following directories to store files:
     - `download/`: To store files available for download.
     - `upload/`: To store files uploaded by users.
     - `logs/`: Optionally, to store application logs.

2. **Installing Dependencies:**
   - Install Flask and other dependencies if not already installed:
     ```
     pip install -r requirements.txt
     ```

## Usage
1. **Running the Application:**
   - From the command line, run the `app.py` file to start the Flask server:
     ```
     python app.py <port> <debug_mode>
     ```
     - `<port>`: Port on which the application will run (default is 5000).
     - `<debug_mode>`: Debug mode (0 for off, 1 for on).

2. **Interacting with the Application:**
   - Open a web browser and go to `http://localhost:<port>` to view the user interface.
   - Upload files using the provided form.
   - Download files by clicking on the available download links.

## Credits
Developed by Nicolas Agustín Pieroni