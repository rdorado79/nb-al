'''
import matplotlib.pyplot as plt
import numpy as np
import pymc as mc
from pymc.Matplot import plot

# generate simulated data
ndata = 1000
numCat = 4
c = np.random.randint(0,numCat,ndata)
mu = [-10,0,10,20]
sigma = .25
sample = np.zeros(ndata)
for i in range(ndata):
    sample[i] = np.random.normal(mu[c[i]],sigma,1)

#print sample

# define the model in PyMC
#labels = mc.Categorical('labels', p = np.array([.25,.25,.25,.25]),size = ndata) 
labels = mc.Container([mc.Categorical('label_%d' % i, p = .25) for i in range(4)]) 
means = mc.Uniform('means', lower=-30., upper=30., size=numCat)

@mc.deterministic
def mean(labels=labels, means=means):
    return means[labels]

obs = mc.Normal('obs', mean, 1/(sigma**2), value=sample, observed = True)
model = mc.Model({'labels': labels,'means': means, 'obs': obs})

# fit the model
mcmc = mc.MCMC( model )
mcmc.sample( 5000, 0 )


results = mcmc.trace("means")[:]
results = zip(*results)
for r in results:
  print np.mean(r)
#plot(mcmc)

'''

import pymc as pm
import numpy as np
import matplotlib.pyplot as plt

#create the data
mu1, mu2, sigma = 100, 400, 40 # mean and standard deviation
data1 = np.random.normal(mu1, sigma, 1000)
data2 = np.random.normal(mu2, sigma, 1000)
data = np.append(data1, data2)
np.random.shuffle(data)

# the histogram of the data
n, bins, patches = plt.hist(data, 50, normed=1, facecolor='green', alpha=0.75)

#plt.show()


theta = pm.Uniform("theta", lower=0, upper=1)
bern = pm.Bernoulli("bern", p=theta, size=len(data))

mean1 = pm.Uniform('mean1', lower=min(data), upper=max(data))
mean2 = pm.Uniform('mean2', lower=min(data), upper=max(data))
std_dev = pm.Uniform('std_dev', lower=0, upper=50)

@pm.deterministic(plot=False)
def mean(bern=bern, mean1=mean1, mean2=mean2):
    return bern * mean1 + (1 - bern) * mean2

@pm.deterministic(plot=False)
def precision(std_dev=std_dev):
    return 1.0 / (std_dev * std_dev)

process = pm.Normal('process', mu=mean, tau=precision, value=data, observed=True)
model = pm.Model({'process': process, 'std_dev': std_dev, 'mean1':mean1, 'mean2':mean2})

mcmc = pm.MCMC( model )
mcmc.sample( 2000, 0 )


for p in ['mean1','mean2','std_dev']:
    print np.mean(mcmc.trace(p)[-1500:])






