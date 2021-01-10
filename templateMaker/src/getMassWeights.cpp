#include "getMassWeights.hpp"

RNode getMassWeights::run(RNode d)
{

  auto BreitWigner = [](float Q2, float M2, float G2) -> float {
    return 1. / ((Q2 - M2) * (Q2 - M2) + M2 * G2);
  };

  auto getBWVec = [&](float Q) {
    ROOT::VecOps::RVec<float> v;
    v.emplace_back(1.);
    float w1 = BreitWigner(Q * Q, 80.419002 * 80.419002, 2.0476 * 2.0476) /
         BreitWigner(Q * Q, 80.319002 * 80.319002, 2.0476 * 2.0476);
    v.emplace_back(w1);
    float w2 = BreitWigner(Q * Q, 80.419002 * 80.419002, 2.0476 * 2.0476) /
         BreitWigner(Q * Q, 80.519002 * 80.519002, 2.0476 * 2.0476);
    v.emplace_back(w2);
    
    return v;
  };

  auto d1 = d.Define("massWeights", getBWVec, {"Wmass_preFSR"});

  //define mass weights as variations
  std::vector<std::string> masses = {"", "massUp", "massDown"};
  getMassWeights::vary("massWeights", true, masses);
  return d1;
}
