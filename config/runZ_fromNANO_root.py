import os
import sys
import ROOT
import argparse
import copy
import time
from datetime import datetime

FWKBASE=os.getenv('FWK_BASE')
print('Adding path: {}/RDFprocessor/framework'.format(FWKBASE))
sys.path.append('{}/RDFprocessor/framework'.format(FWKBASE))
from RDFtree import RDFtree

sys.path.append('{}/Common/data'.format(FWKBASE))
from samples_2016_ul import samplespreVFP, samplespostVFP
#from samples_2016_ulCentral import samplespreVFP, samplespostVFP

from genSumWClipped import sumwClippedDictpreVFP, sumwClippedDictpostVFP

ROOT.gSystem.Load('{}/nanotools/bin/libNanoTools.so'.format(FWKBASE))
sys.path.append('../nanotools')
from nanoSequence import nanoSequence

ROOT.gSystem.Load('{}/nanotools/bin/libNanoTools.so'.format(FWKBASE))
sys.path.append('{}/nanotools'.format(FWKBASE))
from nanoSequence import nanoSequence

sys.path.append('{}/templateMaker/'.format(FWKBASE))
from dySequenceROOT  import dySelectionSequence

ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")

def RDFprocess(fvec, outputDir, sample, xsec, systType, sumwClipped, era, pretendJob):
    print("processing ", sample)
    p = RDFtree(outputDir = outputDir, inputFile = fvec, outputFile="{}.root".format(sample), pretend=pretendJob)
    postnano, endNode=nanoSequence(p, systType, era)
    print("Post nano node name: ", endNode)
    #return postnano
    resultNode=dySelectionSequence(postnano, xsec, systType, sumwClipped, endNode, era)
    return resultNode


def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-p', '--pretend',type=bool, default=False, help="run over a small number of event")
    parser.add_argument('-r', '--report',type=bool, default=False, help="Prints the cut flow report for all named filters")
    parser.add_argument('-o', '--outputDir',type=str, default='outputDY', help="output dir name")
    parser.add_argument('-i', '--inputDir',type=str, default='/scratchnvme/wmass/BARENANO/', help="input dir name")    
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
    ROOT.ROOT.EnableImplicitMT(64)
    RDFtrees = {}
    
    samples = samplespreVFP
    sumwClippedDict=sumwClippedDictpreVFP
    if era == 'postVFP': 
        samples = samplespostVFP
        sumwClippedDict=sumwClippedDictpostVFP

    for sample in samples:
        print('analysing sample: %s'%sample)
        if 'WPlus' in sample or 'WMinus' in sample: continue
        checkS= 'DYJetsToMuMu' in sample or 'data' in sample
        #print('CheckSample={}'.format(checkS))
        if not checkS : continue
        direc = samples[sample]['dir']
        xsec = samples[sample]['xsec']
        fvec=ROOT.vector('string')()
        for d in direc:
            #targetDir='{}/{}/merged/'.format(inDir, d)
            targetDir='{}/{}/'.format(inDir, d)
            for f in os.listdir(targetDir):#check the directory
                if not f.endswith('.root'): continue
                #Debug with Marco 
                #if '_99.' not in f : continue
                inputFile=targetDir+f
                #print(f)
                fvec.push_back(inputFile)
        if fvec.empty():
            print("No files found for directory:", samples[sample], " SKIPPING processing")
            continue
        print(fvec)         
        systType = samples[sample]['nsyst']
        sumwClipped=1.
        if systType == 2:
            sumwClipped=sumwClippedDict[sample]
            print(sample, sumwClipped)
        RDFtrees[sample] = RDFprocess(fvec, outputDir, sample, xsec, systType, sumwClipped, era, pretendJob)
    #sys.exit(0)
    #now trigger all the event loops at the same time:
    objList = []
    cutFlowreportDict = {}
    yieldDict = {}
    for sample in samples:
        if 'WPlus' in sample or 'WMinus' in sample: continue
        checkS= 'DYJetsToMuMu' in sample or 'data' in sample
        if not checkS : continue
        print(sample)
        RDFtreeDict = RDFtrees[sample].getObjects()
        if args.report: cutFlowreportDict[sample] = RDFtrees[sample].getCutFlowReport()
        if 'data' not in sample:
            yieldDict[sample] = {}
            varlist=["lumiweight", "puWeight", "SF", "totalWeight"]
            yieldDict[sample] = RDFtrees[sample].getYieldMap('defs', "uno", varlist)
        for node in RDFtreeDict:
            objList.extend(RDFtreeDict[node])

    #magic happens here
    start = time.time()
    ROOT.RDF.RunGraphs(objList)
    #now write the histograms:
    
    for sample in samples:
        if 'WPlus' in sample or 'WMinus' in sample: continue
        checkS= 'DYJetsToMuMu' in sample or 'data' in sample
        if not checkS : continue
        print(sample)
        RDFtrees[sample].getROOTOutput()
        if args.report: cutFlowreportDict[sample].Print()
        #RDFtrees[sample].saveGraph()

    print('all samples processed in {} s'.format(time.time()-start))
    
    print("Printing yield report")
    for sample, ymap in yieldDict.items():
        print(sample)
        for col, val in ymap.items():
            print("{:20s}:{}".format(col, val.GetW()))
#At some point this should be what we want
#p.Histogram(columns = ["dimuonMass", "Mu1_eta", "Mu1_pt", "Mu2_eta", "Mu2_pt", "dimuonPt", "dimuonY", "MET_T1_pt"], types = ['float']*8,node='defs',histoname=ROOT.string('data_muons'),bins = [zmassBins, etaBins, ptBins, etaBins, qtBins, etaBins, metBins], variations = [])
if __name__ == "__main__":
    main()

