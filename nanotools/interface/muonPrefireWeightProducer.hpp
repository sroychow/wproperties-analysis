#ifndef MUONPREFIREWEIGHTPRODUCER_H
#define MUONPREFIREWEIGHTPRODUCER_H

#include "module.hpp"
#include<string>
class muonPrefireWeightProducer : public Module {
private:
  TFile* _wtfile;
  TH1F* _hwt;
public:

  muonPrefireWeightProducer(TFile* wtfile, int era) {
    _wtfile = wtfile;
    if(era==1) {
      _hwt = (TH1F*)(_wtfile->Get("muonPrefiring_preVFP"));
      std::cout << "muonPrefireWeightProducer::Read histo muonPrefiring_preVFP" << std::endl;
    }
    else if(era==2) {
      _hwt = (TH1F*)(_wtfile->Get("muonPrefiring_postVFP"));
      std::cout << "muonPrefireWeightProducer::Read histo muonPrefiring_postVFP" << std::endl;
    }
    else 
      std::cout << "Wrong era code passed to muon prefire weight producer" << std::endl;
  };
  ~muonPrefireWeightProducer() {};
  RNode run(RNode) override;
  
};

#endif
