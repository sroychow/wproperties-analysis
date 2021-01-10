import os
import sys
import ROOT
import json
import argparse
import copy
import time
sys.path.append('../RDFprocessor/framework')
from RDFtree import RDFtree
sys.path.append('data/')
from samples_2016 import samples
sys.path.append('python/')
from getLumiWeight import getLumiWeight

ROOT.gSystem.Load('bin/libAnalysisOnData.so')
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")

def RDFprocess(fvec, outputDir, sample, xsec, fileSF, systType, pretendJob):
    print("processing ", sample)
    p = RDFtree(outputDir = outputDir, inputFile = fvec, outputFile="{}.root".format(sample), pretend=pretendJob)
    
    ptBins = ROOT.vector('float')([25.+i*0.5 for i in range(61)])
    etaBins = ROOT.vector('float')([-2.4+i*0.1 for i in range(49)])
    chargeBins = ROOT.vector('float')(-2. +i*2. for i in range(3))
    mTBins = ROOT.vector('float')([0.,30.,40.,2000.])
    isoBins = ROOT.vector('float')([0.,0.15,1.])

    if systType == 0: #this is data
        p.branch(nodeToStart='input', nodeToEnd='defs', modules=[ROOT.baseDefinitions(False, False)])
        p.EventFilter(nodeToStart='defs', nodeToEnd='filtered', evfilter="HLT_SingleMu24", filtername="Pass HLT")
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="(Vtype==0 || Vtype==1)", filtername="Vtype selection")
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="HLT_SingleMu24", filtername="Pass HLT")
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="MET_filters==1", filtername="Pass MET filter")
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="nVetoElectrons==0", filtername="Electron veto")
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Idx_mu1>-1", filtername="Event has atleast 1 muon")
        p.Histogram(columns = ["Mu1_eta","Mu1_pt","Mu1_charge","MT","Mu1_relIso"], types = ['float']*5,node='defs',histoname=ROOT.string("test"),bins = [etaBins,ptBins,chargeBins,mTBins,isoBins])
        return p
    elif systType < 2: #this is MC with no PDF variations
        p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.baseDefinitions(True, False),ROOT.weightDefinitions(fileSF),getLumiWeight(xsec=xsec, inputFile=fvec)])
    else:
        p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.baseDefinitions(True, False),ROOT.weightDefinitions(fileSF),getLumiWeight(xsec=xsec, inputFile=fvec),ROOT.Replica2Hessian()])
    
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="HLT_SingleMu24", filtername="Pass HLT")
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="(Vtype==0 || Vtype==1)", filtername="Vtype selection")
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="HLT_SingleMu24", filtername="Pass HLT")
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="MET_filters==1", filtername="Pass MET filter")
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="nVetoElectrons==0", filtername="Electron veto")
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Idx_mu1>-1", filtername="Event has atleast 1 muon")
    p.Histogram(columns = ["Mu1_eta","Mu1_pt","Mu1_charge","MTVars","Mu1_relIso", "lumiweight", "PrefireWeight", "puWeight", "WHSFVars"], types = ['float']*9,node='defs',histoname=ROOT.string("test"),bins = [etaBins,ptBins,chargeBins,mTBins,isoBins])
    return p

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-p', '--pretend',type=bool, default=False, help="run over a small number of event")
    parser.add_argument('-r', '--report',type=bool, default=False, help="Prints the cut flow report for all named filters")
    parser.add_argument('-o', '--outputDir',type=str, default='./output/', help="output dir name")
    parser.add_argument('-i', '--inputDir',type=str, default='/scratchnvme/wmass/NanoAOD2016-V2/', help="input dir name")    

    args = parser.parse_args()
    pretendJob = args.pretend
    outputDir = args.outputDir
    inDir = args.inputDir
    print("Print report?>>>{}".format(args.report))
    if pretendJob:
        print("Running a test job over a few events")
    else:
        print("Running on full dataset")
    ROOT.ROOT.EnableImplicitMT(64)
    RDFtrees = {}
    
    for sample in samples:
        #print('analysing sample: %s'%sample)

        direc = samples[sample]['dir']
        xsec = samples[sample]['xsec']
        fvec=ROOT.vector('string')()
        for d in direc:
            ##check if file exists or not
            inputFile = '{}/{}/tree.root'.format(inDir, d)
            isFile = os.path.isfile(inputFile)
            if not isFile:
                print(inputFile, " does not exist")
                continue
            fvec.push_back(inputFile)
            #f = ROOT.TFile(inputFile)
            #t = f.Get('Events')
            #it = t.GetClusterIterator(0)
            #counter = 0
            #n_entries = t.GetEntries()
            #while it.Next() != n_entries:
            #    counter += 1
            #print('number of clusters:',counter, sample)
        if fvec.empty():
            print("No files found for directory:", samples[sample], " SKIPPING processing")
            continue
        #print(fvec) 
        fileSF = ROOT.TFile.Open("data/ScaleFactors_OnTheFly.root")
        systType = samples[sample]['nsyst']
        RDFtrees[sample] = RDFprocess(fvec, outputDir, sample, xsec, fileSF, systType, pretendJob)

    #now trigger all the event loops at the same time:
    objList = []
    for sample in samples:
        RDFtreeDict = RDFtrees[sample].getObjects()
        for node in RDFtreeDict:
            objList.extend(RDFtreeDict[node])
    #magic happens here
    start = time.time()
    ROOT.RDF.RunGraphs(objList)
    #now write the histograms:
    
    for sample in samples:
        print(sample)
        #RDFtrees[sample].getOutput()
        RDFtrees[sample].gethdf5Output()
        if args.report: 
            RDFtrees[sample].getCutFlowReport()

    print('all samples processed in {} s'.format(time.time()-start))
if __name__ == "__main__":
    main()
