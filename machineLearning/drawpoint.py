import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
x1 = [0,0]
y1 = [1,-1]
x2 = [-2,2]
y2 = [0,0]
plt.xlabel("x")
plt.ylabel("y")

plt.plot(x1, y1,'*',label='A')
plt.plot(x2, y2,'*',label='B')
plt.show()
