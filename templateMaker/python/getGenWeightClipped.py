import ROOT
import json
import sys
import os

sys.path.append('../../Common/data')

ROOT.gInterpreter.Declare("""
#include "ROOT/RDataFrame.hxx"
#include "ROOT/RDF/RInterface.hxx"

using RNode = ROOT::RDF::RNode;

ROOT::RDF::RResultPtr<double> getClippedSumW(std::vector<std::string> fileNames)
{
  auto df = RNode(ROOT::RDataFrame("Events", fileNames));

  auto clipGenWeight = [](float Gen_weight) {
    double sign = Gen_weight / abs(Gen_weight);
    //return sign;                                                                                                                                                                                   
    double new_weight = double(std::min(fabs(Gen_weight), float(50118.72)));
    return sign * new_weight;
  };
  auto d1 = df.Define("Generator_weight_clipped", clipGenWeight, {"genWeight"}).Sum<double>("Generator_weight_clipped");
  return d1;
}
""")

from samples_2016_ul import samplespreVFP

def genwtsum(sample, fvec) :
    print("processing ", sample)
    
ROOT.ROOT.EnableImplicitMT(128)

#inDir='/scratchnvme/wmass/BARENANO/preVFP/'
inDir='/scratchnvme/wmass/BARENANO/postVFP/'
samples = samplespreVFP
sumwProc={}
sumwRunProc = {}
objList = []
for sample in samples:
    if 'data' in sample: continue
    computeYes= 'DY' in sample or 'WPlus' in sample or 'WMinus' in sample
    if not computeYes : continue
    fvec=ROOT.vector('string')()
    direc = samples[sample]['dir']
    for d in direc:
        targetDir='{}/{}/merged/'.format(inDir, d)
        for f in os.listdir(targetDir):
            if not f.endswith('.root'): continue
            inputFile=targetDir+f
            fvec.push_back(inputFile)
    if fvec.empty():
        print("No files found for directory:", samples[sample], " SKIPPING processing")
        continue
    print(fvec)  
    sumwProc[sample] = ROOT.getClippedSumW(fvec)
    objList.append(sumwProc[sample])

ROOT.RDF.RunGraphs(objList)

sumwClipped = {} 

for sample in samples:
    if sample not in sumwProc.keys() : continue
    sumwClipped[sample]=sumwProc[sample].GetValue()

with open('genSumWOutput.py', 'w') as fp:
    json.dump(sumwClipped, fp, indent=4)
