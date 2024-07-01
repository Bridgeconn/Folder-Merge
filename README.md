# Folder-Merge
This script is structured to organize and merge directories with common prefixes, while handling duplicate chapters.
## Features

- Scans the base directory to find unique three-character prefixes of subdirectories.
- Finds directories with given prefixes.
- Checks for duplicate chapters across directories with the same prefix.
- Copies files from source directories to a target destination.
- Counts and reports the number of chapters and files.
## Requirements

- Python 3.x
## Setup

1. Clone this repo, https://github.com/Bridgeconn/Folder-Merge.git
2. Ensure you have Python  installed on your system.
3. Place the script in a directory of your choice.
4. Update the base_dir to point to the directory containing the language folders 
    eg.  'base_dir = '/home/Desktop/Export''
5. Run the script using the command:
    python script_name.py 
    eg.python merge_folder.py

6. Output will be saved in the output directory.
