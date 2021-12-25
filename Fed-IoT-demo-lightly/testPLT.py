import matplotlib.pyplot as plt
import numpy as np
import time
from math import *
import random
 
plt.ion() #开启interactive mode 成功的关键函数
plt.figure(1)
a0 = plt.subplot(131)
a1 = plt.subplot(132)
a2 = plt.subplot(133)

n = 500

x = []
y = []
z = []

for i in range(1, n):
    plt.clf()
    
    a11 = plt.subplot(231)
    a12 = plt.subplot(232)
    a13 = plt.subplot(233)
    a21 = plt.subplot(234)
    a22 = plt.subplot(235)
    a23 = plt.subplot(233)
    
    #x.append(i)
    #y.append(random.randint(1, 10000))
    m = 1 - 2**(-i)
    n = 2**(-(i/10))
    x.append(i)
    y.append(m)
    z.append(n)
    if i > 100:
        x.pop(0)
        y.pop(0)
        z.pop(0)
    #a0.plot(x, y, linewidth = '1', label = "test", color='coral', linestyle=':', marker='|')

    a11.plot(x, y, label='accuracy', color='red')
    a11.legend(loc='upper right')
    a21.plot(x, z, label='loss', color='blue')
    a21.legend(loc='upper right')
    a22.plot(m, n)
    a2.plot(x, y)
    plt.pause(0.001)
    plt.draw()

#plt.plot()