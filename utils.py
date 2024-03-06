import shutil
import trimesh
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