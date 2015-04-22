# -*- coding: utf-8 -*-
"""
Created on Wed Mar 04 18:41:11 2015

@author: Ryan
"""
import pylab as pl
import numpy as np
import os

#make a bunch of xy plots
def MultiPlot(xypairs,titles):
    """PLot a series of xy graphs and automatically determine the number of subplots"""
    nplot=len(xypairs)
    nx=nplot
    ny=1
    if nplot>15:
        print "MultiPlot can only handle 15 histograms"
        return    
    if nplot>4:
        ny=2   
        if nplot>10:
            ny=3  
        nx= nplot/ny if nplot%ny==0 else nplot/ny+1 
        
    for i in range(nplot):
        pl.subplot(nx,ny,i+1,title=titles[i])
        ax = pl.gca()  # gca stands for 'get current axis'
        ax.spines['right'].set_color('none')
        ax.spines['top'].set_color('none')
        ax.xaxis.set_ticks_position('bottom')
        ax.spines['bottom'].set_position(('data',0))
        ax.yaxis.set_ticks_position('left')
        ax.spines['left'].set_position(('data',0))
        if len(xypairs[i])==3:#allow for a third parameter with the xypair to control the plot         
            pl.plot(xypairs[i][0],xypairs[i][1],xypairs[i][2])
        else:
            pl.plot(xypairs[i][0],xypairs[i][1])  
    pl.tight_layout()
    pl.show()

#histograms a list of Numpy arrays (nparrs)
def MultiHistogram(nparrs,titles,nbins=50):
    """Automatically plot a bunch of histograms and determine the layout for subplots"""
    nhist=len(nparrs)
    nx=nhist
    ny=1
    if nhist>15:
        print "HistogramArrays can only handle 15 histograms"
        return
    if nhist>4:
        nx=4
        ny=2
        if nhist>8:
            nx=5
            if nihist>10:
                ny=3

    for i in range(nhist):
        pl.subplot(nx,ny,i+1,title=titles[i])
        pl.hist(nparrs[i],bins=nbins)
    pl.tight_layout()
    pl.show() 
    
#Draws a 2D heat map, assuming 3 columns of data, for x,y,z (z is the heat)
def HeatMap(filename,delim=','):
    """Read a file to produce a 2D Histogram"""
    xyz=np.genfromtxt(os.path.normpath(filename),delimiter=delim)
    x=xyz[:,0]
    y=xyz[:,1]
    z=xyz[:,2]    
#    xmax=np.amax(x)
#    xmin=np.amin(x)
#    ymax=np.amax(y)
#    ymin=np.amin(y)  
#    
#    xi = np.linspace(xmin,xmax,4)
#    yi = np.linspace(ymin,ymax,4)
#    # grid the data.
#    zi = pl.griddata(x, y, z, xi, yi, interp='linear')  
    #pl.contour(xi, yi, zi, 15, linewidths=0.5, colors='k') 
    xi,yi=np.meshgrid(x,y)
    #pl.tricontourf(x,y,z,20)

    zi=z.reshape(15,15)

   # pl.plot(xi,yi,zi)
    pl.pcolor(zi)
    pl.colorbar()
    pl.show()
    
    
    
    
    
    
    