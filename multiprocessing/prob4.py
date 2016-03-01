from mpi4py import MPI

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()

if RANK == 0:
 if SIZE == 5:
  print "Success!"
  COMM.Abort()
 print "Error: This program must run with 5 processes!"
 

