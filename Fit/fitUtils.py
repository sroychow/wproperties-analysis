import ROOT
import pickle
from termcolor import colored
import math
from HiggsAnalysis.CombinedLimit.DatacardParser import *
from collections import OrderedDict
import copy
from systToapply import systematicsDict
import numpy as np
import sys
sys.path.append('../Common/data')
import h5py

class fitUtils:
    def __init__(self, channel ="WPlus", doSyst=False):
        
        self.doSyst = doSyst
        self.processes = []
        self.signals = []

        #combine utils
        self.channel = channel
        self.shapeMap = {}
        self.helGroups = OrderedDict()
        self.sumGroups = OrderedDict()
        self.helMetaGroups = OrderedDict()
        
        # self.templSystematics = systematicsDict
        self.templSystematics = {}

        # load files 
        self.ftempl = h5py.File('../Common/shapesWplus.hdf5', mode='r+')

        self.helXsecs = ['L', 'I', 'T', 'A', 'P','7','8', '9','UL']
        
        self.data = self.ftempl['data_obs'][:]
        self.templ = self.ftempl['template'][:]
        self.templw2 = self.ftempl['template_sumw2'][:]
        self.gen = self.ftempl['helicity'][:]
        self.lowacc = self.ftempl['lowacc'][:]
        self.lowaccw2 = self.ftempl['lowacc_sumw2'][:]
        self.Wtau = self.ftempl['Wtau'][:]
        self.Wtauw2 = self.ftempl['Wtau_sumw2'][:]
        self.DY = self.ftempl['DY'][:]
        print(self.DY.shape)
        self.DYw2 = self.ftempl['DY_sumw2'][:]
        self.Top = self.ftempl['Top'][:]
        self.Topw2 = self.ftempl['Top_sumw2'][:]
        self.Diboson = self.ftempl['Diboson'][:]
        self.Dibosonw2 = self.ftempl['Diboson_sumw2'][:]
        self.fakeslow = self.ftempl['fakesLowMt'][:]
        self.fakesloww2 = self.ftempl['fakesLowMt_sumw2'][:]
        self.fakeshigh = self.ftempl['fakesHighMt'][:]
        self.fakeshighw2 = self.ftempl['fakesHighMt_sumw2'][:]

        # reduce bins to acceptance
        from binning import ptBins, etaBins, mTBins, etaBins, isoBins, chargeBins, yBins, qtBins, cosThetaBins, phiBins
        threshold_y = np.digitize(2.4,yBins)-1
        threshold_qt = np.digitize(60.,qtBins)-1
        self.yBins = np.array(yBins[:threshold_y+1])
        self.qtBins = np.array(qtBins[:threshold_qt+1])
        print(self.yBins,self.qtBins)
        self.yBinsC = 0.5*(self.yBins[1:]+self.yBins[:-1])
        self.qtBinsC = 0.5*(self.qtBins[1:]+self.qtBins[:-1])
        
    def fillProcessList(self):
        for hel in self.helXsecs:
            for i in range(len(self.yBinsC)):
                for j in range(len(self.qtBinsC)):
                    proc = 'helXsecs' + hel + '_y_{}'.format(i)+'_qt_{}'.format(j)
                    self.processes.append(proc)
                    if not "helXsecs7" in proc and not "helXsecs8" in proc and not "helXsecs9" in proc:
                        self.signals.append(proc)
        bkg_list = ["DY","Diboson","Top","fakesLowMt","fakesHighMt", "Wtau","LowAcc"]
        # bkg_list = ["DY","Diboson","Top","Wtau","LowAcc"]

        # bkg_list = []
        self.processes.extend(bkg_list)
    
    def shapeFile(self):
        dtype = 'float64'
        with h5py.File('{}.hdf5'.format(self.channel), mode="w") as f:
            for proc in self.processes:
                if "helXsecs" in proc:
                    coeff = self.helXsecs.index(proc.split('_')[0].replace('helXsecs',''))
                    iY = int(proc.split('_')[2])
                    iQt = int(proc.split('_')[4])
                    dset_templ = f.create_dataset(proc, self.templ[...,iY,iQt,coeff].ravel().shape, dtype=dtype)
                    dset_templ[...] = self.templ[...,iY,iQt,coeff].ravel()
                    dset_templw2 = f.create_dataset(proc+'_sumw2', self.templw2[...,iY,iQt,coeff].ravel().shape, dtype=dtype)
                    dset_templw2[...] = self.templw2[...,iY,iQt,coeff].ravel()

            dset_bkg = f.create_dataset("DY", self.DY.ravel().shape, dtype=dtype)
            dset_bkg[...] = self.DY.ravel()
            dset_bkgw2 = f.create_dataset("DY_sumw2", self.DYw2.ravel().shape, dtype=dtype)
            dset_bkgw2[...] = self.DYw2.ravel()

            dset_bkg = f.create_dataset("Diboson", self.Diboson.ravel().shape, dtype=dtype)
            dset_bkg[...] = self.Diboson.ravel()
            dset_bkgw2 = f.create_dataset("Diboson_sumw2", self.Dibosonw2.ravel().shape, dtype=dtype)
            dset_bkgw2[...] = self.Dibosonw2.ravel()

            dset_bkg = f.create_dataset("Top", self.Top.ravel().shape, dtype=dtype)
            dset_bkg[...] = self.Top.ravel()
            dset_bkgw2 = f.create_dataset("Top_sumw2", self.Topw2.ravel().shape, dtype=dtype)
            dset_bkgw2[...] = self.Topw2.ravel()

            dset_bkg = f.create_dataset("Wtau", self.Wtau.ravel().shape, dtype=dtype)
            dset_bkg[...] = self.Wtau.ravel()
            dset_bkgw2 = f.create_dataset("Wtau_sumw2", self.Wtauw2.ravel().shape, dtype=dtype)
            dset_bkgw2[...] = self.Wtauw2.ravel()

            dset_bkg = f.create_dataset("fakesLowMt", self.fakeslow.ravel().shape, dtype=dtype)
            dset_bkg[...] = self.fakeslow.ravel()
            dset_bkgw2 = f.create_dataset("fakesLowMt_sumw2", self.fakesloww2.ravel().shape, dtype=dtype)
            dset_bkgw2[...] = self.fakesloww2.ravel()

            dset_bkg = f.create_dataset("fakesHighMt", self.fakeshigh.ravel().shape, dtype=dtype)
            dset_bkg[...] = self.fakeshigh.ravel()
            dset_bkgw2 = f.create_dataset("fakesHighMt_sumw2", self.fakeshighw2.ravel().shape, dtype=dtype)
            dset_bkgw2[...] = self.fakeshighw2.ravel()

            dset_bkg = f.create_dataset("LowAcc", self.lowacc.ravel().shape, dtype=dtype)
            dset_bkg[...] = self.lowacc.ravel()
            dset_bkgw2 = f.create_dataset("LowAcc_sumw2", self.lowacc.ravel().shape, dtype=dtype)
            dset_bkgw2[...] = self.lowaccw2.ravel()
                    
            # placeholder for data
            dset_data = f.create_dataset('data_obs', self.data.ravel().shape, dtype=dtype)
            dset_data[...] = self.data.ravel()
    
            # copy fakes nuisances in shape file
            for type in ["Up","Down"]:
                for i in range(48*30):
                    histo = self.ftempl['fakesLowMt_fakeNormLowMtBin{}{}'.format(i,type)][:]
                    dset = f.create_dataset(name='fakesLowMt_fakeNormLowMtBin{}{}'.format(i,type), shape=histo.ravel().shape, dtype='float64')
                    dset[...] = histo.ravel()

                    histo = self.ftempl['fakesHighMt_fakeNormHighMtBin{}{}'.format(i,type)][:]
                    dset = f.create_dataset(name='fakesHighMt_fakeNormHighMtBin{}{}'.format(i,type), shape=histo.ravel().shape, dtype='float64')
                    dset[...] = histo.ravel()

                    histo = self.ftempl['fakesLowMt_fakeShapeBin{}{}'.format(i,type)][:]
                    dset = f.create_dataset(name='fakesLowMt_fakeShapeBin{}{}'.format(i,type), shape=histo.ravel().shape, dtype='float64')
                    dset[...] = histo.ravel()

                    histo = self.ftempl['fakesHighMt_fakeShapeBin{}{}'.format(i,type)][:]
                    dset = f.create_dataset(name='fakesHighMt_fakeShapeBin{}{}'.format(i,type), shape=histo.ravel().shape, dtype='float64')
                    dset[...] = histo.ravel()
                    pass

    def maskedChannels(self):
        dtype = 'float64'
        with h5py.File('{}_xsec.hdf5'.format(self.channel), mode="w") as f:
            for proc in self.processes:
                if "helXsecs" in proc: #give the correct xsec to unfold
                    coeff = self.helXsecs.index(proc.split('_')[0].replace('helXsecs',''))
                    iY = int(proc.split('_')[2])
                    iQt = int(proc.split('_')[4])
                    dset_masked = f.create_dataset(proc, [1], dtype=dtype)
                    dset_masked[...] = self.gen[iY,iQt,coeff]
                else:
                    dset_masked = f.create_dataset(proc, [1], dtype=dtype)
                    dset_masked[...] = 0.
            dset_masked = f.create_dataset("data_obs", [1], dtype=dtype)
            dset_masked[...] = 0.

    def setPreconditionVec(self):
        f=h5py.File('fitresults_asimov.hdf5', 'r+')
        hessian = f['hess'][:]
        eig, U = np.linalg.eigh(hessian)
        M1 = np.matmul(np.diag(1./np.sqrt(eig)),U.T)
        M2 = np.linalg.inv(np.linalg.inv(M1))
        # print(M1,np.linalg.inv(np.linalg.inv(M1)))
        self.preconditioner = M1
        self.invpreconditioner = np.linalg.inv(self.preconditioner)
        # print(np.matmul(self.preconditioner,np.linalg.inv(self.preconditioner)))
        # test = np.matmul(self.preconditioner,np.linalg.inv(self.preconditioner)) - np.identity(M1.shape[0])
        # print(np.max(np.abs(test)))
        # self.preconditioner = np.identity(len(self.signals))
        # self.invpreconditioner = np.identity(len(self.signals))

    def fillHelGroup(self):

        for i in range(len(self.yBinsC)):
            for j in range(len(self.qtBinsC)):

                s = 'y_{i}_qt_{j}'.format(i=i,j=j)
                self.helGroups[s] = []
                
                for hel in self.helXsecs:
                    if 'helXsecs'+hel+'_'+s in self.signals:

                        self.helGroups[s].append('helXsecs'+hel+'_'+s)
                                
                if self.helGroups[s] == []:
                    del self.helGroups[s]
    def fillHelMetaGroup(self):

        for i in range(len(self.yBinsC)):
            s = 'y_{i}'.format(i=i)
            self.helMetaGroups[s] = []
            for key in self.sumGroups:
                if s in key:
                    self.helMetaGroups[s].append(key)
            
            if self.helMetaGroups[s] == []:
                    del self.helMetaGroups[s]
        
        for j in range(len(self.qtBinsC)):
            s = 'qt_{j}'.format(j=j)
            self.helMetaGroups[s] = []
            for key in self.sumGroups:
                if 'qt' in key and key.split('_')[2]==str(j):
                    self.helMetaGroups[s].append(key)
        
            if self.helMetaGroups[s] == []:
                    del self.helMetaGroups[s]
        # print self.helMetaGroups
    def fillSumGroup(self):

        for i in range(len(self.yBinsC)):
            s = 'y_{i}'.format(i=i)
            for hel in self.helXsecs:
                for signal in self.signals:
                    if 'helXsecs'+hel+'_'+s in signal:
                        self.sumGroups['helXsecs'+hel+'_'+s] = []
                        for j in range(len(self.qtBinsC)):
                            if 'helXsecs'+hel+'_'+'y_{i}_qt_{j}'.format(i=i,j=j) in self.signals:
                                self.sumGroups['helXsecs'+hel+'_'+s].append('helXsecs'+hel+'_'+s+'_qt_{j}'.format(j=j))
        
        for j in range(len(self.qtBinsC)):
            s = 'qt_{j}'.format(j=j)
            for hel in self.helXsecs:
                for signal in self.signals:
                    if signal.split('_')[0] == 'helXsecs'+hel and signal.split('_')[4] == str(j):
                        self.sumGroups['helXsecs'+hel+'_'+s] = []
                        for i in range(len(self.yBinsC)):
                            if 'helXsecs'+hel+'_'+'y_{i}_qt_{j}'.format(i=i,j=j) in self.signals:
                            #print i, signal, 'helXsecs'+hel+'_'+'y_{i}_pt_{j}'.format(i=i,j=j)
                            #print 'append', 'helXsecs'+hel+'_y_{i}_'.format(i=i)+s, 'to', 'helXsecs'+hel+'_'+s
                                self.sumGroups['helXsecs'+hel+'_'+s].append('helXsecs'+hel+'_y_{i}_'.format(i=i)+s)
    def makeDatacard(self):

        self.DC = Datacard()

        ############## Setup the datacard (must be filled in) ###########################

        self.DC.bins =   [self.channel, self.channel+'_xsec'] # <type 'list'>
        self.DC.obs =    {} # <type 'dict'>
        self.DC.processes =  self.processes # <type 'list'>
        self.DC.signals =    self.signals # <type 'list'>
        self.DC.isSignal =   {} # <type 'dict'>
        for proc in self.processes:
            if proc in self.signals:
                self.DC.isSignal[proc] = True
            else:
                self.DC.isSignal[proc] = False
        self.DC.keyline = [] # <type 'list'> # not used by combine-tf
        self.DC.exp =    {} # <type 'dict'>
        self.DC.exp[self.channel] = {}
        self.DC.exp[self.channel+'_xsec'] = {}
        for proc in self.processes:
            self.DC.exp[self.channel][proc] = -1.00
            self.DC.exp[self.channel+'_xsec'][proc] = -1.00
        self.DC.systs =  [] # <type 'list'>
        aux = {} #each sys will have a separate aux dict
        aux[self.channel] = {}
        aux[self.channel+'_xsec'] = {}
        for i in range(48*30):
            for proc in self.processes:
                aux[self.channel][proc] = 0.
                aux[self.channel+'_xsec'][proc] = 0.
            aux[self.channel]['fakesLowMt'] = 1.
            aux[self.channel]['fakesHighMt'] = 1.
            self.DC.systs.append(('fakeShapeBin{}'.format(i), False, 'shapeNoConstraint', [], aux))
        aux = {} #each sys will have a separate aux dict
        aux[self.channel] = {}
        aux[self.channel+'_xsec'] = {}
        for proc in self.processes:
                aux[self.channel][proc] = 0.
                aux[self.channel+'_xsec'][proc] = 0.
        aux[self.channel]['fakesLowMt'] = 1.5
        aux[self.channel]['fakesHighMt'] = 0
        self.DC.systs.append(('fakesNormLowMt', False, 'lnNNoConstraint', [], aux))
        aux = {} #each sys will have a separate aux dict
        aux[self.channel] = {}
        aux[self.channel+'_xsec'] = {}
        for proc in self.processes:
                aux[self.channel][proc] = 0.
                aux[self.channel+'_xsec'][proc] = 0.
        aux[self.channel]['fakesLowMt'] = 0.
        aux[self.channel]['fakesHighMt'] = 1.5
        self.DC.systs.append(('fakesNormHighMt', False, 'lnNNoConstraint', [], aux))
        # aux = {} #each sys will have a separate aux dict
        # aux[self.channel] = {}
        # aux[self.channel+'_xsec'] = {}
        # for i in range(48*30):
        #     for proc in self.processes:
        #         aux[self.channel][proc] = 0.
        #         aux[self.channel+'_xsec'][proc] = 0.
        #     aux[self.channel]['fakesLowMt'] = 1.
        #     aux[self.channel]['fakesHighMt'] = 0.
        #     self.DC.systs.append(('fakeNormLowMtBin{}'.format(i), False, 'shapeNoConstraint', [], aux))
        # aux = {} #each sys will have a separate aux dict
        # aux[self.channel] = {}
        # aux[self.channel+'_xsec'] = {}
        # for i in range(48*30):
        #     for proc in self.processes:
        #         aux[self.channel][proc] = 0.
        #         aux[self.channel+'_xsec'][proc] = 0.
        #     aux[self.channel]['fakesLowMt'] = 0.
        #     aux[self.channel]['fakesHighMt'] = 1.
        #     self.DC.systs.append(('fakeNormHighMtBin{}'.format(i), False, 'shapeNoConstraint', [], aux))
        # list of [{bin : {process : [input file, path to shape, path to shape for uncertainty]}}]
        if self.doSyst:
            for syst in self.templSystematics: #loop over systematics
                if 'Nominal' in syst: continue
                for var in self.templSystematics[syst]["vars"]:
                    aux = {} #each sys will have a separate aux dict
                    aux[self.channel] = {}
                    aux[self.channel+'_xsec'] = {}
                    for proc in self.processes: 
                        if proc in self.templSystematics[syst]["procs"]:
                            aux[self.channel][proc] = 1.0
                            aux[self.channel+'_xsec'][proc] = 0.0
                        else:
                            if "Signal" in self.templSystematics[syst]["procs"] and "hel" in proc:
                                aux[self.channel][proc] = 1.0
                                aux[self.channel+'_xsec'][proc] = 0.0
                            else:
                                aux[self.channel][proc] = 0.0
                                aux[self.channel+'_xsec'][proc] = 0.0

                    self.DC.systs.append((var, False, self.templSystematics[syst]["type"], [], aux))
        self.DC.groups = {}
        # self.DC.groups = {'mass': ['mass']} 
        #                  'pdfs': set(['LHEPdfWeightHess{}'.format(i+1) for i in range(60)]+['alphaS']),
        #                 'WHSFStat': set(["WHSFSyst0Eta{}".format(i) for i in range(1, 49)]+["WHSFSyst1Eta{}".format(i) for i in range(1, 49)]+["WHSFSyst2Eta{}".format(i) for i in range(1, 49)]),
        #                  'WHSFSyst': ['WHSFSystFlat'],
        #                  'ptScale': set(["Eta{}zptsyst".format(j) for j in range(1, 5)] + ["Eta{}Ewksyst".format(j) for j in range(1, 5)] + ["Eta{}deltaMsyst".format(j) for j in range(1, 5)]+["Eta{}stateig{}".format(j, i) for i in range(0, 99) for j in range(1, 5)]),
        #                  'jme': set(['jesTotal', 'unclustEn']),
        #                  'PrefireWeight':['PrefireWeight'],
        #                  }  # <type 'dict'>
        
        self.DC.shapeMap = 	{self.channel: {'*': [self.channel+'.root', '$PROCESS', '$PROCESS_$SYSTEMATIC']},\
        self.channel+'_xsec': {'*': [self.channel+'_xsec.root', '$PROCESS', '$PROCESS_$SYSTEMATIC']}} # <type 'dict'>
        self.DC.hasShapes =  True # <type 'bool'>
        self.DC.flatParamNuisances =  {} # <type 'dict'>
        self.DC.rateParams =  {} # <type 'dict'>
        self.DC.extArgs =    {} # <type 'dict'>
        self.DC.rateParamsOrder  =  set([]) # <type 'set'>
        self.DC.frozenNuisances  =  set([]) # <type 'set'>
        self.DC.systematicsShapeMap =  {} # <type 'dict'>
        self.DC.nuisanceEditLines    =  [] # <type 'list'>
        self.DC.discretes    =  [] # <type 'list'>
        self.DC.helGroups = self.helGroups
        self.DC.sumGroups = self.sumGroups
        self.DC.helMetaGroups = self.helMetaGroups
        # self.DC.noiGroups = {'mass':['mass']}
        self.DC.noiGroups = {}

        self.DC.preconditioner  = self.preconditioner 
        self.DC.invpreconditioner  = self.invpreconditioner 
        
        filehandler = open('{}.pkl'.format(self.channel), 'w')
        pickle.dump(self.DC, filehandler)
