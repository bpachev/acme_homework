from solutions import *
import pytest

def test_fibbo():
  assert fibonacci(1) == 1
  assert fibonacci(2) == 2
  assert fibonacci(9) == 55
  with pytest.raises(Exception) as excinfo:
      fibonacci(-1)
  assert excinfo.typename == 'ValueError'
