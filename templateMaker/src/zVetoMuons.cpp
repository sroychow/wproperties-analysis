#include "zVetoMuons.hpp"
#include "functions.hpp"
#include "TLorentzVector.h"

RNode zVetoMuons::run(RNode d) {

  auto d1 = d.Define("vetoMuons", "Muon_pt > 10 && Muon_isPFcand && abs(Muon_eta) < 2.4 && abs(Muon_dxy) < 0.05 && abs(Muon_dz)< 0.2")
    .Define("goodMuons",  "vetoMuons && Muon_pt > 26. && Muon_mediumId == 1"); 

  return d1;

}
