from module import *
import h5py
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from math import pi, sqrt

# external stuff to be defined at global level
file_preVFP = '/scratchnvme/emanca/wproperties-analysis/config/outputW_preVFP/WPlusJetsToMuNu_helweights.hdf5'
file_postVFP = '/scratchnvme/emanca/wproperties-analysis/config/outputW_postVFP/WPlusJetsToMuNu_helweights.hdf5'

f_preVFP = h5py.File(file_preVFP, mode='r+')
f_postVFP = h5py.File(file_postVFP, mode='r+')

# merge pre and post VFP xsecs
htot_preVFP = f_preVFP['totxsecs'][:]
htot_postVFP = f_postVFP['totxsecs'][:]
h_preVFP = f_preVFP['xsecs'][:]
h_postVFP = f_postVFP['xsecs'][:]

yBins = f_preVFP['edges_totxsecs_0'][:]
qtBins = f_preVFP['edges_totxsecs_1'][:]

htot = htot_preVFP+htot_postVFP
h = h_preVFP+h_postVFP
factors = np.array([[20./3., 1./10],[5.,0.],[20.,0.],[4.,0.],[4.,0.],[5.,0.],[5.,0.],[4.,0.],[1.,0.]])
factors = factors[np.newaxis,np.newaxis,...]
print(factors.shape)
h = (h/htot[...,np.newaxis]+factors[...,1])*factors[...,0]

factors_hel = np.array([2.,2*sqrt(2),4.,4.*sqrt(2),2.,2.,2.*sqrt(2),4.*sqrt(2),1.])
factors_hel = factors_hel[np.newaxis,np.newaxis,...]
h = h/factors_hel

@ROOT.Numba.Declare(["float", "float"], "RVec<double>")
def getCoefficients(y, pt):
    biny = np.digitize(np.array([y]), yBins)[0]-1
    binpt = np.digitize(np.array([pt]), qtBins)[0]-1
    coeff = np.zeros(h.shape[-1])
    for i in range(h.shape[-1]):
        coeff[i]=h[biny,binpt,i]
    return coeff

@ROOT.Numba.Declare(["float", "float", "RVec<double>", "RVec<float>"], "float")
def getNorm(y, pt, coeffs, harms):
    biny = np.digitize(np.array([y]), yBins)[0]-1
    binpt = np.digitize(np.array([pt]), qtBins)[0]-1
    totMap = htot[biny,binpt]
    norm =harms[-1]*totMap
    for i in range(coeffs.shape[0]-1):
        norm += coeffs[i]*harms[i]*totMap
    norm *=3./16./pi
    return norm

@ROOT.Numba.Declare(["float", "float", "RVec<double>", "RVec<float>","float"], "RVec<float>")
def getWeights(y, pt, coeffs, harms, norm):
    biny = np.digitize(np.array([y]), yBins)[0]-1
    binpt = np.digitize(np.array([pt]), qtBins)[0]-1
    totMap = htot[biny,binpt]
    weights = np.zeros(h.shape[-1],dtype='float32')
    for i in range(h.shape[-1]):
        if(norm!=0.):
            if i!=8:
                weights[i] = 3./16./pi * totMap * coeffs[i] *harms[i]/norm
            else:
                weights[i] = 3./16./pi * totMap *harms[i]/norm
    return weights

class getHelWeights(module):
   
    def __init__(self):
        pass
      

    def run(self,d):

        self.d = d
        
        self.d = self.d.Define("AngCoeffVec", "Numba::getCoefficients(Vrap_preFSR_abs,Vpt_preFSR)")\
            .Define("norm", "Numba::getNorm(Vrap_preFSR_abs,Vpt_preFSR,AngCoeffVec,harmonicsVec)")\
            .Define("helWeights", "Numba::getWeights(Vrap_preFSR_abs,Vpt_preFSR,AngCoeffVec,harmonicsVec,norm)")\
            .Define("nhelWeights", "helWeights.size()")
        
        return self.d

    def getTH1(self):

        return self.myTH1

    def getTH2(self):

        return self.myTH2  

    def getTH3(self):

        return self.myTH3

    def getTHN(self):

        return self.myTHN

    def getGroupTH1(self):

        return self.myTH1Group

    def getGroupTH2(self):

        return self.myTH2Group  

    def getGroupTH3(self):

        return self.myTH3Group  

    def getGroupTHN(self):

        return self.myTHNGroup

    def reset(self):

        self.myTH1 = []
        self.myTH2 = []
        self.myTH3 = [] 
        self.myTHN = [] 

        self.myTH1Group = []
        self.myTH2Group = []
        self.myTH3Group = [] 
        self.myTHNGroup = [] 
