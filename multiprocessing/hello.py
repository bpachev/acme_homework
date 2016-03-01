from mpi4py import MPI

COMM = MPI.COMM_WORLD
RANK = COMM.Get_rank()
SIZE = COMM.Get_size()

print "Hello World from process {} out of {}\n".format(RANK,SIZE)
