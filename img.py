import matplotlib.pyplot as plt
import numpy as np

def generate_random_points(n_points, n_dimensions):
    return np.random.rand(n_points, n_dimensions)

n_points = 1000  
n_dimensions = 3 

points = generate_random_points(n_points, n_dimensions)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(points[:, 0], points[:, 1], points[:, 2], c='b', marker='o')

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')

ax.set_title('Pontos Aleatórios no Hipercubo [0, 1]^3')

plt.savefig("hipercubo_3d.png")

plt.show()
