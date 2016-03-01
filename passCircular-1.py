import numpy as np
from sys import argv
from mpi4py import MPI

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()

if RANK == 0:
 val = np.random.rand(1)
 print val
 COMM.Send(val,dest=(RANK+1)%SIZE)
 rec_buf=np.zeros(1)
 COMM.Recv(rec_buf,source=(RANK-1)%SIZE)
 print "Process {}, sent {}, recieved {}".format(RANK,val,rec_buf) 
else:
 rec_buf=np.zeros(1)
 COMM.Recv(rec_buf,source=(RANK-1)%SIZE)
 val = np.random.rand(1)
 COMM.Send(val,dest=(RANK+1)%SIZE)
 print "Process {}, sent {}, recieved {}".format(RANK,val,rec_buf)

