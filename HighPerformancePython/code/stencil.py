# University of Pittsburgh
# Center for Simulation and Modeling (SaM)
# High Performance Computing with Python
# Esteban Meneses, PhD
# Description: sequential version of a two-dimensional stencil program.

import sys
from numpy import *
from time import clock

# global values
HEAT=255
DEBUG=0

def stencil(grid,x,y,tol):
	""" Function to compute the 5-point stencil of an x """
	old = copy(grid)
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

		# move values
		tmp = old
		old = grid
		grid = tmp		
		
		if DEBUG:
			print "%d %f" % (iteration,max_error)

	return iteration

# checking command-line parameters
if len(sys.argv) < 4:
    print ("ERROR, Usage: %s <grid dim x> <grid dim y> <tolerance>" % (sys.argv[0]))
    exit(1)
size_x = int(sys.argv[1])
size_y = int(sys.argv[2])
tolerance = float(sys.argv[3])

# creating grid
grid = zeros((size_x,size_y))

# initialize grid
for i in range(0,size_x):
	grid[i,0] = HEAT

# start time
start_time = clock()

# calling stencil function
total = stencil(grid,size_x,size_y,tolerance)

# printing result
print "Convergence in %d iterations" % total

# end time
end_time = clock()
print "Execution time: %f seconds" % (end_time - start_time)

# printing grid
if DEBUG:
	print grid
