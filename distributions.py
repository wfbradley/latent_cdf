# A list of distributions on [0,1], where "distribution"
# is defined as something that can be consumed by "flipCoins()"

import numpy as np

# Uniform on [0,1] interval
def uniform():
	return(np.random.rand())

# Uniform on [0,0.5] interval
def half_uniform():
	return(np.random.rand()/2.0)

# Two symmetric triangle waves, one on [0,1/2] and one on
# [1/2,1].  So, maximum probability at 1/4 and 3/4.
def two_sails():
	# The maximum of two uniform [0,1] r.v.s is a "y=x" r.v.
	x=np.max(np.random.rand(2))/4.0
	if np.random.randint(2)==0:
		x=0.5-x
	if np.random.randint(2)==0:
		x+=0.5
	return(x)


