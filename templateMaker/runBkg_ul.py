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
from genSumWClipped import sumwClippedDict
sys.path.append('python/')
from getLumiWeight import getLumiWeight
from binning import ptBins, etaBins, mTBins, isoBins, chargeBins
from externals import filePt, fileY, fileSFul

ROOT.gSystem.Load('bin/libAnalysisOnData.so')
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")

def RDFprocess(fvec, outputDir, sample, xsec, systType, sumwClipped, pretendJob):
    print("processing ", sample)
    p = RDFtree(outputDir = outputDir, inputFile = fvec, outputFile="{}.root".format(sample), pretend=pretendJob)
    #not for customizeforUL(isMC=true, isWorZ=false)
    if systType == 0: #this is data
        p.branch(nodeToStart='input', nodeToEnd='defs', modules=[ROOT.customizeforUL(False, False), ROOT.recoDefinitions(False, False)])
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="HLT_SingleMu24", filtername="{:20s}".format("Pass HLT"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="(Vtype==0 || Vtype==1)", filtername="{:20s}".format("Vtype selection"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="MET_filters==1", filtername="{:20s}".format("Pass MET filter"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="nVetoElectrons==0", filtername="{:20s}".format("Electron veto"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Idx_mu1>-1", filtername="{:20s}".format("Atleast 1 mu"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Muon_hasTriggerMatch[Idx_mu1]", filtername="{:20s}".format("mu trigger matched"))
        p.Histogram(columns = ["Mu1_eta","Mu1_pt","Mu1_charge","MT","Mu1_relIso"], types = ['float']*5,node='defs',histoname=ROOT.string('data_obs'),bins = [etaBins,ptBins,chargeBins,mTBins,isoBins], variations = [])
        return p
    elif systType < 2: #this is MC with no PDF variations
        p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.customizeforUL(True,False), ROOT.recoDefinitions(True, False),ROOT.lumiWeight(xsec=xsec, sumwclipped=sumwClipped, targetLumi = 19.3), ROOT.SF_ul(fileSFul)])
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="(Vtype==0 || Vtype==1)", filtername="{:20s}".format("Vtype selection"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="HLT_SingleMu24", filtername="{:20s}".format("Pass HLT"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="MET_filters==1", filtername="{:20s}".format("Pass MET filter"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="nVetoElectrons==0", filtername="{:20s}".format("Electron veto"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Idx_mu1>-1", filtername="{:20s}".format("Atleast 1 mu"))
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Muon_hasTriggerMatch[Idx_mu1]", filtername="{:20s}".format("mu trigger matched"))
        p.Histogram(columns = ["Mu1_eta","Mu1_pt","Mu1_charge","MT","Mu1_relIso", "lumiweight"], types = ['float']*6,node='defs',histoname=ROOT.string('ewk'),bins = [etaBins,ptBins,chargeBins,mTBins,isoBins], variations = [])
        
    else:
        if 'DY' in sample: #reweight full Z kinematics
            p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.customizeforUL(True, True), ROOT.recoDefinitions(True, False),ROOT.lumiWeight(xsec=xsec, sumwclipped=sumwClipped, targetLumi = 19.3), ROOT.SF_ul(fileSFul)])
            p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="(Vtype==0 || Vtype==1)", filtername="{:20s}".format("Vtype selection"))
            p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="HLT_SingleMu24", filtername="{:20s}".format("Pass HLT"))
            p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="MET_filters==1", filtername="{:20s}".format("Pass MET filter"))
            p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="nVetoElectrons==0", filtername="{:20s}".format("Electron veto"))
            p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Idx_mu1>-1", filtername="{:20s}".format("Aleast 1 mu"))
            p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Muon_hasTriggerMatch[Idx_mu1]", filtername="{:20s}".format("mu trigger matched"))
            p.Histogram(columns = ["Mu1_eta","Mu1_pt","Mu1_charge","MT","Mu1_relIso", "lumiweight"], types = ['float']*6,node='defs',histoname=ROOT.string('ewk'),bins = [etaBins,ptBins,chargeBins,mTBins,isoBins], variations = [])

        else:
            p.branch(nodeToStart = 'input', nodeToEnd = 'defs', modules = [ROOT.customizeforUL(True, True), ROOT.recoDefinitions(True, False),ROOT.lumiWeight(xsec=xsec, sumwclipped=sumwClipped, targetLumi = 19.3), ROOT.SF_ul(fileSFul)])
            p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="(Vtype==0 || Vtype==1)", filtername="{:20s}".format("Vtype selection"))
            p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="HLT_SingleMu24", filtername="{:20s}".format("Pass HLT"))
            p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="MET_filters==1", filtername="{:20s}".format("Pass MET filter"))
            p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="nVetoElectrons==0", filtername="{:20s}".format("Electron veto"))
            p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Idx_mu1>-1", filtername="{:20s}".format("Aleast 1 mu"))
            p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Muon_hasTriggerMatch[Idx_mu1]", filtername="{:20s}".format("mu trigger matched"))
            p.Histogram(columns = ["Mu1_eta","Mu1_pt","Mu1_charge","MT","Mu1_relIso", "lumiweight"], types = ['float']*6,node='defs',histoname=ROOT.string('ewk'),bins = [etaBins,ptBins,chargeBins,mTBins,isoBins], variations = [])


    return p

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-p', '--pretend',type=bool, default=False, help="run over a small number of event")
    parser.add_argument('-r', '--report',type=bool, default=False, help="Prints the cut flow report for all named filters")
    parser.add_argument('-o', '--outputDir',type=str, default='output', help="output dir name")
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
        if 'TTTo' in sample: continue
        direc = samples[sample]['dir']
        xsec = samples[sample]['xsec']
        sumwClipped=1.
        if not 'data' in sample:
            sumwClipped=sumwClippedDict[sample]
        print(sample, sumwClipped)
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
        RDFtrees[sample] = RDFprocess(fvec, outputDir, sample, xsec, systType, sumwClipped, pretendJob)
    #sys.exit(0)
    #now trigger all the event loops at the same time:
    objList = []
    cutFlowreportDict = {}
    for sample in samples:
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
        #RDFtrees[sample].getOutput()
        RDFtrees[sample].gethdf5Output()
        if args.report: cutFlowreportDict[sample].Print()

    print('all samples processed in {} s'.format(time.time()-start))
if __name__ == "__main__":
    main()
