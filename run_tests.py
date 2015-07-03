import numpy as np
import flipCoins as fc
import distributions as D
import cPickle as pickle
import matplotlib.pyplot as plt
import types
import CDF_confidence_nested as nest
from scipy.stats import beta

plot_dir='plots'
pkl_dir='pickled'

def run_test(test_name,n,m,dist,make_pickle=False):

	results=fc.flipCoins(n,m,dist)
	if make_pickle:
		max_m=np.max(m)
		pickle_filename="%s/%s_n%d_maxm%d.pkl"%(pkl_dir,name_string,n,max_m)
		pickle.dump( results, open( pickle_filename, "wb" ) )
	return(results)

def ground_truth(dist, num_bins=50, plot_histo=True,dist_type='pdf'):
	# Make "ground truth"
	num_dist_samples=500000
	if type(dist)==types.FunctionType:
		dist_samples=[dist() for i in xrange(num_dist_samples)]
	elif type(dist)==float or type(dist)==int:
		dist_samples=float(dist)*np.ones(num_dist_samples)
	else:
		dist_samples=dist

	if plot_histo:
		if dist_type=='pdf':
			# the histogram of the data with histtype='step'
			n, bins, patches = plt.hist(dist_samples, num_bins, normed=1,
				histtype='stepfilled',label='True dist')
			plt.setp(patches, 'facecolor', 'g', 'alpha', 0.75)
		elif dist_type=='cdf':
			x=np.sort(dist_samples)		
			y=np.linspace(0,1,len(x))
			plt.plot(x,y,label='True dist')
			plt.ylim([0,1])
		else:
			raise NameError('Unknown dist_type')
		plt.title(test_name)
		plt.xlim([0,1])
	return(dist_samples)

# CI = "credible interval" = how much probability is contained in the 
# error bars around the estimate at each point
def guess_beta(num_weights,results,CI=.9,alpha=.3,color='green'):
	num_coins=fc.total_num_coins(results)
	x=np.linspace(0,1,num_weights)
	y=np.zeros(num_weights)
	lower=np.zeros(num_weights)
	upper=np.zeros(num_weights)
	for i,xx in enumerate(x):
		for num_flips in results:
			for heads in results[num_flips]:
				#print 'num_flips=%d,heads=%d'%(num_flips,heads)
				sum_weight=float(results[num_flips][heads])/float(num_coins)
				y[i]+=sum_weight * beta.cdf(xx,heads+1,num_flips-heads+1)
	if y[-1]>1.0:
		#print 'y[-1] = %f !  Fixing...'%(y[-1])
		y/=y[-1]
	for i,xx in enumerate(x):
		(lower[i],upper[i])=nest.inverse_beta_ml_band(CI,y[i]*float(num_coins),num_coins)

	plt.plot(x,y,color=color,label='Estimate with %.1f%% credible interval'%(100.0*CI))
	ax=plt.gca()
	ax.fill_between(x,lower,upper,alpha=alpha,color=color)


if __name__ == "__main__":
	# Choose some weight distributions and sets of coin flips to test on.
	tests=[]
	#     (name, num coins, num flips per coin, coin weight distribution)
	tests.append(('half_uniform',1024,100,D.half_uniform))
	tests.append(('uniform',1024,10,D.uniform)
	tests.append(('all_coins_0.8',40,1000,0.8))
	tests.append(('two_sails_400',1024,400,D.two_sails)
	tests.append(('two_sails_10',1024,10,D.two_sails)

	for (test_name,n,m,dist) in tests:
		results=run_test(test_name,n,m,dist)
		ground_truth(dist,dist_type='cdf')
		guess_beta(1000,results,color='purple')
		plt.legend(loc='best')
		plt.show()
