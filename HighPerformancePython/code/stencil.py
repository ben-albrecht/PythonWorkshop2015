#!/usr/bin/env python
from __future__ import print_function, division
"""
University of Pittsburgh
Center for Simulation and Modeling (SaM)
High Performance Computing with Python
Esteban Meneses, PhD
Description: sequential version of a two-dimensional stencil program.
"""

import sys
from time import clock
import numpy as np

# Global values
DEBUG=0

def stencil(grid,x,y,tol):
    """ Function to compute the 5-point stencil of an x """
    old = np.copy(grid)
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

        # Move values
        tmp = old
        old = grid
        grid = tmp

        if DEBUG:
            print('{0:d} {1:f}'.format(iteration,max_error))

    return iteration

def main():

    heat = 255

    # Checking command-line parameters
    if len(sys.argv) < 4:
        print ('ERROR, Usage: {0} <grid dim x> <grid dim y> <tolerance>'.format(sys.argv[0]))
        exit(1)

    size_x = int(sys.argv[1])
    size_y = int(sys.argv[2])
    tolerance = float(sys.argv[3])

    # Creating grid
    grid = np.zeros((size_x,size_y))

    # Initialize grid
    for i in range(0,size_x):
        grid[i,0] = heat

    # Start time
    start_time = clock()

    # Calling stencil function
    total = stencil(grid,size_x,size_y,tolerance)

    # Printing result
    print('Convergence in  iterations'.format(total))

    # End time
    end_time = clock()
    print('Execution time: {0} seconds'.format(end_time - start_time))

    # Printing grid
    if DEBUG:
        print(grid)

if __name__ == '__main__':
    main()
