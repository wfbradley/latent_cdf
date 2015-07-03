This repository is designed for testing statistical techniques for estimating latent distributions.

Specifically, consider the following generative process:

For i=1,2,...,N:
   Make a coin with weight w(i), where w(i) is drawn i.i.d from some distribution D on [0,1].
   Flip the coin M(i) times and output the resulting sequence of heads and tails.

We are interested in solving the inference problem:
   Given the sequence of heads and tails for each coin, infer D.

Note that in the inference problem, we observe N, M(1),...,M(N), and the number of heads and tails for each coin.

If we observed the w(i) directly, then we would be trying to recover D from i.i.d. samples.  A natural approach could be to consider the CDF of the empirical distribution.  This gives us a point estimate for each quantile.  In fact, the (marginal) posterior distribution of each quantile can be computed exactly, and is some beta distribution for each sample.

We would like to construct a similar estimate for the CDF of D.

To run this code, run:
	python run_tests.py
After a few seconds, you should see a plot showing the performance of an estimator on a synthetic data sets.  Close
the plot, and a few seconds you'll see the performance on a second synthetic data set, and so forth.




