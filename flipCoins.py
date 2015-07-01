import numpy as np
import types

# We consider the following generative process: We are given a distribution
# D on [0,1].  We generate n coins, each with a weight drawn iid from D.
# We flip the i=th coin m(i) times and observe the results.
#
# The inference problem is: given n, {m_i}, and the flips, recover (a maximum
# likelihood estimate for) D
#
# Usage: n is the number of coins selected.
#        m is the number of flips for each coin.  We can have
#			m=5   			# 5 flips for each coin
#			m=[3,17,2]  	# 3 flips for first coin, 17 for 2nd, etc
#			m=f 			# Can pass a function called independently
#							# on each coin.  Function takes no inputs.
# 		 D is the distribution on [0,1] of coin weights (=prob of
#							flipping a 1, i.e. weight = expected value
#							of coin)
#			D=[.1,.8,.2]	# .1 weight for first coin, .8 for 2nd, etc
#			D=f 			# Can pass a function called independently
#							# on each coin.  Function takes no inputs.
#           D=.7			# .7 weight for each coin.
#        
#
# Output is out{}, where
#   out[number_of_times_coin_flipped][number_of_heads]
#		=number of times we observed this

def flipCoins(n,m,D):

	# Figure out how many times we flip each coin
	if type(m)==types.FunctionType:
		num_flip_list=[m() for i in xrange(n)]
	elif type(m)==int:
		num_flip_list=m*np.ones(n)
	else:
		num_flip_list=m

	if len(num_flip_list)!=n:
		print "There are %d coins, but len(m)=%d"%(n,len(m))
		sys.exit(1)

	# Figure out weight for each coin
	if type(D)==types.FunctionType:
		weights=[D() for i in xrange(n)]
	elif type(D)==float or type(D)==int:
		weights=float(D)*np.ones(n)
	else:
		weights=D
		if len(D)!=n:
			print "There are %d coins, but len(D)=%d"%(n,len(D))
			sys.exit(1)

	# Actually flip all the coins
	out={}
	for i in xrange(n):
		# Actually flip coins
		num_flips=num_flip_list[i]
		num_heads=np.random.binomial(num_flips,weights[i])

		if num_flip_list[i] not in out:
			out[num_flips]={}
		if num_heads not in out[num_flips]:
			out[num_flips][num_heads]=0
		out[num_flip_list[i]][num_heads]+=1

	return(out)

def total_num_coins(out):
	total=0
	for num_flip in out:	
		total+=sum(out[num_flip].values())
	return(total)

def total_num_coin_flips(out):
	total=0
	for num_flip in out:
		total+=num_flip * sum(out[num_flip].values())
	return(total)
