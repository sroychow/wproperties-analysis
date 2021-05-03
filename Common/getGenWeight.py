import ROOT
import json
import sys
import os

sys.path.append('data')

ROOT.gSystem.CompileMacro("getClippedSumW.cpp", "kO")
from samples_2016_ulCentral import samplespreVFP, samplespostVFP
eras = ["preVFP", "postVFP"]

def genwtsum(sample, fvec) :
    print("processing ", sample)

ROOT.ROOT.EnableImplicitMT(64)

inDir='/scratchnvme/wmass/'
for era in eras:
    samples = samplespreVFP if era=="preVFP" else samplespostVFP
    sumwProc={}
    sumwRunProc = {}
    objList = []
    for sample in samples:
        if 'data' in sample: continue
        computeYes= 'DY' in sample or 'WPlus' in sample or 'WMinus' in sample
        fvec=ROOT.vector('string')()
        direc = samples[sample]['dir']
        for d in direc:
            targetDir='{}/{}/'.format(inDir, d)
            for f in os.listdir(targetDir):
                if not f.endswith('.root'): continue
                inputFile=targetDir+f
                fvec.push_back(inputFile)
        if fvec.empty():
            print("No files found for directory:", samples[sample], " SKIPPING processing")
            continue
        # print(fvec)
        if computeYes: sumwProc[sample] = ROOT.getClippedSumW(fvec)
        else:
            RDF = ROOT.ROOT.RDataFrame
            runs = RDF('Runs', fvec)
            sumwProc[sample] = runs.Sum("genEventSumw")
        objList.append(sumwProc[sample])

    ROOT.RDF.RunGraphs(objList)

    sumwClipped = {} 

    for sample in samples:
        if sample not in sumwProc.keys() : continue
        sumwClipped[sample]=sumwProc[sample].GetValue()

    with open('genSumWOutput{}.py'.format(era), 'w') as fp:
        json.dump(sumwClipped, fp, indent=4)
