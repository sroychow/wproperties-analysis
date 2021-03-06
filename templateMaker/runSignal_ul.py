import os
import sys
import ROOT
import copy
import time
import h5py
from math import pi
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from array import array
sys.path.append('../RDFprocessor/framework')
sys.path.append('../Common/data')
from RDFtree import RDFtree
sys.path.append('python/')
from getLumiWeight import getLumiWeight
from binning import ptBins, etaBins, mTBins, etaBins, isoBins, chargeBins, yBins, qtBins, cosThetaBins, phiBins
from externals import filePt, fileY, fileSF

# matplotlib stuff
plt.style.use([hep.style.ROOT])
hep.cms.label(loc=0, year=2016, lumi=35.9, data=True)
hep.cms.text('Simulation')

ROOT.gSystem.Load('bin/libAnalysisOnData.so')

ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")

ROOT.ROOT.EnableImplicitMT(48)

outputDir = 'PLOTS'
inputFile = '/scratchnvme/wmass/NanoAOD2016-UL/postNanoDec2020/WplusJetsToMuNu_preVFP_addVars/merged/*.root'

p = RDFtree(outputDir = outputDir, inputFile = inputFile, outputFile="test.root", pretend=False)
p.branch(nodeToStart='input', nodeToEnd='defs', modules=[ROOT.lumiWeight(xsec=11572.19, sumwclipped=5895447715506.5, targetLumi = 35.9), ROOT.customizeforUL(True,True), ROOT.genDefinitions(), ROOT.defineHarmonics(),ROOT.recoDefinitions()])
p.Histogram(columns = ["Wrap_preFSR_abs","Vpt_preFSR","CStheta_preFSR","CSphi_preFSR","lumiweight"], types = ['float']*5,node='defs',histoname=ROOT.string("xsecs"), bins = [yBins,qtBins,cosThetaBins,phiBins])
p.gethdf5Output()


fewk = h5py.File('PLOTS/test.hdf5', mode='r+')
h = np.array(fewk['xsecs'][:].reshape((len(yBins)-1,len(qtBins)-1, len(cosThetaBins)-1, len(phiBins)-1),order='F'),order='C')

fig, ax1 = plt.subplots()
ax1.set_title("CS theta", fontsize=18)
ax1.set_ylabel('Events')
ax1.set_xlabel('CS $\theta$')
data = np.sum(h,axis=(0,1,3))
hep.histplot([data],bins = cosThetaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1)
plt.savefig('CStheta.png')
plt.cla()

fig, ax1 = plt.subplots()
ax1.set_title("CS phi", fontsize=18)
ax1.set_ylabel('Events')
ax1.set_xlabel('CS $\phi$')
data = np.sum(h,axis=(0,1,2))
hep.histplot([data],bins = phiBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1)
plt.savefig('CSphi.png')
plt.cla()

# pick the right harmonics and reweight
cosThetaBins = np.asarray(cosThetaBins)
cosThetaBinsC = 0.5*(cosThetaBins[1:]+cosThetaBins[:-1])
phiBins = np.asarray(phiBins)
phiBinsC = 0.5*(phiBins[1:]+phiBins[:-1])

P0w = np.outer(1. / 2. * (1. - 3. * cosThetaBinsC * cosThetaBinsC),np.ones(len(phiBinsC)))
P1w = np.outer(2. * cosThetaBinsC * np.sqrt(1. - cosThetaBinsC * cosThetaBinsC),np.cos(phiBinsC))
P2w = np.outer(1. / 2. * (1. - cosThetaBinsC * cosThetaBinsC),np.cos(2. * phiBinsC))
P3w = np.outer(np.sqrt(1. - cosThetaBinsC * cosThetaBinsC),np.cos(phiBinsC))
P4w = np.outer(cosThetaBinsC,np.ones(len(phiBinsC)))
P5w = np.outer((1. - cosThetaBinsC * cosThetaBinsC),np.sin(2. * phiBinsC))
P6w = np.outer(2. * cosThetaBinsC * np.sqrt(1. - cosThetaBinsC * cosThetaBinsC),np.sin(phiBinsC))
P7w = np.outer(np.sqrt(1. - cosThetaBinsC * cosThetaBinsC),np.sin(phiBinsC))
P8w = np.outer(1 + cosThetaBinsC * cosThetaBinsC,np.ones(len(phiBinsC)))

