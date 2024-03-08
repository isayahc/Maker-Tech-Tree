from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt
from typing import List, Tuple


def generate_mesh_images(file_path: str, viewing_angles: List[Tuple[int, int]], output_prefix: str = 'mesh_') -> List[str]:
    """
    Generate images of an STL file from different viewing angles and return their file paths.

    Args:
        file_path (str): Path to the STL file.
        viewing_angles (List[Tuple[int, int]]): List of tuples containing the elevation and azimuth angles for viewing.
        output_prefix (str, optional): Prefix for the output image filenames. Defaults to 'mesh_'.

    Returns:
        List[str]: List of file paths of the generated images.
    """
    # Load the STL file
    your_mesh = mesh.Mesh.from_file(file_path)

    # List to store the file paths of the generated images
    image_paths = []

    # Iterate over each viewing angle and generate an image
    for i, (elev, azim) in enumerate(viewing_angles, start=1):
        # Create a new plot with a larger figure size
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')

        # Add the STL file to the plot
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(your_mesh.vectors))

        # Calculate the limits of the mesh
        max_dim = max(your_mesh.points.flatten())
        min_dim = min(your_mesh.points.flatten())

        # Set the limits of the plot
        ax.set_xlim([min_dim, max_dim])
        ax.set_ylim([min_dim, max_dim])
        ax.set_zlim([min_dim, max_dim])

        # Set the viewing angle
        ax.view_init(elev=elev, azim=azim)

        # Save the plot as an image
        image_path = f'{output_prefix}{i}.png'
        plt.savefig(image_path)
        image_paths.append(image_path)

        # Close the plot to avoid memory leaks
        plt.close()

    return image_paths


if __name__ == "__main__":
    # Example usage:
    # file_path = 'sample_data.stl'
    viewing_angles = [(30, 45), (60, 90), (45, 135)]
    # generate_mesh_images(file_path, viewing_angles)
