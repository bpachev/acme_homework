import numpy as np
import timeit
import matplotlib.pyplot as plt
import subprocess

def prob1():

 n = 18
 times = []
 for i in xrange(n):
  setup = """
import numpy as np
a=np.zeros(2**18)
"""
  
  code = """
a[::2**"""+str(i)+"""] = 1
"""
  times.append(sum(timeit.repeat(code, setup=setup, number = 10, repeat = 10))/10.)
 plt.plot(np.arange(n/2),times[:n/2],marker = 'o')
 plt.grid()
 plt.xlabel("Step Size (powers of 2)")
 plt.xticks(np.arange(n/2),["2^"+str(i) for i in xrange(n/2)])
 plt.ylabel("Time")
 plt.show()

def prob2():
 """
 determines the L1, and L2 cache sizes
 """
 times = []
 subprocess.call(["gcc","-O3","-mtune=native","-o","cache_size","cache_size.c"])
 for i in xrange(10, 20):
  res = subprocess.check_output(["./cache_size","16" ,str(2**(i-10)),"10"])
  times.append(float(res.split(" ")[0][:-1]))
 plt.plot(times,marker='o')
 plt.grid()
 plt.xlabel("Array Size (bytes)")
 plt.xticks(np.arange(10),["2^"+str(i+10) for i in xrange(10)])
 plt.ylabel("Time")
 plt.show()
prob2()
