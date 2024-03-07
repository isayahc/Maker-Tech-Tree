import trimesh
import shutil
import base64
import os

def save_file(input_file, output_file):
    """
    Copy a file from input location to output location.

    Args:
    input_file (str): Path to the input file.
    output_file (str): Path to the output file.

    Returns:
    bool: True if the file is successfully saved, False otherwise.
    """
    try:
        shutil.copy(input_file, output_file)
        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
    

def convert_obj_to_stl(input_file: str, output_file: str):
    # Load the OBJ file
    mesh = trimesh.load(input_file)

    # Export as STL
    mesh.export(output_file)
    
def change_file_extension(file_path: str, new_extension: str) -> str:
    """
    Change the extension of a file path.

    Args:
        file_path (str): The original file path.
        new_extension (str): The new file extension (without the dot).

    Returns:
        str: The modified file path with the new extension.
    """
    base_path, _ = os.path.splitext(file_path)
    new_file_path = base_path + '.' + new_extension
    return new_file_path

        
def file_to_base64(file_location: str) -> str:
    """
    This function is to convert files into base64
    ## Input
    file_location (str) : the location of the file on the machine
    
    ## Output
    the base64 encoding of the file
    """
    with open(file_location, "rb") as file:
        file_content = file.read()
        base64_encoded = base64.b64encode(file_content)
        return base64_encoded.decode("utf-8")
    
def base64_to_file(base64_string: str, output_file_location: str) -> None:
    """
    Decodes a base64-encoded string and writes the resulting binary data to a file.

    Args:
        base64_string (str): The base64-encoded string to decode.
        output_file_location (str): The file path where the decoded binary data will be written.

    Returns:
        None
    """
    binary_data = base64.b64decode(base64_string)
    with open(output_file_location, "wb") as output_file:
        output_file.write(binary_data)

def copy_file_to_location(file_path: str, destination_path: str) -> None:
    """
    Copy a file to a new location with the same name.

    Args:
        file_path: The path of the file to be copied.
        destination_path: The path of the destination directory.
    """
    shutil.copy(file_path, destination_path)
    
def remove_files(file_paths):
    """Remove files given a list of file paths."""
    for file_path in file_paths:
        try:
            os.remove(file_path)
            print(f"File '{file_path}' removed successfully.")
        except OSError as e:
            print(f"Error removing file '{file_path}': {e}")