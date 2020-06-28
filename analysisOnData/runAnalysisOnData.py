import os
import sys
import ROOT

sys.path.append('../RDFprocessor/framework/')
from RDFtree import RDFtree
sys.path.append('python/')
sys.path.append('data/')
from systematics import systematics
from selections import *

from getLumiWeight import getLumiWeight

ROOT.gSystem.Load('bin/libAnalysisOnData.so')

c=4
		
ROOT.ROOT.EnableImplicitMT(c)

print "running with {} cores".format(c)

inputFile = '/scratchssd/sroychow/NanoAOD2016-V2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tree.root'

inputFile='/home/sroychow/wmass/v6/081594F6-3B7A-0044-B7B8-D9F44C91B6E1_Skim.root'
cutSignal = 'Vtype==0 && HLT_SingleMu24 && Mu1_pt>25. && MT>0. && MET_filters==1 && nVetoElectrons==0' 
regions = {}
regions['signal'] = cutSignal

weight = 'float(puWeight*lumiweight*TriggerSF*RecoSF)'

fileSF = ROOT.TFile.Open("data/ScaleFactors.root")

p = RDFtree(outputDir = 'TEST', inputFile = inputFile, outputFile="test.root", pretend=False)

p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.baseDefinitions(),ROOT.weightDefinitions(fileSF),getLumiWeight(xsec=61526.7, inputFile=inputFile)])

for region,cut in selections.iteritems():
    nom = ROOT.vector('string')()
    nom.push_back("Nom")
    #last argument refers to histo category - 0 = Nominal, 1 = corrected Pt , 2 = JER , 3 = JES, 4 = unclusEn
    p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}'.format(region), modules = [ROOT.selectionDefs(cut)])
    #one can also pass an empty cut below
    p.branch(nodeToStart = 'prefit_{}'.format(region), nodeToEnd = 'prefit_{}_Nominal'.format(region), modules = [ROOT.muonHistos(cut, weight, nom,"Nom",0)])    
    #weight variations
    for s,variations in systematics.iteritems():
        weight.replace(s, "1.")
        vars_vec = ROOT.vector('string')()
        for var in variations[0]:
            vars_vec.push_back(var)
        p.branch(nodeToStart = 'prefit_{}'.format(region), nodeToEnd = 'prefit_{}_{}Vars'.format(region,s), modules = [ROOT.muonHistos(cut, weight,vars_vec,variations[1], 0)])
    #column variations#weight will be nominal, cut will vary
    for vartype, vardict in selectionVars.iteritems():
        newnode = vartype
        selVarvec = ROOT.vector('string')()
        for selvar, hcat in vardict.iteritems() :
            newcut = cut.replace('MT', 'MT_'+selvar)
            if 'corrected' in selvar:
                newcut = newcut.replace('Mu1_pt', 'Mu1_pt_'+selvar)
            print newcut, '\t', hcat, '\t', newnode
            p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}/{}/{}'.format(region, vartype, selvar), modules = [ROOT.muonHistos(newcut, weight, nom,"Nom",hcat,selvar)])  
      
    
p.getOutput()
p.saveGraph()




