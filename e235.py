from sympy.mpmath import *
import numpy as np
import matplotlib.pyplot as plt

mp.dps = 50
def solve(n=5000,C=-6*10**11,a=900,b=3):
 """
 u(k,r) = (a-bk) * r^(k+1)
 s(n,r) = sum i = 1 to n u(i,r)
 Solve s(r) = C for r
 """
 coeffs = np.zeros(n+2)
 coeffs[0] = a-b*n
 coeffs[1] = b*(n+1) - a
 coeffs[-3] = -C
 coeffs[-2] = 2*C - a
 coeffs[-1] = a+b-C
 mp.dps = 27
 roots = polyroots(coeffs)
 for root in roots:
  print root

def objective(rp,n=5000,C=-2*10**11,a=300,b=1):
 """
 Takes in r^n and evaluates p from solve
 """
 l = log(rp)/n
 r = exp(l)
 rm1 = r-1
 return (rp-1)*((a-b*n)*rm1 + 1) - C*(rm1)*(rm1)
 #return rm1

def obj2(r,n=5000,C=-2*10**11,a=300,b=1):
 rm1 = r-1
 return (r**n-1)*((a-b*n)*rm1+1) - C*rm1*rm1

def obj3(r):
 s = 0
 for i in xrange(1,5001):
  s += (300-i)*r**(i-1)
 return s+2*10**11

def secant_method(F,x0=1,x1=0.1,maxiters = 20, tol = 1e-13):
  niters = 0
  while abs(x1-x0) > tol:
    fx1 = F(x1)
    x1_old = x1
    x1 = x1 - fx1*(x1 - x0) / (fx1 - F(x0))
    x0 = x1_old
    niters += 1
    if niters == maxiters:
      break
  return x1


rp = secant_method(obj3,mpf("1.002"),mpf("1.003"),maxiters=10000,tol=1e-16)
print str(rp)[:15],obj3(rp)
#r = exp(log(rp)/5000)
#print r,obj2(r),obj3(r)

