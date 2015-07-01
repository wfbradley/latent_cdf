import numpy as np
from scipy.stats import beta
from scipy.optimize import brentq
import IPython


def inverse_beta_ml_band(z,i,N):
	alpha_param=i+1
	beta_param=N-i+1

	small=.5
	if i<small:
		x=0
		xx=beta.ppf(z,alpha_param,beta_param)
	elif i>N-small:
		x=beta.ppf(1.0-z,alpha_param,beta_param)
		xx=1
		if np.isnan(x):
			print "NaN failure in beta edge case"
			IPython.embed()			
	else:
		x_min=0
		x_max=beta.ppf(1.0-z,alpha_param,beta_param)


		def g(x):
			prob_xx=beta.cdf(x,alpha_param,beta_param)+z
			if prob_xx>1: #Numerical precision paranoia
				prob_xx=1
			xx=beta.ppf(prob_xx,alpha_param,beta_param)
			prob_diff=beta.pdf(x,alpha_param,beta_param)-beta.pdf(xx,alpha_param,beta_param)
			#print '   x=%f, prob_xx=%f, xx=%f, prob_diff=%f'%(x,prob_xx,xx,prob_diff)
			return(prob_diff)
		try:
			#print '*** (x_min,x_max)=%f,%f'%(x_min,x_max)
			x=brentq(g,x_min,x_max)
			#print '    (x)=%f\n'%(x)
		except:
			print "Failure at 'brentq'."
			IPython.embed()			
		prob_xx=beta.cdf(x,alpha_param,beta_param)+z
		if prob_xx>1: #Numerical precision paranoia
			prob_xx=1
		xx=beta.ppf(prob_xx,alpha_param,beta_param)
	larger_x=np.max((x,xx))
	smaller_x=np.min((x,xx))	
	return((smaller_x,larger_x))







