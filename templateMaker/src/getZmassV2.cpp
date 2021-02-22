#include "getZmassV2.hpp"
#include "functions.hpp"
#include "TLorentzVector.h"

RNode getZmassV2::run(RNode d) {
  auto getdimuonP4 = [](float mu1_pt, float mu1_eta, float mu1_phi, float mu2_pt, float mu2_eta, float mu2_phi) {
    TLorentzVector mu1P;
    mu1P.SetPtEtaPhiM(mu1_pt, mu1_eta, mu1_phi, 0.1057);
    TLorentzVector mu2P;
    mu2P.SetPtEtaPhiM(mu2_pt, mu2_eta, mu2_phi, 0.1057);
    //float mass = (mu1P + mu2P).M();
    return (mu1P + mu2P);
  };

  //+ve muon is mu1
  auto getprefmuonIdxFromCharge = [](RVec<int> mucharge) {
    RVec<int> prefidx;
    if(mucharge[0] > 0 && mucharge[1] < 0) {
      prefidx.emplace_back(0);
      prefidx.emplace_back(1);
    } else if (mucharge[0] < 0 && mucharge[1] > 0) {
      prefidx.emplace_back(1);
      prefidx.emplace_back(0);
    }
    return prefidx;
  };

  auto hasTriggerMatch = [](const float mueta, const float muphi, const RVec<float> &TrigObj_eta, const RVec<float> &TrigObj_phi) {
   bool muhasTrigm = false;
   for (unsigned int jtrig = 0; jtrig < TrigObj_eta.size(); ++jtrig) {
     if (deltaR(mueta, muphi, TrigObj_eta[jtrig], TrigObj_phi[jtrig]) < 0.3) {
       muhasTrigm = true;
       break;
     }//if
   }
   
   return muhasTrigm;
  };

  //.Define("Mu2_hasTriggerMatch", "Muon_hasTriggerMatch[prefIdx[1]]")

  auto d1 = d.Define("prefIdx", getprefmuonIdxFromCharge, {"Muon_charge"})
    .Define("Mu1_eta", "Muon_eta[prefIdx[0]]")
    .Define("Mu1_phi", "Muon_phi[prefIdx[0]]")
    .Define("Mu1_charge", "Muon_charge[prefIdx[0]]")
    .Define("Mu1_relIso", "Muon_pfRelIso04_all[prefIdx[0]]")
    .Define("Mu1_pt", "Muon_pt[prefIdx[0]]")
    .Define("Mu1_hasTriggerMatch", hasTriggerMatch, {"Mu1_eta", "Mu1_phi", "goodTrigObjs_eta", "goodTrigObjs_phi"})
    .Define("Mu2_eta", "Muon_eta[prefIdx[1]]")
    .Define("Mu2_phi", "Muon_phi[prefIdx[1]]")
    .Define("Mu2_charge", "Muon_charge[prefIdx[1]]")
    .Define("Mu2_relIso", "Muon_pfRelIso04_all[prefIdx[1]]")
    .Define("Mu2_pt", "Muon_pt[prefIdx[1]]")
    .Define("dimuonP4", getdimuonP4, {"Mu1_pt", "Mu1_eta", "Mu1_phi", "Mu2_pt", "Mu2_eta", "Mu2_phi"})
    .Define("dimuonMass", [this](TLorentzVector p){ return float(p.M());}, {"dimuonP4"})
    .Define("dimuonPt", [this](TLorentzVector p){ return float(p.Pt());}, {"dimuonP4"})
    .Define("dimuonY", [this](TLorentzVector p){ return float(p.Rapidity());}, {"dimuonP4"})
    .Define("nPV", [this](int p){ return float(1.*p);}, {"PV_npvsGood"}); 

  return d1;

}
