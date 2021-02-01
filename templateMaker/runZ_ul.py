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
from binning import ptBins, etaBins, mTBins, etaBins, isoBins, chargeBins, zmassBins, qtBins
from externals import fileSFul
sys.path.append('python/')
from getLumiWeight import getLumiWeight
from genSumWClipped import sumwClippedDict

ROOT.gSystem.Load('bin/libAnalysisOnData.so')
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")

def RDFprocess(fvec, outputDir, sample, xsec, systType, sumwClipped, pretendJob):
    print("processing ", sample)
    p = RDFtree(outputDir = outputDir, inputFile = fvec, outputFile="{}.root".format(sample), pretend=pretendJob)
    p.EventFilter(nodeToStart='input', nodeToEnd='defs', evfilter="Vtype==2", filtername="{:20s}".format("Vtype multilepton selection"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Idx_mu1>-1 && Idx_mu2>-1", filtername="{:20s}".format("Atleast 2 mu"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="nVetoElectrons==0", filtername="{:20s}".format("Electron veto"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="HLT_SingleMu24", filtername="{:20s}".format("Pass HLT"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Muon_hasTriggerMatch[Idx_mu1] && Muon_hasTriggerMatch[Idx_mu2]", filtername="{:20s}".format("Both mu trigger matched"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Vtype_subcat == 0", filtername="{:20s}".format("Opposite Charge and loose isolation"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Muon_mediumId[Idx_mu1] == 1 && Muon_mediumId[Idx_mu2] == 1", filtername="{:20s}".format("MuonID"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Muon_pfRelIso04_all[Idx_mu1] < 0.15 && Muon_pfRelIso04_all[Idx_mu2] < 0.15", filtername="{:20s}".format("Both muon pass ISO"))  
    #note for customizeforUL(isMC=true, isWorZ=false)
    if systType == 0: #this is data
        p.branch(nodeToStart='defs', nodeToEnd='defs', modules=[ROOT.customizeforUL(False, False), ROOT.recoDefinitions(False, False)])
        p.branch(nodeToStart='defs', nodeToEnd='defs', modules=[ROOT.getZmass(isData=True)])
        #p.displayColumn(node="defs", columname="dimuonMass")
        p.Histogram(columns = ["dimuonMass", "Mu1_eta", "Mu1_pt", "dimuonPt", "dimuonY"], types = ['float']*5,node='defs',histoname=ROOT.string('data_obs'),bins = [zmassBins,etaBins, ptBins,qtBins, etaBins], variations = [])
        return p
    else:
        p.branch(nodeToStart = 'defs', nodeToEnd = 'defs', modules = [ROOT.lumiWeight(xsec=xsec, sumwclipped=sumwClipped, targetLumi = 19.3), ROOT.customizeforUL(True, False), ROOT.recoDefinitions(True, False)])
        p.branch(nodeToStart='defs', nodeToEnd='defs', modules=[ROOT.getZmass(),ROOT.SF_ul(fileSFul, isZ=True)])
        #p.displayColumn(node="defs", columname={"dimuonMass", "lumiweight", "puWeight", "SF"})
        p.Histogram(columns = ["dimuonMass", "Mu1_eta", "Mu1_pt", "Vpt_preFSR", "Vrap_preFSR", "lumiweight", "puWeight", "SF", "PrefireWeight"], types = ['float']*9,node='defs',histoname=ROOT.string('DY'),bins = [zmassBins,etaBins,ptBins,qtBins, etaBins], variations = [])
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
    ROOT.ROOT.EnableImplicitMT(64)
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
        sumwClipped=1.
        if systType == 2:
            sumwClipped=sumwClippedDict[sample]
            print(sample, sumwClipped)
        RDFtrees[sample] = RDFprocess(fvec, outputDir, sample, xsec, systType, sumwClipped, pretendJob)
    #sys.exit(0)
    #now trigger all the event loops at the same time:
    objList = []
    cutFlowreportDict = {}
    for sample in samples:
        if not 'DY' in sample and not 'data' in sample: continue
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
        if not 'DY' in sample and not 'data' in sample: continue
        print(sample)
        #RDFtrees[sample].getOutput()
        RDFtrees[sample].gethdf5Output()

    print('all samples processed in {} s'.format(time.time()-start))
if __name__ == "__main__":
    main()
