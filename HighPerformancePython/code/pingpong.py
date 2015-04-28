#!/usr/bin/env mpirun -np 2 /usr/bin/env python
from __future__ import print_function
"""
University of Pittsburgh
Center for Simulation and Modeling (SaM)
High Performance Computing with Python
Esteban Meneses, PhD
"""

from mpi4py import MPI

def main():
    """Exchange of messages between two ranks."""
    # Getting basic info
    comm = MPI.COMM_WORLD
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()
    name = MPI.Get_processor_name()

    print('comm', comm)
    print('rank', rank)
    print('size', size)
    print('name', name)

    if size != 2:
        raise ValueError('Number of ranks should be exactly 2')

    # Ping-pong between two ranks
    counter = 0
    for x in range(1000):
        if rank == 0:
            comm.send(counter, dest=1, tag=7)
            counter = comm.recv(source=1, tag=7)
        else:
            counter = comm.recv(source=0, tag=7)
            counter += 1
            comm.send(counter, dest=0, tag=7)
    if rank == 0:
        print("Total number of message exchanges: {0}".format(counter))


if __name__ == '__main__':
    main()
