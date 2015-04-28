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
    """Traditional Hello World example in MPI4Py."""

    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()
    name = MPI.Get_processor_name()

    print("Hello, world! This is rank %d of %d running on %s" % (rank, size, name))

if __name__ == '__main__':
    main()
