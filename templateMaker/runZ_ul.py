import os
import sys
import ROOT
import argparse
import copy
import time
from datetime import datetime
sys.path.append('../RDFprocessor/framework')
sys.path.append('../Common/data')
from RDFtree import RDFtree
from samples_2016_ul import samplespreVFP
sys.path.append('python/')
from binning import ptBins, etaBins, mTBins, zmassBins, isoBins, chargeBins
from externals import fileSFul

ROOT.gSystem.Load('bin/libAnalysisOnData.so')
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")

def RDFprocess(fvec, outputDir, sample, xsec, systType, pretendJob):
    print("processing ", sample)
    p = RDFtree(outputDir = outputDir, inputFile = fvec, outputFile="{}.root".format(sample), pretend=pretendJob)
    #not for customizeforUL(isMC=true, isWorZ=false)
    if systType == 0: #this is data
        p.branch(nodeToStart='input', nodeToEnd='defs', modules=[ROOT.customizeforUL(False, False), ROOT.recoDefinitions(False, False)])
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="HLT_SingleMu24", filtername="{:20s}".format("Pass HLT"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Vtype==2", filtername="{:20s}".format("Vtype multilepton selection"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="MET_filters==1", filtername="{:20s}".format("Pass MET filter"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Idx_mu1>-1 && Idx_mu2>-1", filtername="{:20s}".format("Atleast 2 mu"))
        p.branch(nodeToStart='defs', nodeToEnd='defs', modules=[ROOT.getZmass()])
        p.Histogram(columns = ["dimuonMass", "Mu1_eta", "Mu2_eta", "Mu1_pt", "Mu2_pt", "Mu1_relIso", "Mu2_relIso"], types = ['float']*7,node='defs',histoname=ROOT.string('data_obs'),bins = [zmassBins,etaBins,etaBins,ptBins, ptBins,isoBins, isoBins], variations = [])
        return p
    else:
        p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.lumiWeight(xsec=xsec), ROOT.customizeforUL(True, True), ROOT.recoDefinitions(True, False)])
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="HLT_SingleMu24", filtername="{:20s}".format("Pass HLT"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Vtype==2", filtername="{:20s}".format("Vtype multilepton selection"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="MET_filters==1", filtername="{:20s}".format("Pass MET filter"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Idx_mu1>-1 && Idx_mu2>-1", filtername="{:20s}".format("Atleast 2 mu"))
        p.branch(nodeToStart='defs', nodeToEnd='defs', modules=[ROOT.getZmass()])
        p.Histogram(columns = ["dimuonMass", "Mu1_eta", "Mu2_eta", "Mu1_pt", "Mu2_pt", "Mu1_relIso", "Mu2_relIso", "lumiweight", "puWeight"], types = ['float']*9,node='defs',histoname=ROOT.string('DY'),bins = [zmassBins,etaBins,etaBins,ptBins, ptBins,isoBins, isoBins], variations = [])
        return p

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-p', '--pretend',type=bool, default=False, help="run over a small number of event")
    parser.add_argument('-r', '--report',type=bool, default=False, help="Prints the cut flow report for all named filters")
    parser.add_argument('-o', '--outputDir',type=str, default='outputDY', help="output dir name")
    parser.add_argument('-i', '--inputDir',type=str, default='/scratchnvme/wmass/NanoAOD2016-UL/', help="input dir name")    
    parser.add_argument('-e', '--era',type=str, default='preVFP', help="either (preVFP|postVFP)")    

    args = parser.parse_args()
    pretendJob = args.pretend
    now = datetime.now()
    dt_string = now.strftime("_%d_%m_%Y_%H_%M_%S")
    outputDir = args.outputDir + dt_string
    inDir = args.inputDir
    era=args.era
    ##Add era to input dir
    inDir+=era
    if pretendJob:
        print("Running a test job over a few events")
    else:
        print("Running on full dataset")
    ROOT.ROOT.EnableImplicitMT(128)
    RDFtrees = {}
    
    samples = samplespreVFP
    for sample in samples:
        #print('analysing sample: %s'%sample)
        if not 'DY' in sample and not 'data' in sample: continue
        direc = samples[sample]['dir']
        xsec = samples[sample]['xsec']
        fvec=ROOT.vector('string')()
        for d in direc:
            targetDir='{}/{}/merged/'.format(inDir, d)
            for f in os.listdir(targetDir):#check the directory
                if not f.endswith('.root'): continue
                inputFile=targetDir+f
                #print(f)
                fvec.push_back(inputFile)
        if fvec.empty():
            print("No files found for directory:", samples[sample], " SKIPPING processing")
            continue
        print(fvec)         
        systType = samples[sample]['nsyst']
        RDFtrees[sample] = RDFprocess(fvec, outputDir, sample, xsec, systType, pretendJob)
    #sys.exit(0)
    #now trigger all the event loops at the same time:
    objList = []
    for sample in samples:
        if not 'DY' in sample and not 'data' in sample: continue
        RDFtreeDict = RDFtrees[sample].getObjects()
        for node in RDFtreeDict:
            objList.extend(RDFtreeDict[node])
    #magic happens here
    start = time.time()
    ROOT.RDF.RunGraphs(objList)
    #now write the histograms:
    
    for sample in samples:
        if not 'DY' in sample and not 'data' in sample: continue
        print(sample)
        #RDFtrees[sample].getOutput()
        RDFtrees[sample].gethdf5Output()
        if args.report: RDFtrees[sample].getCutFlowReport()

    print('all samples processed in {} s'.format(time.time()-start))
if __name__ == "__main__":
    main()
