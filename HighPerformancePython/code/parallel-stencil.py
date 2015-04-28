#!/usr/bin/env mpirun -np 2 /usr/bin/env python
from __future__ import print_function, division
"""
University of Pittsburgh
Center for Simulation and Modeling (SaM)
High Performance Computing with Python
Esteban Meneses, PhD
Description: parallel MPI version of a two-dimensional stencil program.
"""

from mpi4py import MPI
import sys
import numpy as np

DEBUG=0

def stencil(grid, x, y, tol, comm, rank, size):
    """ Function to compute the 5-point stencil of an x """
    old = np.copy(grid)
    column = np.zeros(x)
    iteration = 0

    # Iterate while error is greater than tolerance
    max_error = tol
    while max_error >= tol:
        iteration = iteration + 1
        max_error = 0.0

        # Iterate over all the grid points
        for i in range(1,x-1):
            for j in range(1,y-1):
                grid[i,j] = (old[i-1,j] + old[i,j-1] + old[i+1,j] + old[i,j+1] + old[i,j]) / 5.0
                error = abs(grid[i,j] - old[i,j])
                max_error = max(max_error, error)

        # Collective communication operation to reduce max_error
        value = np.array(max_error, 'f')
        result = np.array(0, 'f')
        comm.Allreduce([value,MPI.FLOAT],[result,MPI.FLOAT],op=MPI.MAX)
        max_error = result

        # Move values
        tmp = old
        old = grid
        grid = tmp

        # Communication operations
        if rank != 0:
            np.copyto(column,old[:,1])
            comm.Send([column,MPI.FLOAT],dest=rank-1)
        if rank != (size-1):
            np.copyto(column,old[:,y-2])
            comm.Send([column,MPI.FLOAT],dest=rank+1)
        if rank != 0:
            comm.Recv([column,MPI.FLOAT],source=rank-1)
            np.copyto(old[:,0],column)
        if rank != (size-1):
            comm.Recv([column,MPI.FLOAT],source=rank+1)
            np.copyto(old[:,y-1],column)

        if DEBUG:
            if rank == 0:
                print('{0} {1}'.format(iteration,max_error))

    return iteration

def main():

    heat=255

    # Checking command-line parameters
    if len(sys.argv) < 4:
        print("ERROR, Usage: {0} <grid dim x> <grid dim y> <tolerance>".format(sys.argv[0]))
        sys.exit(1)

    size_x = int(sys.argv[1])
    size_y = int(sys.argv[2])
    tolerance = float(sys.argv[3])

    # Getting basic info
    comm = MPI.COMM_WORLD
    rank = MPI.COMM_WORLD.Get_rank()
    size = int(MPI.COMM_WORLD.Get_size())

    # Computing size on y dimension per rank
    size_y_rank = (size_y-2)//size
    if rank < (size_y-2) % size:
        size_y_rank = size_y_rank + 1

    # Creating grid
    grid = np.zeros((size_x,size_y_rank+2))

    # Initialize grid
    if rank == 0:
        for i in range(0,size_x):
            grid[i,0] = heat

    # Start time
    if rank == 0:
        start_time = MPI.Wtime()

    # Calling stencil function
    total = stencil(grid,size_x,size_y_rank+2,tolerance,comm,rank,size)

    # Printing result
    if rank == 0:
        print("Convergence in {0} iterations".format(total))

    # End time
    if rank == 0:
        end_time = MPI.Wtime()
        print("Execution time: {0} seconds".format(end_time - start_time))

    # Printing grid
    if DEBUG:
        if rank == 0:
            print(grid)

if __name__ == '__main__':
    main()
