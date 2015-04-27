# University of Pittsburgh
# Center for Simulation and Modeling (SaM)
# High Performance Computing with Python
# Esteban Meneses, PhD
# Description: parallel MPI version of a two-dimensional stencil program.

import sys
from numpy import *
import time
from mpi4py import MPI

# global values
HEAT=255
DEBUG=0

def stencil(grid,x,y,tol,comm,rank,size):
	""" Function to compute the 5-point stencil of an x """
	old = copy(grid)
	column = zeros(x)
	iteration = 0

	# iterate while error is greater than tolerance
	max_error = tol
	while max_error >= tol:
		iteration = iteration + 1
		max_error = 0.0

		# iterate over all the grid points
		for i in range(1,x-1):
			for j in range(1,y-1):
				grid[i,j] = (old[i-1,j] + old[i,j-1] + old[i+1,j] + old[i,j+1] + old[i,j]) / 5.0
				error = abs(grid[i,j] - old[i,j])
				max_error = max(max_error, error)

		# collective communication operation to reduce max_error
		value = array(max_error, 'f')
		result = array(0, 'f')
		comm.Allreduce([value,MPI.FLOAT],[result,MPI.FLOAT],op=MPI.MAX)
		max_error = result

		# move values
		tmp = old
		old = grid
		grid = tmp		
	
		# communication operations
		if rank != 0:
			copyto(column,old[:,1])
			comm.Send([column,MPI.FLOAT],dest=rank-1)
		if rank != (size-1):
			copyto(column,old[:,y-2])
			comm.Send([column,MPI.FLOAT],dest=rank+1)
		if rank != 0:
			comm.Recv([column,MPI.FLOAT],source=rank-1)
			copyto(old[:,0],column)
		if rank != (size-1):
			comm.Recv([column,MPI.FLOAT],source=rank+1)
			copyto(old[:,y-1],column)	
	
		if DEBUG:
			if rank == 0:
				print "%d %f" % (iteration,max_error)

	return iteration

# checking command-line parameters
if len(sys.argv) < 4:
    print ("ERROR, Usage: %s <grid dim x> <grid dim y> <tolerance>" % (sys.argv[0]))
    exit(1)
size_x = int(sys.argv[1])
size_y = int(sys.argv[2])
tolerance = float(sys.argv[3])

# getting basic info
comm = MPI.COMM_WORLD
rank = MPI.COMM_WORLD.Get_rank()
size = MPI.COMM_WORLD.Get_size()

# computing size on y dimension per rank
size_y_rank = (size_y-2)/size
if rank < (size_y-2) % size:
	size_y_rank = size_y_rank + 1

# creating grid
grid = zeros((size_x,size_y_rank+2))

# initialize grid
if rank == 0:
	for i in range(0,size_x):
		grid[i,0] = HEAT

# start time
if rank == 0:
	start_time = MPI.Wtime()

# calling stencil function
total = stencil(grid,size_x,size_y_rank+2,tolerance,comm,rank,size)

# printing result
if rank == 0:
	print "Convergence in %d iterations" % total

# end time
if rank == 0:
	end_time = MPI.Wtime()
	print "Execution time: %f seconds" % (end_time - start_time)

# printing grid
if DEBUG:
	if rank == 0:
		print grid
