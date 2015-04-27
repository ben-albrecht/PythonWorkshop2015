# University of Pittsburgh
# Center for Simulation and Modeling (SaM)
# High Performance Computing with Python
# Esteban Meneses, PhD
# Description: ring exchange of messages between ranks. Each rank circulates its random value until it reaches all the ranks.

from mpi4py import MPI
from random import randint

# getting basic info
comm = MPI.COMM_WORLD
rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()
name = MPI.Get_processor_name()

# ring exchange between ranks
counter = 0
data = randint(0,100)
for x in xrange(size):
    comm.send(data, dest=(rank+1)%size, tag=7)
    data = comm.recv(source=(rank+size-1)%size, tag=7)
    counter += data

print("[%d] Total sum: %d" % (rank,counter))
