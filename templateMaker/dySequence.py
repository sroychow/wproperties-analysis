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
def dySelectionSequence(p, xsec, systType, sumwClipped, nodetoStart):
    p.EventFilter(nodeToStart=nodetoStart, nodeToEnd='defs', evfilter="nMuon>=2", filtername="{:20s}".format("twomuon"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="(HLT_IsoMu24 ||  HLT_IsoTkMu24)", filtername="{:20s}".format("Pass HLT"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="(Muon_charge[0] + Muon_charge[1] )== 0", filtername="{:20s}".format("Opposite charge"))
    #For cross-check                                                                                                                                   
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Muon_mediumId[0] == 1 && Muon_mediumId[1] == 1", filtername="{:20s}".format("MuonID"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Muon_pfRelIso04_all[0] < 0.15 && Muon_pfRelIso04_all[1] < 0.15", filtername="{:20s}".format("both mu isolated"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="abs(Muon_dxy[0]) < 0.05 && abs(Muon_dxy[1]) < 0.05", filtername="{:20s}".format("dxy"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="abs(Muon_dz[0]) < 0.2 && abs(Muon_dz[1]) < 0.2", filtername="{:20s}".format("dz"))
    p.branch(nodeToStart='defs', nodeToEnd='defs', modules=[ROOT.zSelection()])
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="60. < dimuonMass && dimuonMass < 120.", filtername="{:20s}".format("mZ range"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Mu1_hasTriggerMatch", filtername="{:20s}".format("+ve mu trig matched"))
    
    if systType == 0: #this is data
        p.Histogram(columns = ["dimuonMass", "Mu1_eta", "Mu1_pt", "Mu2_eta", "Mu2_pt"], types = ['float']*5,node='defs',histoname=ROOT.string('data_muons'),bins = [zmassBins, etaBins, ptBins, etaBins, ptBins], variations = [])
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="abs(Mu1_eta) < 2.4 && abs(Mu2_eta) < 2.4 && Mu1_pt > 25. && Mu2_pt > 25. && Mu1_pt < 55. && Mu2_pt < 55.", filtername="{:20s}".format("mu pt eta acceptance"))
        p.Histogram(columns = ["dimuonMass", "dimuonPt", "dimuonY", "MET_pt"], types = ['float']*4,node='defs',histoname=ROOT.string('data_dimuon'),bins = [zmassBins,qtBins, etaBins, metBins], variations = [])
        return p
    elif systType == 1:
        p.branch(nodeToStart = 'defs', nodeToEnd = 'defs', modules = [getLumiWeight(xsec=xsec, inputFile = fvec, genEvsbranch = "genEventSumw", targetLumi = 19.3), ROOT.SF_ul(fileSFul, isZ=True)])
        p.Histogram(columns = ["dimuonMass", "Mu1_eta", "Mu1_pt", "Mu2_eta", "Mu2_pt", "lumiweight", "puWeight"], types = ['float']*7,node='defs',histoname=ROOT.string('DY_muons'),bins = [zmassBins, etaBins, ptBins, etaBins, ptBins], variations = [])
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="abs(Mu1_eta) < 2.4 && abs(Mu2_eta) < 2.4 && Mu1_pt > 25. && Mu2_pt > 25. && Mu1_pt < 55. && Mu2_pt < 55.", filtername="{:20s}".format("mu pt eta acceptance"))
        p.Histogram(columns = ["dimuonMass", "dimuonPt", "dimuonY", "MET_pt", "lumiweight", "puWeight"], types = ['float']*6,node='defs',histoname=ROOT.string('DY_dimuon'),bins = [zmassBins,qtBins, etaBins,metBins], variations = [])
        return p
    else:
        p.branch(nodeToStart = 'defs', nodeToEnd = 'defs', modules = [ROOT.lumiWeight(xsec=xsec, sumwclipped=236188699235.12158, targetLumi = 19.3), ROOT.SF_ul(fileSFul, isZ=True)])
        p.Histogram(columns = ["dimuonMass", "Mu1_eta", "Mu1_pt", "Mu2_eta", "Mu2_pt", "lumiweight", "puWeight"], types = ['float']*7,node='defs',histoname=ROOT.string('DY_muons'),bins = [zmassBins, etaBins, ptBins, etaBins, ptBins], variations = [])
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="abs(Mu1_eta) < 2.4 && abs(Mu2_eta) < 2.4 && Mu1_pt > 25. && Mu2_pt > 25. && Mu1_pt < 55. && Mu2_pt < 55.", filtername="{:20s}".format("mu pt eta acceptance"))
        p.Histogram(columns = ["dimuonMass", "dimuonPt", "dimuonY", "MET_pt", "lumiweight", "puWeight"], types = ['float']*6,node='defs',histoname=ROOT.string('DY_dimuon'),bins = [zmassBins,qtBins, etaBins,metBins], variations = [])
        return p

