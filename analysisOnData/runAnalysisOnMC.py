import os
import sys
import ROOT
import json
import argparse
import copy
import time
from RDFtree import RDFtree

sys.path.append('data/')
from systematics import systematics
from selections import selections, selectionVars, selections_bkg
sys.path.append('python/')
from getLumiWeight import getLumiWeight

ROOT.gSystem.Load('bin/libAnalysisOnData.so')
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")

def RDFprocess(fvec, outputDir, sample, xsec, fileSF, systType, pretendJob,SBana=False):

    p = RDFtree(outputDir = outputDir, inputFile = fvec, outputFile="{}_plots.root".format(sample), pretend=pretendJob)
    
    if systType == 0: #this is data
        p.branch(nodeToStart='input', nodeToEnd='defs', modules=[ROOT.baseDefinitions(False, False)])
    elif systType < 2: #this is MC with no PDF variations
        p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.baseDefinitions(True, False),ROOT.weightDefinitions(fileSF),getLumiWeight(xsec=xsec, inputFile=fvec)])
    else:
        p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.baseDefinitions(True, False),ROOT.weightDefinitions(fileSF),getLumiWeight(xsec=xsec, inputFile=fvec),ROOT.Replica2Hessian()])
    weight = 'float(puWeight*PrefireWeight*lumiweight*WHSF)'
    if systType == 0:
        weight = "float(1.)"
    cut = 'HLT_SingleMu24 && MET_filters==1 && nVetoElectrons==0'
    #nominal part of the analysis
    nom = ROOT.vector('string')()
    nom.push_back("")
    p.branch(nodeToStart = 'defs', nodeToEnd = 'templates/Nominal', modules = [ROOT.templates(sample, cut, weight, nom,"Nom",0)])

    return p
def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-p', '--pretend',type=bool, default=False, help="run over a small number of event")
    parser.add_argument('-o', '--outputDir',type=str, default='./output/', help="output dir name")
    parser.add_argument('-i', '--inputDir',type=str, default='/scratchnvme/wmass/NanoAOD2016-V2/', help="input dir name")    
    parser.add_argument('-s', '--SBana',type=bool, default=False, help="run also on the sideband (clousure test)")

    args = parser.parse_args()
    pretendJob = args.pretend
    outputDir = args.outputDir
    inDir = args.inputDir
    SBana = args.SBana

    if pretendJob:
        print("Running a test job over a few events")
    else:
        print("Running on full dataset")
    ROOT.ROOT.EnableImplicitMT(64)
    RDFtrees = {}
    samples={}
    with open('data/samples_2016.json') as f:
        samples = json.load(f)
    for sample in samples:
        #print('analysing sample: %s'%sample)
        direc = samples[sample]['dir']
        xsec = samples[sample]['xsec']
        fvec=ROOT.vector('string')()
        for dirname,fname in list(direc.items()):
            ##check if file exists or not
            inputFile = '{}/{}/tree.root'.format(inDir, dirname)
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
        systType = samples[sample]['systematics']
        RDFtrees[sample] = RDFprocess(fvec, outputDir, sample, xsec, fileSF, systType, pretendJob, SBana)

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
        #RDFtrees[sample].getOutput()
        RDFtrees[sample].gethdf5Output()
    print('all samples processed in {} s'.format(time.time()-start))
if __name__ == "__main__":
    main()
