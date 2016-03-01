from plot_poly import *
import numpy as np
import pytest

def test_poly_eval():
  dom = np.linspace(0,1,200)
  e = lambda x: x**2 + 3*x + 1
  p = poly_plotter("x**2 + 3*x + 1")
  assert np.allclose(p.eval(dom), e(dom))
  assert p.repr[0] == [1, 2]
  

