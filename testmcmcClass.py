# -*- coding: utf-8 -*-
"""
Created on Sat Mar 07 10:56:11 2015

@author: Ryan
"""

import pylab as pl
import numpy as np
import math
import os
import MakePlots as mp
import mcmc as MC

global xdata,ydata,sigmadata,sigma_pars

def chisquare(a,b,sigma):
    """Simple chi-squared between 2 NP arrays. Assumes that sigmas are non-zero!!!"""
    if a.size != b.size:
        print "error in chisquare: arrays are not the same size"
        return 0
    if a.size != sigma.size:
        print "error in chisquare: arrays are not the same size"
        return 0
    chi=np.power((a-b)/sigma,2)#should really check if sigma is non-zero!!!
    return np.sum(chi)

def model(pars,x):
    """return a value for the model based on the parameters
    and one independent coordinate"""
    #return pars[0]+pars[1]*x
    return pars[0]/np.sqrt(2.*np.pi)/pars[2]*np.exp(-np.power((x-pars[1])/pars[2],2)/2.)

    
def make_fake_data(n,modelfcn,pars):
    xdata=np.linspace(0,n,n)
    ydata=np.zeros(n)
    sigmadata=np.zeros(n)
    for i in range(n):
        mu=max(0.,modelfcn(pars,xdata[i]))
        sigmadata[i]=math.sqrt(mu)
        ydata[i]=np.random.normal(mu,sigmadata[i],1)
    return xdata,ydata,sigmadata

def likelihood(pars):
    """Return likelihood as estimated from a chi-squared"""
    return math.exp(-0.5*chisquare(ydata,model(pars,xdata),sigmadata))
    

def proposal_pars(pars):
    """Generate trial parameters based on a gaussian proposal distribution"""
    npars=len(pars)
   
    test_pars=np.empty(npars)
    for i in range(npars):
        test_pars[i]=np.random.normal(pars[i],sigma_pars[i])
    return test_pars

###########################################################################
#####Beginning of procedural code
###########################################################################

####Generate some fake data (as global)
ndata=100
trueParameters=[100,50,10]
xdata,ydata,sigmadata=make_fake_data(ndata,model,trueParameters)

##Initialize and run the MCMC
start_pars=[100,50,10]
sigma_pars=[1.0,0.75,0.5]
mcmc=MC.MCMC(start_pars)
mcmc.get_likelihood=likelihood#set the likelihood function
mcmc.get_proposal_pars=proposal_pars#set the proposal function for trial pars
mcmc.run(10000,1000)

results=MC.MCMCResult(mcmc.accepted[mcmc.burnin:])
print results.get_par_means(),results.get_par_variances()

fig=pl.figure(figsize=[20,15],facecolor='white')
mp.MultiHistogram([mcmc.accepted[:,0],mcmc.accepted[:,1],mcmc.accepted[:,2]],["par0","par1","par2"])

acf_1=results.get_autocorr_function(1,100)
pl.plot(np.linspace(0,acf_1.size,acf_1.size),acf_1)
pl.show()






























