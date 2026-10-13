import matplotlib.pyplot as plt
import numpy as np
x = [i for i in range (-5, 5)]
y = [2 * x + (np.sin(x) ** 2) + 3 for x in x]
fig, ax = plt.subplots()
ax.plot(x, y)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_title('hello, po!')
ax.grid(True)
plt.show()