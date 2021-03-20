import os
import sys
import ROOT
import copy
import time
import h5py
from math import pi, sqrt
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
from externals import filePt, fileY, fileSF, fileSFul

# matplotlib stuff
plt.style.use([hep.style.ROOT])
hep.cms.label(loc=0, year=2016, lumi=35.9, data=True)
hep.cms.text('Simulation')

ROOT.gSystem.Load('bin/libAnalysisOnData.so')

ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")

ROOT.ROOT.EnableImplicitMT(48)

outputDir = 'PLOTS'
inputFile = '/scratchnvme/wmass/NanoAOD2016-UL/postNanoDec2020/WplusJetsToMuNu_preVFP_addVars/merged/*.root'

luminosityN = 19.3
sumwclipped = 5895502305412.54

p = RDFtree(outputDir = outputDir, inputFile = inputFile, outputFile="test.root", pretend=False)
p.branch(nodeToStart='input', nodeToEnd='defs', modules=[ROOT.lumiWeight(xsec=11572.19, sumwclipped=sumwclipped, targetLumi = luminosityN), ROOT.customizeforUL(True,True), ROOT.genDefinitions()])
p.Histogram(columns = ["Wrap_preFSR_abs","Vpt_preFSR","CStheta_preFSR","CSphi_preFSR","lumiweight"], types = ['float']*5,node='defs',histoname=ROOT.string("xsecs"), bins = [yBins,qtBins,cosThetaBins,phiBins])
p.gethdf5Output()

fewk = h5py.File('PLOTS/test.hdf5', mode='r+')
hFullAcc = np.array(fewk['xsecs'][:].reshape((len(yBins)-1,len(qtBins)-1, len(cosThetaBins)-1, len(phiBins)-1),order='F'),order='C')

fig, ax1 = plt.subplots()
ax1.set_title("CS theta", fontsize=18)
ax1.set_ylabel('Events')
ax1.set_xlabel('CS $\theta$')
data = np.sum(hFullAcc,axis=(0,1,3))
hep.histplot([data],bins = cosThetaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1)
plt.savefig('CStheta.png')
plt.cla()

fig, ax1 = plt.subplots()
ax1.set_title("CS phi", fontsize=18)
ax1.set_ylabel('Events')
ax1.set_xlabel('CS $\phi$')
data = np.sum(hFullAcc,axis=(0,1,2))
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
totalxsec = np.sum(hFullAcc,axis=(2,3))

fig, ax1 = plt.subplots()
ax1.set_title("total xsec", fontsize=18)
hep.hist2dplot(totalxsec,yBins,qtBins)
plt.savefig("total_xsec")
plt.cla()

factors = [(20./3., 1./10),(5.,0.),(20.,0.),(4.,0.),(4.,0.),(5.,0.),(5.,0.),(4.,0.)]
for i,hw in enumerate(wharmonics):
    htmp = np.einsum('ijkm,km->ij',hFullAcc,hw)/totalxsec
    htmp = factors[i][0]*(htmp+factors[i][1])
    hharmonics.append(htmp)
    fig, ax1 = plt.subplots()
    ax1.set_title("A{}".format(i), fontsize=18)
    hep.hist2dplot(htmp,yBins,qtBins)
    plt.savefig("A{}".format(i))
    plt.cla()

# reprocess with acceptance cuts
p2 = RDFtree(outputDir = outputDir, inputFile = inputFile, outputFile="templates.root", pretend=False)
p2.EventFilter(nodeToStart='input', nodeToEnd='defs', evfilter="HLT_SingleMu24", filtername="{:20s}".format("Pass HLT"))
p2.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="All(Muon_mediumId)", filtername="{:20s}".format("MuonID"))
p2.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="All(Muon_pfRelIso04_all < 0.15)", filtername="{:20s}".format("both mu isolated"))
p2.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="All(abs(Muon_dxy) < 0.05)", filtername="{:20s}".format("dxy"))
p2.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="All(abs(Muon_dz) < 0.2)", filtername="{:20s}".format("dz"))
p2.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="All(Muon_pt > 25.)", filtername="{:20s}".format("Muon pt cut"))
p2.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="All(abs(Muon_eta) < 2.4)", filtername="{:20s}".format("Muon eta cut"))
p2.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="nMuon== 1", filtername="{:20s}".format("one muon"))
p2.branch(nodeToStart = 'defs', nodeToEnd = 'defs', modules = [ROOT.customizeforUL(True, True), ROOT.genDefinitions(),ROOT.recoDefinitions(True, False),ROOT.lumiWeight(xsec=11572.19, sumwclipped=sumwclipped, targetLumi = luminosityN), ROOT.SF_ul(fileSFul)])
p2.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Mu1_hasTriggerMatch", filtername="{:20s}".format("+ve mu trig matched"))
p2.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Mu1_pt < 65.", filtername="{:20s}".format("mu1 pt-eta acceptance"))
p2.Histogram(columns = ["Wrap_preFSR_abs","Vpt_preFSR","CStheta_preFSR","CSphi_preFSR","Mu1_eta", "Mu1_pt","lumiweight"], types = ['float']*7,node='defs',histoname=ROOT.string("templates"), bins = [yBins,qtBins,cosThetaBins,phiBins,etaBins,ptBins])
p2.gethdf5Output()

