import os
import sys
import ROOT
import argparse
import copy
import time
from datetime import datetime

FWKBASE=os.getenv('FWK_BASE')
sys.path.append('{}/RDFprocessor/framework'.format(FWKBASE))
from RDFtree import RDFtree

sys.path.append('{}/Common/data/'.format(FWKBASE))
from externals import pufile_mc_UL2016, pufile_data_UL2016_allData, pufile_data_UL2016_preVFP, pufile_data_UL2016_postVFP

ROOT.gSystem.Load('{}/nanotools/bin/libNanoTools.so'.format(FWKBASE))

ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")

#pass a RDFtree object
def nanoSequence(rdftree, systType, era):    
    endNode="input" #this is to protect if no postnano sequence is run
    if systType == 0: #this is data
        endNode='postnano'
        rdftree.branch(nodeToStart='input', nodeToEnd='postnano', modules=[ROOT.trigObjMatchProducer()])
    else: #this is mc
        endNode='postnano'
        datapu = pufile_data_UL2016_preVFP
        mcprofName="Pileup_nTrueInt_Wplus_preVFP"
        eraCode=1#1 for preVFP, 2 for postVFP
            
        if era == 'postVFP' : 
            datapu=pufile_data_UL2016_postVFP
            mcprofName="Pileup_nTrueInt_Wplus_preVFP"
            eraCode=2
        if not datapu :
            print("DATA pu hist doesn't exist")
            sys.exit(2)
        if not pufile_mc_UL2016 :
            print("MC pu hist doesn't exist")
            sys.exit(2)   
        print('Using puWeight producer era code=',eraCode)
        #TFile *puMC, TFile *puData, TString hmcName, TString hdataName, bool dosyst, booql fixlargeW = true, bool normtoArea = true
        #rdftree.branch(nodeToStart='input', nodeToEnd='postnano', modules=[ROOT.puWeightProducer(mcprofName, "pileup", False, True, True), ROOT.trigObjMatchProducer()])
        #FOR ROOT HISTOS
        rdftree.branch(nodeToStart='input', nodeToEnd='postnano', modules=[ROOT.puWeightProducer(eraCode), ROOT.trigObjMatchProducer()])
    return rdftree,endNode
