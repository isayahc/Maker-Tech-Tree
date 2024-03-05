import os
import shutil
import subprocess
import sys
import tarfile
import urllib.request

def download_blender(url, destination):
    urllib.request.urlretrieve(url, destination)

def extract_archive(archive_file, destination):
    with tarfile.open(archive_file, 'r:xz') as tar:
        tar.extractall(destination)

def remove_file(file_path):
    os.remove(file_path)

def move_folder(source, destination):
    shutil.move(source, destination)

def create_symbolic_link(source, target):
    os.symlink(source, target)

def install_packages(packages):
    subprocess.run(['sudo', 'apt-get', 'update'])
    subprocess.run(['sudo', 'apt-get', 'install'] + packages + ['-y'])

def main():
    blender_url = 'https://download.blender.org/release/Blender4.0/blender-4.0.2-linux-x64.tar.xz'
    archive_file = 'blender-4.0.2-linux-x64.tar.xz'
    extracted_folder = 'blender-4.0.2-linux-x64'
    destination_folder = '/opt/blender-4.0.2'
    symbolic_link = '/usr/local/bin/blender'
    packages_to_install = ['libxxf86vm1', 'libgl1-mesa-glx', 'libegl-mesa0', 'libegl1']

    # Download Blender
    print("Downloading Blender...")
    download_blender(blender_url, archive_file)

    # Extract the downloaded archive
    print("Extracting Blender archive...")
    extract_archive(archive_file, '.')

    # Remove the downloaded archive
    print("Removing downloaded archive...")
    remove_file(archive_file)

    # Move the extracted folder to the desired location
    print("Moving Blender folder...")
    move_folder(extracted_folder, destination_folder)

    # Create a symbolic link to the Blender executable
    print("Creating symbolic link to Blender executable...")
    create_symbolic_link(os.path.join(destination_folder, 'blender'), symbolic_link)

    # Install required packages
    print("Installing required packages...")
    install_packages(packages_to_install)

    print("Installation complete.")

if __name__ == "__main__":
    main()
