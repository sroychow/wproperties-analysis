#include "interface/functions.hpp"
#include "interface/rochesterWeights.hpp"
RNode rochesterWeights::run(RNode d)
{
  
  auto defineRochweights = [this](float pt, float eta) {
    ROOT::VecOps::RVec<float> RochesterVars;
    RochesterVars.emplace_back(getCorrfromhisto(_Zptcorv, pt, eta, 0));
    RochesterVars.emplace_back(getCorrfromhisto(_Zptcorv, pt, eta, 1));
    RochesterVars.emplace_back(getCorrfromhisto(_Ewkcorv, pt, eta, 0));
    RochesterVars.emplace_back(getCorrfromhisto(_Ewkcorv, pt, eta, 1));
    RochesterVars.emplace_back(getCorrfromhisto(_deltaMcorv, pt, eta, 0));
    RochesterVars.emplace_back(getCorrfromhisto(_deltaMcorv, pt, eta, 1));
    RochesterVars.emplace_back(getCorrfromhisto(_Ewk2corv, pt, eta, 0));
    RochesterVars.emplace_back(getCorrfromhisto(_Ewk2corv, pt, eta, 1));
    for (unsigned int idx = 0; idx < 99; idx++) {
      RochesterVars.emplace_back(getCorrfromhisto(_statUpv, pt, eta, idx));
      RochesterVars.emplace_back(getCorrfromhisto(_statDownv, pt, eta, idx));
    }
    return RochesterVars;
  };

  auto df = d.Define("rochWeights", defineRochweights, {"Mu1_pt", "Mu1_eta"});

  return df;
}

float rochesterWeights::getCorrfromhisto(std::vector<TH2D *> hvec, float pt, float eta, unsigned int idx)
{
  return  hvec.at(idx)->GetBinContent(hvec.at(idx)->FindBin(eta, pt));
};