wharmonics = [P0w,P1w,P2w,P3w,P4w,P5w,P6w,P7w]
hharmonics = []
totalxsec = np.sum(h,axis=(2,3))
factors = [(20./3., 1./10),(5.,0.),(20.,0.),(4.,0.),(4.,0.),(5.,0.),(5.,0.),(4.,0.)]
for i,hw in enumerate(wharmonics):
    htmp = np.einsum('ijkm,km->ij',h,hw)/totalxsec
    htmp = factors[i][0]*(htmp+factors[i][1])
    hharmonics.append(htmp)
    fig, ax1 = plt.subplots()
    ax1.set_title("A{}".format(i), fontsize=18)
    hep.hist2dplot(htmp,yBins,qtBins)
    plt.savefig("A{}".format(i))
    plt.cla()

# reprocess with acceptance cuts
p2 = RDFtree(outputDir = outputDir, inputFile = inputFile, outputFile="templates.root", pretend=False)
p2.branch(nodeToStart='input', nodeToEnd='defs', modules=[ROOT.lumiWeight(xsec=11572.19, sumwclipped=5895447715506.5, targetLumi = 35.9), ROOT.customizeforUL(True,True), ROOT.genDefinitions(), ROOT.defineHarmonics(),ROOT.recoDefinitions()])
p2.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Idx_mu1>0", filtername="{:20s}".format("Vtype selection"))
p2.Histogram(columns = ["Wrap_preFSR_abs","Vpt_preFSR","CStheta_preFSR","CSphi_preFSR","Mu1_eta", "Mu1_pt","lumiweight"], types = ['float']*7,node='defs',histoname=ROOT.string("templates"), bins = [yBins,qtBins,cosThetaBins,phiBins,etaBins,ptBins])
p2.gethdf5Output()

fewk = h5py.File('PLOTS/templates.hdf5', mode='r+')
h = np.array(fewk['templates'][:].reshape((len(yBins)-1,len(qtBins)-1, len(cosThetaBins)-1, len(phiBins)-1, len(etaBins)-1, len(ptBins)-1),order='F'),order='C')

# now derive the weights for the templates
totalxsec = np.sum(h,axis=(4,5)) # total differential xsec in y,qt,costheta,phi
norm = np.zeros(totalxsec.shape, dtype='float64')
norm+=totalxsec*P8w
for i,hw in enumerate(wharmonics):
    hharmonics[i] = hharmonics[i][..., np.newaxis, np.newaxis]
    norm+=totalxsec * hw * hharmonics[i]
norm*=3./(16.*pi)

wL = np.where(norm>0,3./(16.*pi) * totalxsec * P0w * hharmonics[0]/norm, 0)
wI = np.where(norm>0,3./(16.*pi) * totalxsec * P1w * hharmonics[1]/norm, 0)
wT = np.where(norm>0,3./(16.*pi) * totalxsec * P2w * hharmonics[2]/norm, 0)
wA = np.where(norm>0,3./(16.*pi) * totalxsec * P3w * hharmonics[3]/norm, 0)
wP = np.where(norm>0,3./(16.*pi) * totalxsec * P4w * hharmonics[4]/norm, 0)
wUL = np.where(norm>0,3./(16.*pi) * totalxsec * P8w/norm, 0)

whelicity = [wL,wI,wT,wA,wP,wUL]
hhelicity = []
# now reduce and produce the templates
for i,hw in enumerate(whelicity):
    htmp = np.einsum('ijmnkl,ijmn->ijkl',h,hw)
    hhelicity.append(htmp)
    # plot one slice of every templates
    fig, ax1 = plt.subplots()
    ax1.set_title("templates{}".format(i), fontsize=18)
    hep.hist2dplot(htmp[0,0,:,:-1],etaBins,ptBins[:-1])
    plt.savefig("templates{}".format(i))
    plt.cla()