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
def wSelectionSequence(p, xsec, systType, sumwClipped, nodetoStart, era, fvec):

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
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="nMuon== 1", filtername="{:20s}".format("one muon"))

    # note for customizeforUL(isMC=true, isWorZ=false)
    if systType == 0: #this is data
        p.branch(nodeToStart='defs', nodeToEnd='defs', modules=[ROOT.customizeforUL(False, False), ROOT.recoDefinitions(False, False)])
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Mu1_hasTriggerMatch", filtername="{:20s}".format("+ve mu trig matched"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Mu1_pt < 65.", filtername="{:20s}".format("mu1 pt-eta acceptance"))
        p.Histogram(columns = ["Mu1_eta","Mu1_pt","Mu1_charge","MT","Mu1_relIso"], types = ['float']*5,node='defs',histoname=ROOT.string('data_obs'),bins = [etaBins,ptBins,chargeBins,mTBins,isoBins], variations = [])
    elif systType < 2: #this is MC with no PDF variations
        print("Sample will be normalized to {}/fb".format(luminosityN))
        #falling back to old lumi weight computation
        p.branch(nodeToStart = 'defs', nodeToEnd = 'defs', modules = [ROOT.customizeforUL(True,False), ROOT.recoDefinitions(True, False), getLumiWeight(xsec=xsec, inputFile = fvec, genEvsbranch = "genEventSumw", targetLumi = luminosityN), ROOT.SF_ul(fileSFul)])
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Mu1_hasTriggerMatch", filtername="{:20s}".format("+ve mu trig matched"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Mu1_pt < 65.", filtername="{:20s}".format("mu1 pt-eta acceptance"))
        p.Histogram(columns = ["Mu1_eta","Mu1_pt","Mu1_charge","MT","Mu1_relIso", "lumiweight","puWeight","SF"], types = ['float']*8,node='defs',histoname=ROOT.string('ewk'),bins = [etaBins,ptBins,chargeBins,mTBins,isoBins], variations = [])
    else:
        print("Sample will be normalized to {}/fb".format(luminosityN))
        p.branch(nodeToStart = 'defs', nodeToEnd = 'defs', modules = [ROOT.customizeforUL(True, True), ROOT.recoDefinitions(True, False),ROOT.lumiWeight(xsec=xsec, sumwclipped=sumwClipped, targetLumi = luminosityN), ROOT.SF_ul(fileSFul)])
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Mu1_hasTriggerMatch", filtername="{:20s}".format("+ve mu trig matched"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Mu1_pt < 65.", filtername="{:20s}".format("mu1 pt-eta acceptance"))
        p.Histogram(columns = ["Mu1_eta","Mu1_pt","Mu1_charge","MT","Mu1_relIso", "lumiweight","puWeight","SF"], types = ['float']*8,node='defs',histoname=ROOT.string('ewk'),bins = [etaBins,ptBins,chargeBins,mTBins,isoBins], variations = [])
    return p
