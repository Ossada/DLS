import math
import time

t = 273.15
a = time.time()
nov = t**2
print(time.time() - a)
print(nov)
a = time.time()
nov = t*t
print(time.time() - a)
print(nov)
print('kvadrat')

a = time.time()
nov = t**3
print(time.time() - a)
print(nov)
nov = t*t*t
print(time.time() - a)
print(nov)
print('kub')

a = time.time()
nov = t**4
print(time.time() - a)
print(nov)
nov = t*t*t*t 
print(time.time() - a)
print(nov)
print('četrta ')