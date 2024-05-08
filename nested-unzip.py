"""
Script Name: nested-unzip.py
Author: Justin Lund
Last modified: 04/16/24
Date created: 11/05/23
Version: 2.1.1

Purpose:
Unzip zip files within nested folders.
Created specifically for restoring MS Defender Quarantine files obtained via an EDR system.

Parameters:
| Short | Long       | Function                                                                 |
| -f    | --folder   | Specify the target folder for zip extraction.                            |
| -p    | --password | Specify the password for zip files (optional - defaults to "infected").  |
| -r    | --remove   | Remove zip files after extraction (optional - defaults to keeping them). |
| -c    | --create   | Create a new 'Quarantine' folder with subfolders.                        |

# Usage Examples for nested-unzip.py on a folder named "Quarantine":

1. Unzip with password "infected" or no password:
    python3 nested-unzip.py -f "Quarantine"

2. Specify password:
    python3 nested-unzip.py -f "Quarantine" -p "superSecretPassw0rd"

3. Remove files after unzipping (will prompt for confirmation):
    python3 nested-unzip.py -f "Quarantine" -r

4. Specify password + remove zips:
   python3 nested-unzip.py -f "Quarantine" -p "superSecretPassw0rd" -r

5. Create 'Quarantine' folder with subfolders:
   python3 nested-unzip.py -c

6. Create 'Quarantine' folder with specified subfolders in 'Resources' and 'ResourceData':
   python3 nested-unzip.py -c 2E 57 61 97

"""

import zipfile
import argparse
from pathlib import Path
import os
import subprocess

def create_quarantine_folders(subfolder_names):
    base_path = Path('Quarantine')
    subfolders = ['Entries', 'Resources', 'ResourceData']

    base_path.mkdir(exist_ok=True)
    for folder in subfolders:
        (base_path / folder).mkdir(exist_ok=True)

        # Create additional subfolders in 'Resources' and 'ResourceData'
        if folder in ['Resources', 'ResourceData']:
            for name in subfolder_names:
                (base_path / folder / name).mkdir(exist_ok=True)

    print("Quarantine folder structure created.")

def unzip_using_native_tool(file_path, password, directory):
    try:
        # Redirecting output to DEVNULL to suppress the native command's output
        subprocess.run(['unzip', '-P', password, '-d', directory, file_path], 
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Failed to unzip {file_path}: {e}")
        return False

def unzip_recursive(directory, password, remove):
    directory_path = Path(directory).resolve()
    zipped_files = list(directory_path.rglob('*.zip'))
    extracted_files = []

    # Check OS and decide on unzip method
    os_type = os.uname().sysname
    use_native_unzip = os_type in ['Darwin', 'Linux']

    # Unzip process
    for file_path in zipped_files:
        print(f"Unzipping: {file_path}")
        if use_native_unzip:
            success = unzip_using_native_tool(str(file_path), password, str(file_path.parent))
            if success:
                extracted_files.append(file_path)
        else:
            try:
                with zipfile.ZipFile(file_path, 'r') as zip_ref:
                    zip_ref.extractall(path=file_path.parent, pwd=bytes(password, 'utf-8'))
                extracted_files.append(file_path)
            except zipfile.BadZipFile:
                print(f"Failed to unzip {file_path}: Bad zip file.")
            except RuntimeError as errorMsg:
                if "Bad password" in str(errorMsg):
                    print(f"Failed to unzip {file_path}: Incorrect password.")
                else:
                    print(f"Error: {errorMsg}")

    # Removal process
    if remove and extracted_files:
        response = input("Do you want to remove the zip files? [y/n]: ").lower()
        while response not in ['y', 'yes', 'n', 'no']:
            response = input("Invalid input. Please enter 'y' for yes or 'n' for no: ").lower()

        if response in ['y', 'yes']:
            for file_path in extracted_files:
                file_path.unlink()
                print(f"Removed: {file_path}")

def main():
    parser = argparse.ArgumentParser(description='Recursively unzip files in a directory.')
    parser.add_argument('-f', '--folder', type=str, help='Specify the target folder.', required=False)
    parser.add_argument('-p', '--password', type=str, default='infected', help='Specify the password for zip files. Tries password "infected" if not specified.')
    parser.add_argument('-r', '--remove', action='store_true', help='Remove zip files after extraction.')
    parser.add_argument('-c', '--create', nargs='*', help='Create a new Quarantine folder with subfolders. Additional arguments are subfolder names for Resources and ResourceData.')

    args = parser.parse_args()

    if args.create is not None:
        create_quarantine_folders(args.create)
    else:
        if args.folder:
            unzip_recursive(args.folder, args.password, args.remove)
        else:
            print("Error: Please specify a folder with -f or use -c to create a Quarantine folder.")

if __name__ == "__main__":
    main()
