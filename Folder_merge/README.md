# Folder Merge Application

## folder_merge_app_new.py

A simple pyqt6 application to merge folders,convert files to MP3,displaying progress and handling task in a separate thread.

## merge_all_books.py

A utility module to merge folders based on unique prefixes and convert files to MP3.

## Features

- Select a source folder for merging.
- Merge folders based on unique prefixes.
- Convert merged files to MP3 format.
- Display progress of the merging process.
- Handle tasks in a separate thread to keep the UI responsive.
- Show completion message upon successful merge and conversion.

## Requirements

- Python 3.7+
- PyQT6
- ffmpeg

## Installation

1.  Clone the repository.
    git clone https://github.com/Bridgeconn/Folder-Merge.git
2.  Navigate to the project directory.
    cd Folder-Merge
3.  Create and activate virtual environment.

    - On Windows:
      python -m venv venv
      venv\Scripts\activate

    - On macOS/Linux:
      python3 -m venv venv
      source venv/bin/activate

4.  Install the required python dependencies:
    pip install -r requirements.txt

5.  Install ffmpeg:
    For windows,download and install ffmpeg from FFmpeg website.

    For Ubuntu/Linux:
    sudo apt install ffmpeg.

6.  Install ffmpeg-python:
    pip install ffmpeg-python

## Run the application:

    python folder_merge_app_new.py

## Creating an Executable file:

    To create a standalone executable file from the folder_merge_app_new.py script, follow these steps:

     1. Install PyInstaller (if not already installed):
          pip install pyinstaller.
     2. Generate the Executable:
          Run the following command in the terminal from the project directory:
            pyinstaller --onefile folder_merge_app_new.py
     3. Locate the Executable:
          After running the command, the executable file will be located in the 'dist' directory with in the project folder.
            On Windows, it will be folder_merge_app_new.exe.
            On macOS/Linux, it will be folder_merge_app_new.
     4. Running the Executable:
          Users can run it without needing Python or any dependencies installed on their system.
