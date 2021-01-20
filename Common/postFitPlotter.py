import ROOT
import os
import sys
import h5py
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
sys.path.append('data/')
from binning import ptBins, etaBins, mTBins, isoBins, chargeBins

plt.style.use([hep.style.ROOT])
# hep.cms.label(loc=0, year=2016, lumi=35.9, data=True)

fIn = ROOT.TFile.Open('../Fit/fitbkgWplus.root')
data = fIn.Get('obs')
hdata = np.array(data)[1:-1].reshape((len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1))

types = ['prefit', 'postfit']
for type in types:
    ewk = fIn.Get('expproc_ewk_{}'.format(type))
    hewk = np.array(ewk)[1:-1].reshape((len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1))
    fakesLowMt = fIn.Get('expproc_fakesLowMt_{}'.format(type))
    hfakesLowMt = np.array(fakesLowMt)[1:-1].reshape((len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1))
    hfakesLowMt_err=np.array([fakesLowMt.GetSumw2()[i] for i in range(fakesLowMt.GetSumw2().GetSize())])[1:-1].reshape((len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1))
    fakesHighMt = fIn.Get('expproc_fakesHighMt_{}'.format(type))
    hfakesHighMt = np.array(fakesHighMt)[1:-1].reshape((len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1))
    hfakesHighMt_err=np.array([fakesHighMt.GetSumw2()[i] for i in range(fakesHighMt.GetSumw2().GetSize())])[1:-1].reshape((len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1))

    for i in range(2):
        fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
        ax1.set_title("eta_iso{}_highMt_{}".format(i,type), fontsize=18)
        ax1.set_ylabel('number of events')
        ax2.set_ylabel('data/prediction')
        ax2.set_xlabel('muon $\eta$')
        etadata = np.sum(hdata,axis=1)[:,-1,i]
        etaewk = np.sum(hewk,axis=1)[:,-1,i]
        etafake = np.sum(hfakesHighMt,axis=1)[:,-1,i]
        etaerr = np.sqrt(np.sum(hfakesHighMt_err,axis=1)[:,-1,i]) * etadata/np.square(etafake+etaewk)
        hep.histplot([etadata],bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
        hep.histplot([etafake,etaewk],bins = etaBins, histtype = 'fill',linestyle = 'solid', color =["g","r"], label=["fakes", "ewk"], stack = True, ax=ax1)
        ax2.set_ylim([0.9, 1.1])
        hep.histplot([etadata/(etafake+etaewk)], yerr = etaerr, bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
        ax1.legend(loc='upper right', frameon=True)

        plt.savefig('eta_iso{}_highMt_{}.png'.format(i,type))
        plt.cla()

        fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
        ax1.set_title("pt_iso{}_highMt_{}".format(i,type), fontsize=18)
        ax1.set_ylabel('number of events')
        ax2.set_ylabel('data/prediction')
        ax2.set_xlabel('muon $p_T$')
        ptdata = np.sum(hdata,axis=0)[:,-1,i]
        ptewk = np.sum(hewk,axis=0)[:,-1,i]
        ptfake = np.sum(hfakesHighMt,axis=0)[:,-1,i]

        hep.histplot([ptdata],bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1,label = ["data"])
        hep.histplot([ptfake,ptewk],bins = ptBins, histtype = 'fill',linestyle = 'solid', color =["g","r"], label=["fakes", "ewk"], stack = True, ax=ax1)
        ax2.set_ylim([0.9, 1.1])
        hep.histplot([ptdata/(ptfake+ptewk)],bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
        ax1.legend(loc='upper right', frameon=True)

        plt.savefig('pt_iso{}_highMt_{}.png'.format(i,type))
        plt.cla()

        fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
        ax1.set_title("eta_iso{}_lowMt_{}".format(i,type), fontsize=18)
        ax1.set_ylabel('number of events')
        ax2.set_ylabel('data/prediction')
        ax2.set_xlabel('muon $\eta$')
        etadata = np.sum(hdata,axis=1)[:,0,i]
        etaewk = np.sum(hewk,axis=1)[:,0,i]
        etafake = np.sum(hfakesLowMt,axis=1)[:,0,i]

        hep.histplot([etadata],bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1,label = ["data"])
        hep.histplot([etafake,etaewk],bins = etaBins, histtype = 'fill',linestyle = 'solid', color =["g","r"], label=["fakes", "ewk"], stack = True, ax=ax1)
        ax2.set_ylim([0.9, 1.1])
        hep.histplot([etadata/(etafake+etaewk)],bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
        ax1.legend(loc='upper right', frameon=True)

        plt.savefig('eta_iso{}_lowMt_{}.png'.format(i,type))
        plt.cla()

        fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
        ax1.set_title("pt_iso{}_lowMt_{}".format(i,type), fontsize=18)
        ax1.set_ylabel('number of events')
        ax2.set_ylabel('data/prediction')
        ax2.set_xlabel('muon $p_T$')
        ptdata = np.sum(hdata,axis=0)[:,0,i]
        ptewk = np.sum(hewk,axis=0)[:,0,i]
        ptfake = np.sum(hfakesLowMt,axis=0)[:,0,i]

        hep.histplot([ptdata],bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1,label = ["data"])
        hep.histplot([ptfake,ptewk],bins = ptBins, histtype = 'fill',linestyle = 'solid', color =["g","r"], label=["fakes", "ewk"], stack = True, ax=ax1)
        ax2.set_ylim([0.9, 1.1])
        hep.histplot([ptdata/(ptfake+ptewk)],bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
        ax1.legend(loc='upper right', frameon=True)

        plt.savefig('pt_iso{}_lowMt_{}.png'.format(i,type))
        plt.cla()