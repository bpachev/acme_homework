from solutions import *
import pytest

def test_list_node():
  n1,n2 = LinkedListNode(1), LinkedListNode(2)
  assert n1.data == 1
  assert n1.next == None
  assert str(n1) == "1"
  assert n1 == n1
  assert not n1 == n2
  assert n1 < n2
  assert n2 > n1
  assert not n1 > n2
  assert not n2 < n1

def test_list():
  l = []
  linked = LinkedList()
  assert str(l)== str(linked)
  with pytest.raises(Exception) as e:
   linked.remove(8)
  assert e.typename == "ValueError"

  with pytest.raises(Exception) as e:
   linked.insert(1,3)
  assert e.typename == "ValueError"  

  for i in xrange(10):
   l.append(i)
   linked.add(i)
   assert str(l) == str(linked)
  
  for el in xrange(9):
   l.remove(el)
   linked.remove(el)
   assert str(l) == str(linked)
  
  for el in xrange(20, 30):
   l.insert(0,el)
   linked.insert(el, linked.head.data)
   assert str(l) == str(linked)
 
