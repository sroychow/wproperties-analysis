#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "interface/defineHarmonics.hpp"

RNode defineHarmonics::run(RNode d)
{

  // angular coefficients as defined in https://arxiv.org/pdf/1609.02536.pdf

  // auto getHarmonicsVec = [](float costheta, float phi) {
  //   float P0 = 1. / 2. * (1. - 3. * costheta * costheta);
  //   float P1 = 2. * costheta * sqrt(1. - costheta * costheta) * cos(phi);
  //   float P2 = 1. / 2. * (1. - costheta * costheta) * cos(2. * phi);
  //   float P3 = sqrt(1. - costheta * costheta) * cos(phi);
  //   float P4 = costheta;
  //   float P5 = (1. - costheta * costheta) * sin(2. * phi);
  //   float P6 = 2. * costheta * sqrt(1. - costheta * costheta) * sin(phi);
  //   float P7 = sqrt(1. - costheta * costheta) * sin(phi);
  //   float PUL = 1 + costheta * costheta;

  //   ROOT::VecOps::RVec<float> harms;

  //   harms.push_back(1.);
  //   harms.push_back(P0);
  //   harms.push_back(P1);
  //   harms.push_back(P2);
  //   harms.push_back(P3);
  //   harms.push_back(P4);
  //   harms.push_back(P5);
  //   harms.push_back(P6);
  //   harms.push_back(P7);
  //   harms.push_back(PUL);
  //   return harms;
  // };

  auto Sq = [](const ROOT::VecOps::RVec<float> &w) -> ROOT::VecOps::RVec<float> { return w * w; };

  auto d1 = d.Define("P0", "float(1. / 2. * (1. - 3. * CStheta_preFSR * CStheta_preFSR))")
                .Define("P1", "float(2. * CStheta_preFSR * sqrt(1. - CStheta_preFSR * CStheta_preFSR) * cos(CSphi_preFSR))")
                .Define("P2", "float(1. / 2. * (1. - CStheta_preFSR * CStheta_preFSR) * cos(2. * CSphi_preFSR))")
                .Define("P3", "float(sqrt(1. - CStheta_preFSR * CStheta_preFSR) * cos(CSphi_preFSR))")
                .Define("P4", "float(CStheta_preFSR)")
                .Define("P5", "float((1. - CStheta_preFSR * CStheta_preFSR) * sin(2. * CSphi_preFSR))")
                .Define("P6", "float(2. * CStheta_preFSR * sqrt(1. - CStheta_preFSR * CStheta_preFSR) * sin(CSphi_preFSR))")
                .Define("P7", "float(sqrt(1. - CStheta_preFSR * CStheta_preFSR) * sin(CSphi_preFSR))")
                .Define("PUL", "float(1 + CStheta_preFSR * CStheta_preFSR)");
                //.Define("harmonicsVecSq", Sq, {"harmonicsVec"});

  return d1;
}