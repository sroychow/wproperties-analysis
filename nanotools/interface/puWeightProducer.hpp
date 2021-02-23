#ifndef PUWEIGHTPRODUCER_H
#define PUWEIGHTPRODUCER_H

#include "module.hpp"
#include "TString.h"
#include "TFile.h"
#include<vector>
#include<string>
class puWeightProducer : public Module
{

private:
    TFile *_puMC;
    TFile *_puData;
    TH1D *_hmc;
    TH1D *_hdata;
    bool _dosyst;
    bool _fixlargeW;
    bool _normtoArea;
    TH1D* _nompuwtH;
public:
  puWeightProducer(std::string hmcName, std::string hdataName, bool dosyst, bool fixlargeW, bool normtoArea)
    {
      
      _puData = TFile::Open("../Common/data/PileupData_2016Legacy_all2016.root");
      _puMC = TFile::Open("../Common/data/PileupMC_2016Legacy.root");
      _dosyst = dosyst;
      _fixlargeW = fixlargeW;
      _normtoArea = normtoArea;
      _hmc = (TH1D *)_puMC->Get(hmcName.c_str());
      //_hmc->SetDirectory(0);
      _hdata = (TH1D *)_puData->Get(hdataName.c_str());
      //_hdata->SetDirectory(0);

      _nompuwtH = ratio(_hmc, _hdata, "nom");
    };

  ~puWeightProducer(){
    
  };
  
  RNode run(RNode) override;
  
  TH1D* ratio(TH1D*,  TH1D*, TString); 
  void fixLargeWeights(std::vector<float> &weights, const std::vector<float> refvals, float maxshift,float hardmax);
  float checkIntegral(std::vector<float> wgt1, std::vector<float> wgt2, const std::vector<float> refvals);
};

#endif
