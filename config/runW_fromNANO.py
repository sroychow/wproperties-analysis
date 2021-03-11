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
#from samples_2016_ul import samplespreVFP, samplespostVFP
from genSumWClipped import sumwClippedDictpreVFP, sumwClippedDictpostVFP
from samples_2016_ulCentral import samplespreVFP, samplespostVFP

ROOT.gSystem.Load('{}/nanotools/bin/libNanoTools.so'.format(FWKBASE))
sys.path.append('../nanotools')
from nanoSequence import nanoSequence

ROOT.gSystem.Load('{}/nanotools/bin/libNanoTools.so'.format(FWKBASE))
sys.path.append('{}/nanotools'.format(FWKBASE))
from nanoSequence import nanoSequence

sys.path.append('{}/templateMaker/'.format(FWKBASE))
from wSequence import wSelectionSequence

ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")

def RDFprocess(fvec, outputDir, sample, xsec, systType, sumwClipped, era, pretendJob):
    print("processing ", sample)
    p = RDFtree(outputDir = outputDir, inputFile = fvec, outputFile="{}.root".format(sample), pretend=pretendJob)
    postnano, endNode=nanoSequence(p, systType, era)
    print("Post nano node name: ", endNode)
    #return postnano
    resultNode=wSelectionSequence(postnano, xsec, systType, sumwClipped, endNode, era, fvec)
    return resultNode


def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-p', '--pretend',type=bool, default=False, help="run over a small number of event")
    parser.add_argument('-r', '--report',type=bool, default=False, help="Prints the cut flow report for all named filters")
    parser.add_argument('-o', '--outputDir',type=str, default='outputW', help="output dir name")
    parser.add_argument('-i', '--inputDir',type=str, default='/scratchnvme/wmass/', help="input dir name")    
    parser.add_argument('-e', '--era',type=str, default='preVFP', help="either (preVFP|postVFP)")    

    args = parser.parse_args()
    pretendJob = args.pretend
    now = datetime.now()
    dt_string = now.strftime("_%d_%m_%Y_%H_%M_%S")
    inDir = args.inputDir
    era=args.era
    outputDir = args.outputDir+"_"+era
    ##Add era to input dir
    #inDir+=era
    if pretendJob:
        print("Running a test job over a few events")
    else:
        print("Running on full dataset")
    ROOT.ROOT.EnableImplicitMT(128)
    RDFtrees = {}
    
    samples = samplespreVFP
    sumwClippedDict=sumwClippedDictpreVFP
    if era == 'postVFP': 
        samples = samplespostVFP
        sumwClippedDict=sumwClippedDictpostVFP

    for sample in samples:
        if 'ST_t-channel_top_5f' in sample: continue
        print('analysing sample: %s'%sample)
        direc = samples[sample]['dir']
        xsec = samples[sample]['xsec']
        fvec=ROOT.vector('string')()
        for d in direc:
            targetDir='{}/{}/'.format(inDir, d)
            for f in os.listdir(targetDir):#check the directory
                if not f.endswith('.root'): continue
                inputFile=targetDir+f
                #print(f)
                fvec.push_back(inputFile)
        if fvec.empty():
            print("No files found for directory:", samples[sample], " SKIPPING processing")
            continue
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
    for sample in samples:
        if 'ST_t-channel_top_5f' in sample: continue
        print(sample)
        RDFtreeDict = RDFtrees[sample].getObjects()
        if args.report: cutFlowreportDict[sample] = RDFtrees[sample].getCutFlowReport()
        for node in RDFtreeDict:
            objList.extend(RDFtreeDict[node])

    #magic happens here
    start = time.time()
    ROOT.RDF.RunGraphs(objList)
    #now write the histograms:
    
    for sample in samples:
        print(sample)
        if 'ST_t-channel_top_5f' in sample: continue
        RDFtrees[sample].gethdf5Output()
        if args.report: cutFlowreportDict[sample].Print()
        #RDFtrees[sample].saveGraph()

    print('all samples processed in {} s'.format(time.time()-start))

if __name__ == "__main__":
    main()

