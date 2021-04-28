#include "muonPrefireWeightProducer.hpp"
#include "functions.hpp"

RNode muonPrefireWeightProducer::run(RNode d) {
  //assumes that you pass muons with pt > 22 GeV & looseId
  auto goodMuonTriggerCandidate = [this](const RVec<float> mueta) {
    float pfw = 1.;
    for(auto& me : mueta) {
      auto wval = _hwt->GetBinContent(_hwt->FindFixBin(me));
      pfw*=(1.-wval);
    }
    return pfw;
  };

  auto d1 = d.Define("LooseMuonPt22_eta", "Muon_eta[Muon_pt > 22 && Muon_looseId]")
             .Define("muprefireWeight", goodMuonTriggerCandidate, {"LooseMuonPt22_eta"});
  return d1;
}
