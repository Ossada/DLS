import matplotlib.pyplot as plt 
import random

a = [random.random() for i in range(100)]
b = [random.random() for j in range(100)]

naslov = ['100', '100']
plt.plot(a, b, 'go')
plt.xlabel('$b_{{10}} = {0}$'.format(naslov[0]))
plt.show()