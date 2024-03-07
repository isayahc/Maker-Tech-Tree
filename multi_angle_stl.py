from stl import mesh
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

def load_stl(file_path):
    """Load the STL file."""
    return mesh.Mesh.from_file(file_path)

def generate_images(mesh, viewing_angles, figsize=(10, 10)):
    """Generate images from different viewing angles."""
    for i, (elev, azim) in enumerate(viewing_angles, start=1):
        fig = plt.figure(figsize=figsize)
        ax = fig.add_subplot(111, projection='3d')
        ax.add_collection3d(mplot3d.art3d.Poly3DCollection(mesh.vectors))
        max_dim = max(mesh.points.flatten())
        min_dim = min(mesh.points.flatten())
        ax.set_xlim([min_dim, max_dim])
        ax.set_ylim([min_dim, max_dim])
        ax.set_zlim([min_dim, max_dim])
        ax.view_init(elev=elev, azim=azim)
        plt.savefig(f'mesh_{i}.png')
        plt.close()

def main():
    # Load the STL file
    # stl_file_path = 'sample_data.stl'
    # your_mesh = load_stl(stl_file_path)

    # Define three different viewing angles
    viewing_angles = [(30, 45), (60, 90), (45, 135)]

    # Generate images from different viewing angles
    # generate_images(your_mesh, viewing_angles)

    # Optional: Show the last generated plot
    # plt.show()

if __name__ == "__main__":
    main()
