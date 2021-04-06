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
        self.poly1DRegGroups = OrderedDict()
        self.poly2DRegGroups = OrderedDict()
        
        # self.templSystematics = systematicsDict
        self.templSystematics = {}

        # load files 
        self.ftempl = h5py.File('../templateMaker/templates.hdf5', mode='r+')

        self.helXsecs = ['L', 'I', 'T', 'A', 'P','7','8', '9','UL']
        
        self.templ = self.ftempl['templates'][:]
        self.templw2 = self.ftempl['templates_sumw2'][:]
        self.gen = self.ftempl['helicity'][:]
        self.lowacc = self.ftempl['lowacc'][:]
        self.lowaccw2 = self.ftempl['lowacc_sumw2'][:]

        # reduce bins to acceptance
        from binning import ptBins, etaBins, mTBins, etaBins, isoBins, chargeBins, yBins, qtBins, cosThetaBins, phiBins
        threshold_y = np.digitize(2.4,yBins)
        threshold_qt = np.digitize(32.,qtBins)
        self.yBins = np.array(yBins[:threshold_y])
        self.qtBins = np.array(qtBins[:threshold_qt])
        print(self.yBins,self.qtBins)
        self.yBinsC = 0.5*(self.yBins[1:]+self.yBins[:-1])
        self.qtBinsC = 0.5*(self.qtBins[1:]+self.qtBins[:-1])

        # self.gen[0,...]+=self.gen[-1,...]/6.
        # self.gen[1,...]+=self.gen[-1,...]/6.
        # self.gen[2,...]+=self.gen[-1,...]/6.
        # self.gen[3,...]+=self.gen[-1,...]/6.
        # self.gen[4,...]+=self.gen[-1,...]/6.
        # self.gen[-1,...]/=6.
        
        # import matplotlib.pyplot as plt
        # import mplhep as hep
        # for i in range(self.gen.shape[0]):
        #     fig, ax1 = plt.subplots()
        #     ax1.set_title("A{}".format(i), fontsize=18)
        #     hep.hist2dplot(self.gen[i,...],self.yBins,self.qtBins)
        #     plt.tight_layout()
        #     plt.savefig("A{}".format(i))
        #     plt.clf()

        # rescale to make templates positive defined

        # self.templ[0,...]+=self.templ[-1,...]/6.
        # self.templ[1,...]+=self.templ[-1,...]/6.
        # self.templ[2,...]+=self.templ[-1,...]/6.
        # self.templ[3,...]+=self.templ[-1,...]/6.
        # self.templ[4,...]+=self.templ[-1,...]/6.
        # self.templ[-1,...]/=6.

        # self.templw2[0,...]+=self.templw2[-1,...]/6.
        # self.templw2[1,...]+=self.templw2[-1,...]/6.
        # self.templw2[2,...]+=self.templw2[-1,...]/6.
        # self.templw2[3,...]+=self.templw2[-1,...]/6.
        # self.templw2[4,...]+=self.templw2[-1,...]/6.
        # self.templw2[-1,...]/=6.

        # import matplotlib.pyplot as plt
        # import mplhep as hep
        # for i in range(self.gen.shape[0]):
        #     fig, ax1 = plt.subplots()
        #     ax1.set_title("templ{}".format(i), fontsize=18)
        #     hep.hist2dplot(self.templ[i,0,2,...],etaBins,ptBins)
        #     plt.tight_layout()
        #     plt.savefig("templ{}".format(i))
        #     plt.clf()
        
    def fillProcessList(self):
        for hel in self.helXsecs:
            for i in range(len(self.yBinsC)):
                for j in range(len(self.qtBinsC)):
                    proc = 'helXsecs' + hel + '_y_{}'.format(i)+'_qt_{}'.format(j)
                    self.processes.append(proc)
                    if not "helXsecs7" in proc and not "helXsecs8" in proc and not "helXsecs9" in proc:
                        self.signals.append(proc)
        #bkg_list = ["DY","Diboson","Top","Fake","Tau","LowAcc"]
        bkg_list = []
        self.processes.extend(bkg_list)
    
    def shapeFile(self):
        dtype = 'float64'
        with h5py.File('{}.hdf5'.format(self.channel), mode="w") as f:
            for proc in self.processes:
                if not 'lowacc' in proc:
                    coeff = self.helXsecs.index(proc.split('_')[0].replace('helXsecs',''))
                    iY = int(proc.split('_')[2])
                    iQt = int(proc.split('_')[4])
                    dset_templ = f.create_dataset(proc, self.templ[coeff,iY,iQt,:,:].ravel().shape, dtype=dtype)
                    dset_templ[...] = self.templ[coeff,iY,iQt,:,:].ravel()
                    dset_templw2 = f.create_dataset(proc+'_sumw2', self.templw2[coeff,iY,iQt,:,:].ravel().shape, dtype=dtype)
                    dset_templw2[...] = self.templw2[coeff,iY,iQt,:,:].ravel()
                else:
                    dset_bkg = f.create_dataset(proc, self.lowacc.ravel().shape, dtype=dtype)
                    dset_bkg[...] = self.lowacc.ravel()
                    dset_bkgw2 = f.create_dataset(proc+'_sumw2', self.lowacc.ravel().shape, dtype=dtype)
                    dset_bkgw2[...] = self.lowacc.ravel()
            # placeholder for data
            dset_data = f.create_dataset('data_obs', self.templ[0,0,0,:,:].ravel().shape, dtype=dtype)
            dset_data[...] = self.templ[0,0,0,:,:].ravel()
    
    def maskedChannels(self):
        dtype = 'float64'
        with h5py.File('{}_xsec.hdf5'.format(self.channel), mode="w") as f:
            for proc in self.processes:
                if not 'lowacc' in proc: #give the correct xsec to unfold
                    coeff = self.helXsecs.index(proc.split('_')[0].replace('helXsecs',''))
                    iY = int(proc.split('_')[2])
                    iQt = int(proc.split('_')[4])
                    dset_masked = f.create_dataset(proc, [1], dtype=dtype)
                    dset_masked[...] = self.gen[coeff,iY,iQt]
                else:
                    dset_masked = f.create_dataset(proc, [1], dtype=dtype)
                    dset_masked[...] = 0.

    def setPreconditionVec(self):
        self.fout = ROOT.TFile.Open('fit_Wplus_asimov.root')
        fitresults = self.fout.Get('fitresults')

        helXsecs_red = ['L', 'I', 'T', 'A', 'P','UL']

        # self.precVec = np.zeros((6,self.gen.shape[1],self.gen.shape[2]))
        # for h,hel in enumerate(helXsecs_red):
        #     for ev in fitresults: #dummy because there's one event only
        #         for i in range(len(self.yBinsC)):
        #             for j in range(len(self.qtBinsC)):
        #                 try:
        #                     coeff_err = eval('ev.helXsecs{hel}_y_{i}_qt_{j}_mu_err'.format(hel=hel, j=j, i=i))
        #                     self.precVec[h,i,j]=coeff_err
        #                 except AttributeError:
        #                     pass
        # self.precVec = self.precVec.ravel()
        f=h5py.File('fitresults_asimov.hdf5', 'r+')
        hessian = f['hess'][:]
        eig, U = np.linalg.eigh(hessian)
        M1 = np.matmul(np.diag(1./np.sqrt(eig)),U.T)
        self.preconditioner = M1
        self.invpreconditioner = np.linalg.inv(self.preconditioner)
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
        ## list of [{bin : {process : [input file, path to shape, path to shape for uncertainty]}}]
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

        coeff = [0,1,2]
        for j in coeff:
            testnames = []
            for i in range(len(self.yBinsC)):
                testnames.append("y_{}_helmeta_A{}".format(i,j))

            etas = [0.2, 0.6, 1.0, 1.4, 1.8, 2.2]

            # self.poly1DRegGroups["poly1dyA{}".format(j)] = {"names": testnames, "bincenters": etas, "firstorder": 0, "lastorder": 2}

            testnames = []
            for i in range(len(self.qtBinsC)):
                testnames.append("qt_{}_helmeta_A{}".format(i, j))

            pts = [2., 6., 10., 14., 18., 22., 26., 30.]
            
            # self.poly1DRegGroups["poly1dqtA{}".format(j)] = {"names": testnames, "bincenters": pts, "firstorder": 0, "lastorder": 3}

        coeff = [3, 4]
        for j in coeff:
            testnames = []
            for i in range(len(self.yBinsC)):
                testnames.append("y_{}_helmeta_A{}".format(i, j))

            etas = [0.2, 0.6, 1.0, 1.4, 1.8, 2.2]
            
            # self.poly1DRegGroups["poly1dyA{}".format(j)] = {"names": testnames, "bincenters": etas, "firstorder": 1, "lastorder": 2}
        
        coeff = [1, 3]
        for j in coeff:
            testnames = []
            for i in range(len(self.qtBinsC)):
                testnames.append("qt_{}_helmeta_A{}".format(i, j))

            pts = [2., 6., 10., 14., 18., 22., 26., 30.]
            
            # self.poly1DRegGroups["poly1dqtA{}".format(j)] = {"names": testnames, "bincenters": pts, "firstorder": 0, "lastorder": 3}

        testnames = []
        for i in range(len(self.qtBinsC)):
            testnames.append("qt_{}_helmeta_A4".format(i))

        pts = [2., 6., 10., 14., 18., 22., 26., 30.]
        
        # self.poly1DRegGroups["poly1dqtA4"] = {"names": testnames, "bincenters": pts, "firstorder": 0, "lastorder": 3}
        
        self.DC.poly1DRegGroups = self.poly1DRegGroups

        #etas = np.array([0.2/2.4, 0.6/2.4, 1.0/2.4, 1.4/2.4, 1.8/2.4, 2.2/2.4])
        #pts = np.array([2./32., 6./32., 10./32., 14./32., 18./32., 22./32., 26./32., 30./32.])
        etas = np.array([0.2, 0.6, 1.0, 1.4, 1.8, 2.2])
        pts = np.array([2., 6., 10., 14., 18., 22., 26., 30.])

        #etas = etas/2.4
        #pts = pts/32.
        
        #### A0
        testnames = []
        bincenters = []
        for i in range(6):
            for j in range(8):
                testnames.append("y_%i_qt_%i_A0" % (i, j))
                bincenters.append([etas[i], pts[j]])

        # self.poly2DRegGroups["poly2dA0"] = {"names": testnames, "bincenters": bincenters, "firstorder": (0, 0), "lastorder": (5, 7), "fullorder": (5, 7)}
        self.poly2DRegGroups["poly2dA0"] = {"names": testnames, "bincenters": bincenters, "firstorder": (0, 2), "lastorder": (4, 4), "fullorder": (5, 7)}
        #### A1
        testnames = []
        bincenters = []
        for i in range(6):
            for j in range(8):
                testnames.append("y_%i_qt_%i_A1" % (i, j))
                bincenters.append([etas[i], pts[j]])

        # self.poly2DRegGroups["poly2dA1"] = {"names": testnames, "bincenters": bincenters, "firstorder": (0, 0), "lastorder": (5, 7), "fullorder": (5, 7)} 
        self.poly2DRegGroups["poly2dA1"] = {"names": testnames, "bincenters": bincenters, "firstorder": (1, 1), "lastorder": (3, 3), "fullorder": (5, 7)}
        
        #### A2
        testnames = []
        bincenters = []
        for i in range(6):
            for j in range(8):
                testnames.append("y_%i_qt_%i_A2" % (i, j))
                bincenters.append([etas[i], pts[j]])

        # self.poly2DRegGroups["poly2dA2"] = {"names": testnames, "bincenters": bincenters, "firstorder": (0, 0), "lastorder": (5, 7), "fullorder": (5, 7)} 
        self.poly2DRegGroups["poly2dA2"] = {"names": testnames, "bincenters": bincenters, "firstorder": (0, 2), "lastorder": (2, 4), "fullorder": (5, 7)}

        #### A3
        testnames = []
        bincenters = []
        for i in range(6):
            for j in range(8):
                testnames.append("y_%i_qt_%i_A3" % (i, j))
                bincenters.append([etas[i], pts[j]])

        # self.poly2DRegGroups["poly2dA3"] = {"names": testnames, "bincenters": bincenters, "firstorder": (0, 0), "lastorder": (5, 7), "fullorder": (5, 7)} 
        self.poly2DRegGroups["poly2dA3"] = {"names": testnames, "bincenters": bincenters, "firstorder": (0, 1), "lastorder": (2, 4), "fullorder": (5, 7)}

        #### A4
        testnames = []
        bincenters = []
        for i in range(6):
            for j in range(8):
                testnames.append("y_%i_qt_%i_A4" % (i, j))
                bincenters.append([etas[i], pts[j]])

        # self.poly2DRegGroups["poly2dA4"] = {"names": testnames, "bincenters": bincenters, "firstorder": (0, 0), "lastorder": (5, 7), "fullorder": (5, 7)} 
        self.poly2DRegGroups["poly2dA4"] = {"names": testnames, "bincenters": bincenters, "firstorder": (1, 0), "lastorder": (3, 4), "fullorder": (5, 7)}
        
        #### UL
        testnames = []
        bincenters = []
        for i in range(6):
            for j in range(8):
                testnames.append("y_%i_qt_%i_unpolarizedxsec" % (i, j))
                bincenters.append([etas[i], pts[j]])

        self.poly2DRegGroups["poly2dunpolarizedxsec"] = {"names": testnames, "bincenters": bincenters, "firstorder": (0, 0), "lastorder": (5, 7), "fullorder": (5, 7)} 

        self.DC.poly2DRegGroups = self.poly2DRegGroups

        self.DC.preconditioner  = self.preconditioner 
        self.DC.invpreconditioner  = self.invpreconditioner 
        
        filehandler = open('{}.pkl'.format(self.channel), 'w')
        pickle.dump(self.DC, filehandler)