fewk = h5py.File('PLOTS/templates.hdf5', mode='r+')
h = np.array(fewk['templates'][:].reshape((len(yBins)-1,len(qtBins)-1, len(cosThetaBins)-1, len(phiBins)-1, len(etaBins)-1, len(ptBins)-1),order='F'),order='C')
herr = np.array(fewk['templates_sumw2'][:].reshape((len(yBins)-1,len(qtBins)-1, len(cosThetaBins)-1, len(phiBins)-1, len(etaBins)-1, len(ptBins)-1),order='F'),order='C')

# now derive the weights for the templates
totalxsec = hFullAcc # total differential xsec in y,qt,costheta,phi with no acceptance cuts
norm = np.zeros(totalxsec.shape, dtype='float64')
norm+=totalxsec*P8w

#rescale to get helicity xsecs
hharmonics[0]/=2.
hharmonics[1]/=(2.*sqrt(2))
hharmonics[2]/=4.
hharmonics[3]/=(4.*sqrt(2))
hharmonics[4]/=2.
hharmonics[5]/=2.
hharmonics[6]/=(2.*sqrt(2))
hharmonics[7]/=(4.*sqrt(2))

for i,hw in enumerate(wharmonics):
    hharmonics[i] = hharmonics[i][..., np.newaxis, np.newaxis]
    norm+=totalxsec * hw * hharmonics[i]
norm*=3./(16.*pi)

# import pdb; pdb.set_trace()

wL = 3./(16.*pi) * totalxsec * P0w * hharmonics[0]/norm
wI = 3./(16.*pi) * totalxsec * P1w * hharmonics[1]/norm
wT = 3./(16.*pi) * totalxsec * P2w * hharmonics[2]/norm
wA = 3./(16.*pi) * totalxsec * P3w * hharmonics[3]/norm
wP = 3./(16.*pi) * totalxsec * P4w * hharmonics[4]/norm
w7 = 3./(16.*pi) * totalxsec * P5w * hharmonics[5]/norm
w8 = 3./(16.*pi) * totalxsec * P6w * hharmonics[6]/norm
w9 = 3./(16.*pi) * totalxsec * P7w * hharmonics[7]/norm
wUL = 3./(16.*pi) * totalxsec * P8w/norm

whelicity = [wL,wI,wT,wA,wP,w7,w8,w9,wUL]
hhelicity = []
herrhelicity = []

# now reduce and produce the templates
for i,hw in enumerate(whelicity):
    htmp = np.einsum('ijmnkl,ijmn->ijkl',h,hw)
    hhelicity.append(htmp)
    htmp_err = np.einsum('ijmnkl,ijmn->ijkl',herr,hw)
    herrhelicity.append(htmp)
    # plot one slice of every templates
    fig, ax1 = plt.subplots()
    ax1.set_title("templates{}".format(i), fontsize=18)
    hep.hist2dplot(htmp[2,2,:,:-1],etaBins,ptBins[:-1])
    plt.savefig("templates{}".format(i))
    plt.cla()

# check closure of templates sum

totalxsec_clos = np.sum(hhelicity[0]+hhelicity[1]+hhelicity[2]+hhelicity[3]+hhelicity[4]+hhelicity[5]+hhelicity[6]+hhelicity[7]+hhelicity[8], axis=(0,1))
totalxsec = np.sum(h,axis=(0,1,2,3))
fig, ax1 = plt.subplots()
ax1.set_title("total xsec closure", fontsize=18)
hep.hist2dplot(totalxsec_clos[:,:-1],etaBins,ptBins[:-1])
plt.savefig("total_xsec_clos")
plt.cla()
ax1.set_title("total xsec etapt", fontsize=18)
hep.hist2dplot(totalxsec[:,:-1],etaBins,ptBins[:-1])
plt.savefig("total_xsec_etapt")
plt.cla()

# propagate uncertainty

# # rescale to make them positive defined

# hhelicity[0]+=hhelicity[-1]/6.
# hhelicity[1]+=hhelicity[-1]/6.
# hhelicity[2]+=hhelicity[-1]/6.
# hhelicity[3]+=hhelicity[-1]/6.
# hhelicity[4]+=hhelicity[-1]/6.
# hhelicity[-1]/=6.

# for i,h in enumerate(hhelicity):
#     # plot one slice of every templates
#     fig, ax1 = plt.subplots()
#     ax1.set_title("templates{}_rescaled".format(i), fontsize=18)
#     hep.hist2dplot(h[0,0,:,:-1],etaBins,ptBins[:-1])
#     plt.savefig("templates{}_rescaled".format(i))
#     plt.cla()
