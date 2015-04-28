#!/usr/bin/env mpirun -np 2 /usr/bin/env python
from __future__ import print_function
"""
University of Pittsburgh
Center for Simulation and Modeling (SaM)
High Performance Computing with Python
Esteban Meneses, PhD
Description: use of collective communication operations to compute the global sum of ranks.
"""

from mpi4py import MPI
from random import randint

def main():
    # Getting basic info
    comm = MPI.COMM_WORLD
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()
    name = MPI.Get_processor_name()

    # Use of collective communication calls
    data = randint(0,100)
    total = comm.reduce(data, op=MPI.SUM, root=0)
    total = comm.bcast(total, root=0)
    print("[{0}] Total sum: {1}".format(rank,total))

if __name__ == '__main__':
    main()
