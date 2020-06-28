import os
import sys
import ROOT

#sys.path.append('../RDFprocessor/framework/')
from RDFtree import RDFtree
sys.path.append('python/')
sys.path.append('data/')
from systematics import systematics
from selections import selections, selectionVars

from getLumiWeight import getLumiWeight

ROOT.gSystem.Load('bin/libAnalysisOnData.so')

c=64
		
ROOT.ROOT.EnableImplicitMT(c)

print "running with {} cores".format(c)

inputFile = '/scratchssd/sroychow/NanoAOD2016-V2/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/WJetsToLNu_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/tree.root'

weight = 'float(puWeight*lumiweight*TriggerSF*RecoSF)'

fileSF = ROOT.TFile.Open("data/ScaleFactors.root")

p = RDFtree(outputDir = 'TEST', inputFile = inputFile, outputFile="test.root", pretend=True)

p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.baseDefinitions(),ROOT.weightDefinitions(fileSF),getLumiWeight(xsec=61526.7, inputFile=inputFile)])

for region,cut in selections.iteritems():
    nom = ROOT.vector('string')()
    nom.push_back("")
    #last argument refers to histo category - 0 = Nominal, 1 = Pt scale , 2 = MET scale
    print "branching nominal"
    p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}_Nominal'.format(region), modules = [ROOT.muonHistos(cut, weight, nom,"Nom",0)])    
    #weight variations
    for s,variations in systematics.iteritems():
        weight.replace(s, "1.")
        vars_vec = ROOT.vector('string')()
        for var in variations[0]:
            vars_vec.push_back(var)
        print "branching weight variations", region, s
        p.branch(nodeToStart = 'defs'.format(region), nodeToEnd = 'prefit_{}_{}Vars'.format(region,s), modules = [ROOT.muonHistos(cut, weight,vars_vec,variations[1], 0)])
    #column variations#weight will be nominal, cut will vary
    
    for vartype, vardict in selectionVars.iteritems():
        cut_vec = ROOT.vector('string')()
        var_vec = ROOT.vector('string')()
        for selvar, hcat in vardict.iteritems() :
            newcut = cut.replace('MT', 'MT_'+selvar)
            
            if 'corrected' in selvar:
                newcut = newcut.replace('Mu1_pt', 'Mu1_pt_'+selvar)
            
            cut_vec.push_back(newcut)
            var_vec.push_back(selvar)
        
        p.branch(nodeToStart = 'defs', nodeToEnd = 'prefit_{}_{}Vars'.format(region,vartype), modules = [ROOT.muonHistos(cut_vec, weight, nom,"Nom",hcat,var_vec)])  
            
    
p.getOutput()
p.saveGraph()




