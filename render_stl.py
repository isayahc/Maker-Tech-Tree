from stl import mesh
from mpl_toolkits import mplot3d
from matplotlib import pyplot as plt

# Load the STL file
your_mesh = mesh.Mesh.from_file('sample_data.stl')

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

# Save the plot as an image
plt.savefig('mesh.png')

# Show the plot (optional)
# plt.show()
