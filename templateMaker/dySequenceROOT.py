import os
import sys
import ROOT
import argparse
import copy
import time
from datetime import datetime
#set all paths from FWK directory
FWKBASE=os.getenv('FWK_BASE')
sys.path.append('{}/RDFprocessor/framework'.format(FWKBASE))
from RDFtree import RDFtree
sys.path.append('{}/Common/data'.format(FWKBASE))
from samples_2016_ul import samplespreVFP
from binning import ptBins, etaBins, mTBins, etaBins, isoBins, chargeBins, zmassBins, qtBins,metBins,pvBins
from externals import fileSFul,filePt, fileY

sys.path.append('{}/templateMaker/python'.format(FWKBASE))
from getLumiWeight import getLumiWeight
ROOT.gSystem.Load('{}/templateMaker/bin/libAnalysisOnData.so'.format(FWKBASE))
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")


#Build the template building sequenc
def dySelectionSequence(p, xsec, systType, sumwClipped, nodetoStart, era):
    print(ptBins)
    print(zmassBins)
    luminosityN = 35.9
    if era == 'preVFP' :     luminosityN = 19.3
    else: luminosityN = 16.6

    p.branch(nodeToStart=nodetoStart, nodeToEnd='defs', modules=[ROOT.zVetoMuons()])
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Sum(vetoMuons)==2 && Sum(goodMuons)==2", filtername="{:20s}".format("two muons"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="(HLT_IsoMu24 ||  HLT_IsoTkMu24)", filtername="{:20s}".format("Pass HLT"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="(Muon_charge[goodMuons][0] + Muon_charge[goodMuons][1]) == 0", filtername="{:20s}".format("Opposite charge"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="std::abs(Muon_eta[goodMuons][0]) < 2.4 && std::abs(Muon_eta[goodMuons][1]) < 2.4", filtername="{:20s}".format("Accept"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Muon_mediumId[goodMuons][0] == 1 && Muon_mediumId[goodMuons][1] == 1", filtername="{:20s}".format("MuonId"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Muon_pfRelIso04_all[goodMuons][0] < 0.15 && Muon_pfRelIso04_all[goodMuons][1] < 0.15", filtername="{:20s}".format("Isolation"))
    p.branch(nodeToStart='defs', nodeToEnd='defs', modules=[ROOT.zSelection()])
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="60. < dimuonMass && dimuonMass < 120.", filtername="{:20s}".format("mZ range"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Mu1_hasTriggerMatch", filtername="{:20s}".format("+ve mu trig matched"))
    
    if systType == 0: #this is data
        weight = 'float(1)'
        nom = ROOT.vector('string')()
        nom.push_back("")
        p.branch(nodeToStart='defs', nodeToEnd='muonHistos', modules=[ROOT.zHistosROOT(weight, nom,"Nom", False)])#4th argument needed for Data
        return p
    elif systType == 1:
        print("Sample will be normalized to {}/fb".format(luminosityN))
        p.branch(nodeToStart = 'defs', nodeToEnd = 'defs', modules = [ROOT.lumiWeight(xsec=xsec, sumwclipped=sumwClipped, targetLumi = luminosityN), ROOT.SF_ul(fileSFul, isZ=True, era=era)])
        weight = 'float(lumiweight*puWeight*SF)'
        nom = ROOT.vector('string')()
        nom.push_back("")
        p.branch(nodeToStart='defs', nodeToEnd='muonHistos', modules=[ROOT.zHistosROOT(weight, nom,"Nom")])
        return p
    else:
        print("Sample will be normalized to {}/fb".format(luminosityN))
        p.branch(nodeToStart = 'defs', nodeToEnd = 'defs', modules = [ROOT.lumiWeight(xsec=xsec, sumwclipped=sumwClipped, targetLumi = luminosityN), ROOT.SF_ul(fileSFul, isZ=True, era=era)])
        #weight = 'float(lumiweight*puWeight*SF)'
        weight = 'float(lumiweight)'
        nom = ROOT.vector('string')()
        nom.push_back("")
        p.branch(nodeToStart='defs', nodeToEnd='muonHistos', modules=[ROOT.zHistosROOT(weight, nom,"Nom")])
        return p
