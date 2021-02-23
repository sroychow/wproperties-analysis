#include "puWeightProducer.hpp"

RNode puWeightProducer::run(RNode d)
{
  auto getpuWeightNom = [this](float npu) {
    int bin = std::max(1, std::min(_nompuwtH->GetNbinsX(), _nompuwtH->GetXaxis()->FindBin(npu)));
    float puW = _nompuwtH->GetBinContent(bin);
    return puW;
  };
  auto df = d.Define("puWeight", getpuWeightNom, {"Pileup_nTrueInt"});
  return df;
}


TH1D* puWeightProducer::ratio(TH1D* hmc, TH1D* hdata, TString tag) {
  std::vector<float> refvals;
  for(int ibin=0; ibin<hmc->GetNcells(); ++ibin)   
    refvals.emplace_back(hmc->GetBinContent(ibin));

  if (_normtoArea) hmc->Scale(hdata->Integral()/hmc->Integral());

  std::vector<float> puWvec;
  for(int ibin=0; ibin<hdata->GetNcells(); ++ibin)  {
    float mcval   = hmc->GetBinContent(ibin);
    float dataval = hdata->GetBinContent(ibin);
    float weight = mcval != 0 ? dataval/mcval : 1;
    puWvec.emplace_back(weight);
  }
  
  if(_fixlargeW) fixLargeWeights(puWvec,refvals, 0.0025, 3);
  
  TH1D* hw = (TH1D*)hmc->Clone("hweights"+tag);
  for(int ibin=0; ibin<(int)puWvec.size(); ++ibin) 
    hw->SetBinContent(ibin, puWvec[ibin]);
  return hw;
}

      
void puWeightProducer::fixLargeWeights(std::vector<float> &weights, const std::vector<float> refvals, float maxshift,float hardmax) {
  float maxw = std::min(*(std::max_element(weights.begin(),weights.end())),float(5.));
  std::vector<float> cropped;
  while (maxw > hardmax) {
    cropped.clear();  
    for(int i=0; i<(int)weights.size(); ++i) cropped.push_back(std::min(maxw,weights[i]));
    float shift = checkIntegral(cropped,weights,refvals);
    if(fabs(shift) > maxshift) break;
    maxw *= 0.95;
  }
  maxw /= 0.95; 

  if (cropped.size()>0) {
      for(int i=0; i<(int)weights.size(); ++i) cropped[i] = std::min(maxw,weights[i]);
      float normshift = checkIntegral(cropped,weights,refvals);
      for(int i=0; i<(int)weights.size(); ++i) weights[i] = cropped[i]*(1-normshift);
  }
}

float puWeightProducer::checkIntegral(std::vector<float> wgt1, std::vector<float> wgt2, const std::vector<float> refvals) {
  float myint=0;
  float refint=0;
  for(int i=0; i<(int)wgt1.size(); ++i) {
    myint += wgt1[i]*refvals[i];
    refint += wgt2[i]*refvals[i];
  }
  return (myint-refint)/refint;
}
