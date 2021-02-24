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
    luminosityN = 35.9
    if era == 'preVFP' :     luminosityN = 19.3
    else: luminosityN = 16.6
    

    p.EventFilter(nodeToStart=nodetoStart, nodeToEnd='defs', evfilter="(HLT_IsoMu24 ||  HLT_IsoTkMu24)", filtername="{:20s}".format("Pass HLT"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="All(Muon_mediumId)", filtername="{:20s}".format("MuonID"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="All(Muon_pfRelIso04_all < 0.15)", filtername="{:20s}".format("both mu isolated"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="All(abs(Muon_dxy) < 0.05)", filtername="{:20s}".format("dxy"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="All(abs(Muon_dz) < 0.2)", filtername="{:20s}".format("dz"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="All(Muon_pt > 25.)", filtername="{:20s}".format("Muon pt cut"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="All(abs(Muon_eta) < 2.4)", filtername="{:20s}".format("Muon eta cut"))

    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="nMuon==2", filtername="{:20s}".format("twomuon"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="(Muon_charge[0] + Muon_charge[1] )== 0", filtername="{:20s}".format("Opposite charge"))
    p.branch(nodeToStart='defs', nodeToEnd='defs', modules=[ROOT.zSelection()])
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="60. < dimuonMass && dimuonMass < 120.", filtername="{:20s}".format("mZ range"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Mu1_hasTriggerMatch", filtername="{:20s}".format("+ve mu trig matched"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Mu1_pt < 65.", filtername="{:20s}".format("mu1 pt-eta acceptance"))

    if systType == 0: #this is data
        p.Histogram(columns = ["dimuonMass", "Mu1_eta", "Mu1_pt", "Mu2_eta", "Mu2_pt"], types = ['float']*5,node='defs',histoname=ROOT.string('data_muons'),bins = [zmassBins, etaBins, ptBins, etaBins, ptBins], variations = [])
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Mu2_pt < 200. ", filtername="{:20s}".format("mu2 pt upper acceptance"))
        p.Histogram(columns = ["dimuonMass", "dimuonPt", "dimuonY", "MET_pt"], types = ['float']*4,node='defs',histoname=ROOT.string('data_dimuon'),bins = [zmassBins,qtBins, etaBins, metBins], variations = [])
        return p
    elif systType == 1:
        print("Sample will be normalized to {}/fb".format(luminosityN))
        p.branch(nodeToStart = 'defs', nodeToEnd = 'defs', modules = [getLumiWeight(xsec=xsec, inputFile = fvec, genEvsbranch = "genEventSumw", targetLumi = luminosityN), ROOT.SF_ul(fileSFul, isZ=True,era=era)])
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Mu2_pt < 200. ", filtername="{:20s}".format("mu2 pt upper acceptance"))
        p.Histogram(columns = ["dimuonMass", "dimuonPt", "dimuonY", "MET_pt", "lumiweight", "puWeight", "SF"], types = ['float']*7,node='defs',histoname=ROOT.string('DY_dimuon'),bins = [zmassBins,qtBins, etaBins,metBins], variations = [])
        return p
    else:
        print("Sample will be normalized to {}/fb".format(luminosityN))
        p.branch(nodeToStart = 'defs', nodeToEnd = 'defs', modules = [ROOT.lumiWeight(xsec=xsec, sumwclipped=sumwClipped, targetLumi = luminosityN), ROOT.SF_ul(fileSFul, isZ=True, era=era)])
        p.Histogram(columns = ["dimuonMass", "Mu1_eta", "Mu1_pt", "Mu2_eta", "Mu2_pt", "lumiweight", "puWeight", "SF"], types = ['float']*8,node='defs',histoname=ROOT.string('DY_muons'),bins = [zmassBins, etaBins, ptBins, etaBins, ptBins], variations = [])
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Mu2_pt < 200. ", filtername="{:20s}".format("mu2 pt upper acceptance"))
        p.Histogram(columns = ["dimuonMass", "dimuonPt", "dimuonY", "MET_pt", "lumiweight", "puWeight", "SF"], types = ['float']*7,node='defs',histoname=ROOT.string('DY_dimuon'),bins = [zmassBins,qtBins, etaBins,metBins], variations = [])
        return p
