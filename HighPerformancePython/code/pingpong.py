# University of Pittsburgh
# Center for Simulation and Modeling (SaM)
# High Performance Computing with Python
# Esteban Meneses, PhD
# Description: exchange of messages between two ranks.

from mpi4py import MPI

# getting basic info
comm = MPI.COMM_WORLD
rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()
name = MPI.Get_processor_name()
if size != 2:
    print("Number of ranks should be exactly 2")
    exit(1)

# ping-pong between two ranks
counter = 0
for x in xrange(1000):
    if rank == 0:
        comm.send(counter, dest=1, tag=7)
        counter = comm.recv(source=1, tag=7)
    else:
        counter = comm.recv(source=0, tag=7)
        counter += 1
        comm.send(counter, dest=0, tag=7)
if rank == 0:
    print("Total number of message exchanges: %d" % counter)
