import matplotlib.pyplot as plt
import numpy as np
import re

class poly_plotter:
  def __init__(self, poly_string):
   self.y = None
   self.x = np.linspace(0,1,100)
   self.repr = self.parse(poly_string)
   self.string_representation = poly_string
   
  
  def eval(self,value):
   res = value*0 # a trick to make sure that if value is an array, res is the same size
   for r in self.repr:
     res += r[0]*value**r[1]
   return res
     
  def parse(self,s):
   res = s.split("+")
   space_stripper = lambda s: s.strip(" ")
   res = map(space_stripper,res)
   rep = []
   if not(len(res)):
    raise valueError()
   for r in res:
     try:
      v = int(r)
      rep.append([v, 0])
      continue
     except Exception:
      pass
     
     nums = map(int, re.findall(r'\d+', r))
     if len(nums) < 1:
      raise ValueError("Missing coefficient")
     
     if len(nums) == 1:
      # no coefficient at start of string
      if not len(re.findall("^\d+",r )):
        rep.append([1, nums[0]])
      else:
        rep.append([nums[0], 1])
     else:
      rep.append(nums)

   return rep
  
  def plot(self):
   self.y = self.eval(self.x)
   plt.plot(self.x,self.y)
   plt.title("Plot of "+self.string_representation)
   plt.show()


