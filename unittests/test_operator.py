from solutions import *
import pytest

def test_operator():
  assert operator(1,1,"+") == 2
  assert operator(1,1,"-") == 0
  assert operator(3,4,"*") == 12
  assert operator(100,10,"/") == 10.
  with pytest.raises(Exception) as excinfo:
    operator(1,0,"/")
  assert excinfo.typename == "ValueError"
  assert excinfo.value.args[0] == "You can't divide by zero!"

  with pytest.raises(Exception) as excinfo:
    operator(1,0,"foo")
  assert excinfo.typename == "ValueError"
  assert excinfo.value.args[0] == "Oper should be one character"

  with pytest.raises(Exception) as excinfo:
    operator(1,0,[])
  assert excinfo.typename == "ValueError"
  assert excinfo.value.args[0] == "Oper should be a string"

  with pytest.raises(Exception) as excinfo:
    operator(1,0,"%")
  assert excinfo.typename == "ValueError"
  assert excinfo.value.args[0] == "Oper can only be: '+', '/', '-', or '*'"
  
  
