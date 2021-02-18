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
from binning import ptBins, etaBins, mTBins, etaBins, isoBins, chargeBins, zmassBins, qtBins,metBins,pvBins
from externals import fileSFul,filePt, fileY
sys.path.append('python/')
from getLumiWeight import getLumiWeight
from genSumWClipped import sumwClippedDict

ROOT.gSystem.Load('bin/libAnalysisOnData.so')
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 2001;")

def RDFprocess(fvec, outputDir, sample, xsec, systType, sumwClipped, pretendJob):
    print("processing ", sample)
    p = RDFtree(outputDir = outputDir, inputFile = fvec, outputFile="{}.root".format(sample), pretend=pretendJob)
    p.branch(nodeToStart='input', nodeToEnd='defs', modules=[ROOT.getZmassV2()])
    
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="nVetoElectrons== 0 && nMuon>=2", filtername="{:20s}".format("twomuon"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="HLT_SingleMu24 > 0 ", filtername="{:20s}".format("Pass HLT"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="(Muon_charge[0] + Muon_charge[1] )== 0", filtername="{:20s}".format("Opposite charge"))
    #For cross-check
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Muon_mediumId[0] == 1 && Muon_mediumId[1] == 1", filtername="{:20s}".format("MuonID"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Muon_pfRelIso04_all[0] < 0.15 && Muon_pfRelIso04_all[1] < 0.15", filtername="{:20s}".format("both mu isolated"))
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="abs(Muon_dxy[0]) < 0.05 && abs(Muon_dxy[1]) < 0.05", filtername="{:20s}".format("dxy"))    
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="abs(Muon_dz[0]) < 0.2 && abs(Muon_dz[1]) < 0.2", filtername="{:20s}".format("dz"))
    
    p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="60. < dimuonMass && dimuonMass < 120.", filtername="{:20s}".format("mZ range"))
    #p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="Muon_hasTriggerMatch[0]", filtername="{:20s}".format("lead mu trig matched"))
    
    #note for customizeforUL(isMC=true, isWorZ=false)
    if systType == 0: #this is data
        p.Histogram(columns = ["dimuonMass", "Mu1_eta", "Mu1_pt", "Mu2_eta", "Mu2_pt"], types = ['float']*5,node='defs',histoname=ROOT.string('data_muons'),bins = [zmassBins, etaBins, ptBins, etaBins, ptBins], variations = [])
        
        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="abs(Mu1_eta) < 2.4 && abs(Mu2_eta) < 2.4 && Mu1_pt > 25. && Mu2_pt > 25. && Mu1_pt < 55. && Mu2_pt < 55.", filtername="{:20s}".format("mu pt eta acceptance"))

        p.Histogram(columns = ["dimuonMass", "dimuonPt", "dimuonY", "MET_T1_pt"], types = ['float']*4,node='defs',histoname=ROOT.string('data_dimuon'),bins = [zmassBins,qtBins, etaBins, metBins], variations = [])

        return p
    elif systType == 1:
        p.branch(nodeToStart = 'defs', nodeToEnd = 'defs', modules = [getLumiWeight(xsec=xsec, inputFile = fvec, genEvsbranch = "genEventSumw", targetLumi = 19.3), ROOT.SF_ul(fileSFul, isZ=True)])
        p.Histogram(columns = ["dimuonMass", "Mu1_eta", "Mu1_pt", "Mu2_eta", "Mu2_pt", "lumiweight", "puWeight", "SF"], types = ['float']*8,node='defs',histoname=ROOT.string('DY_muons'),bins = [zmassBins, etaBins, ptBins, etaBins, ptBins], variations = [])

        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="abs(Mu1_eta) < 2.4 && abs(Mu2_eta) < 2.4 && Mu1_pt > 25. && Mu2_pt > 25. && Mu1_pt < 55. && Mu2_pt < 55.", filtername="{:20s}".format("mu pt eta acceptance"))
        
        p.Histogram(columns = ["dimuonMass", "dimuonPt", "dimuonY", "MET_T1_pt", "lumiweight", "puWeight", "SF"], types = ['float']*7,node='defs',histoname=ROOT.string('DY_dimuon'),bins = [zmassBins,qtBins, etaBins,metBins], variations = [])
        return p
    else:
        p.branch(nodeToStart = 'defs', nodeToEnd = 'defs', modules = [ROOT.lumiWeight(xsec=xsec, sumwclipped=236188699235.12158, targetLumi = 19.3), ROOT.SF_ul(fileSFul, isZ=True)])
        p.Histogram(columns = ["dimuonMass", "Mu1_eta", "Mu1_pt", "Mu2_eta", "Mu2_pt", "lumiweight", "puWeight", "SF"], types = ['float']*8,node='defs',histoname=ROOT.string('DY_muons'),bins = [zmassBins, etaBins, ptBins, etaBins, ptBins], variations = [])

        p.EventFilter(nodeToStart='defs', nodeToEnd='defs', evfilter="abs(Mu1_eta) < 2.4 && abs(Mu2_eta) < 2.4 && Mu1_pt > 25. && Mu2_pt > 25. && Mu1_pt < 55. && Mu2_pt < 55.", filtername="{:20s}".format("mu pt eta acceptance"))        

        p.Histogram(columns = ["dimuonMass", "dimuonPt", "dimuonY", "MET_T1_pt", "lumiweight", "puWeight", "SF"], types = ['float']*7,node='defs',histoname=ROOT.string('DY_dimuon'),bins = [zmassBins,qtBins, etaBins,metBins], variations = [])
        return p

def main():
    parser = argparse.ArgumentParser("")
    parser.add_argument('-p', '--pretend',type=bool, default=False, help="run over a small number of event")
    parser.add_argument('-r', '--report',type=bool, default=False, help="Prints the cut flow report for all named filters")
    parser.add_argument('-o', '--outputDir',type=str, default='outputDY', help="output dir name")
    parser.add_argument('-i', '--inputDir',type=str, default='/scratchnvme/wmass/NanoAOD2016-ULV2/', help="input dir name")    
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
        if 'WPlus' in sample or 'WMinus' in sample: continue
        checkS= 'DYJetsToMuMu' in sample or 'data' in sample
        #print('CheckSample={}'.format(checkS))
        if not checkS : continue
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
        if 'WPlus' in sample or 'WMinus' in sample: continue
        checkS= 'DYJetsToMuMu' in sample or 'data' in sample
        if not checkS : continue
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
        if 'WPlus' in sample or 'WMinus' in sample: continue
        checkS= 'DYJetsToMuMu' in sample or 'data' in sample
        if not checkS : continue
        print(sample)
        #RDFtrees[sample].getOutput()
        RDFtrees[sample].gethdf5Output()
        if args.report: cutFlowreportDict[sample].Print()

    print('all samples processed in {} s'.format(time.time()-start))

#At some point this should be what we want
#p.Histogram(columns = ["dimuonMass", "Mu1_eta", "Mu1_pt", "Mu2_eta", "Mu2_pt", "dimuonPt", "dimuonY", "MET_T1_pt"], types = ['float']*8,node='defs',histoname=ROOT.string('data_muons'),bins = [zmassBins, etaBins, ptBins, etaBins, qtBins, etaBins, metBins], variations = [])
if __name__ == "__main__":
    main()




    
