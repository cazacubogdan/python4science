import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

# Define the vertices of the tetrahedron
vertices = np.array([[0, 0, 0], [1, 0, 0], [0.5, np.sqrt(3)/2, 0], [0.5, np.sqrt(3)/6, np.sqrt(2/3)]])

# Define the faces of the tetrahedron
faces = np.array([[0, 1, 2], [0, 1, 3], [1, 2, 3], [0, 2, 3]])

# Create a 3D axis object
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create a Poly3DCollection object and add it to the axis
tetrahedron = Poly3DCollection(vertices[faces])
ax.add_collection3d(tetrahedron)

# Set the axis limits
ax.set_xlim([0, 1])
ax.set_ylim([0, np.sqrt(3)/2])
ax.set_zlim([0, np.sqrt(2/3)])

# Set the axis labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

# Display the plot
plt.show()
