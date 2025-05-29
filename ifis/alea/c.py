import numpy as np
import matplotlib.pyplot as plt

x, y = np.meshgrid(np.linspace(-5, 5, 10), np.linspace(-5, 5, 10))
P = -y  # Componente x (horizontal)
Q = x   # Componente y (vertical)

plt.quiver(x, y, P, Q)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Campo Vetorial Rotacional: F(x, y) = (-y, x)')
plt.grid()
plt.show()