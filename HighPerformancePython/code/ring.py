#!/usr/bin/env mpirun -np 2 /usr/bin/env python
from __future__ import print_function
"""
University of Pittsburgh
Center for Simulation and Modeling (SaM)
High Performance Computing with Python
Esteban Meneses, PhD
"""

from mpi4py import MPI
from random import randint

def main():
    """
    Ring exchange of messages between ranks.
    Each rank circulates its random value until it reaches all the ranks.
    """
    # Getting basic info
    comm = MPI.COMM_WORLD
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()
    name = MPI.Get_processor_name()

    # Ring exchange between ranks
    counter = 0
    data = randint(0,100)
    for x in range(size):
        comm.send(data, dest=(rank+1)%size, tag=7)
        data = comm.recv(source=(rank+size-1)%size, tag=7)
        counter += data

    print("{0} Total sum: {1}".format(rank, counter))


if __name__ == '__main__':
    main()
