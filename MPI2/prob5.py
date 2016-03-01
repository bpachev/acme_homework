from mpi4py import MPI
import numpy as np
from sys import argv

comm = MPI.COMM_WORLD
rank = comm.Get_rank()



n = comm.Get_size()

if rank == 0:
  x = np.random.random(n)
  A = np.random.random((n,n))
  rec_buf = np.zeros(n)
  print "Serial verision", A.dot(x)
else:
  x,A,rec_buf = None,None,None

local_a = np.empty(n)
comm.Scatter(A,local_a)
comm.Bcast(x,root = 0)
local_a = local_a * local_x[0]
comm.Reduce(local_a,rec_buf,op=MPI.SUM)
if rank == 0:
 print rec_buf
#print "process "+str(rank)+" has ",local_a,local_x
