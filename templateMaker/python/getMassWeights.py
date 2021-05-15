from module import *
import h5py
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from math import pi, sqrt

class getMassWeights(module):
   
    def __init__(self, syst = ""):
        pass
      
    def run(self,d):

        @ROOT.Numba.Declare(["RVec<float>"], "RVec<float>")
        def getMassWeights(fullvec): # corresponding to a variation of 50 MeV
            red = np.zeros((2,),dtype='float32')
            red[0]=fullvec[16]
            red[1]=fullvec[6]
            return red
        
        @ROOT.Numba.Declare(["RVec<float>", "RVec<float>"], "RVec<float>")
        def vecMultiplication (v1, v2):
            products = np.zeros((v1.shape[0],v2.shape[0]),dtype='float32')
            for i in range(products.shape[0]):
              for j in range(products.shape[1]):
                products[i,j] = v1[i]*v2[j]
            return products.ravel()

        self.d = d
        self.d = self.d.Define("massWeights","Numba::getMassWeights(LHEReweightingWeightCorrectMass)").Define("helmassWeights", "Numba::vecMultiplication(helWeights,massWeights)")\
            .Define("nhelmassWeights", "helmassWeights.size()")
        
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
