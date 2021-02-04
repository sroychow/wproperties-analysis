#include "getZmass.hpp"
#include "functions.hpp"
#include "TLorentzVector.h"

RNode getZmass::run(RNode d)
{
  auto getdimuonMass = [](ROOT::VecOps::RVec<float> mu_pt, ROOT::VecOps::RVec<float> mu_eta,
                          ROOT::VecOps::RVec<float> mu_phi, ROOT::VecOps::RVec<float> mu_mass,
                          int mu1idx, int mu2idx) {
    TLorentzVector mu1P;
    mu1P.SetPtEtaPhiM(mu_pt[mu1idx], mu_eta[mu1idx], mu_phi[mu1idx], mu_mass[mu1idx]);
    TLorentzVector mu2P;
    mu2P.SetPtEtaPhiM(mu_pt[mu2idx], mu_eta[mu2idx], mu_phi[mu2idx], mu_mass[mu2idx]);
    float mass = (mu1P + mu2P).M();
    return mass;
  };

  auto getdimuonPt = [](ROOT::VecOps::RVec<float> mu_pt, ROOT::VecOps::RVec<float> mu_eta,
                        ROOT::VecOps::RVec<float> mu_phi, ROOT::VecOps::RVec<float> mu_mass,
                        int mu1idx, int mu2idx) {
    TLorentzVector mu1P;
    mu1P.SetPtEtaPhiM(mu_pt[mu1idx], mu_eta[mu1idx], mu_phi[mu1idx], mu_mass[mu1idx]);
    TLorentzVector mu2P;
    mu2P.SetPtEtaPhiM(mu_pt[mu2idx], mu_eta[mu2idx], mu_phi[mu2idx], mu_mass[mu2idx]);
    float pt = (mu1P + mu2P).Pt();
    return pt;
  };

  auto getdimuonRapidity = [](ROOT::VecOps::RVec<float> mu_pt, ROOT::VecOps::RVec<float> mu_eta,
                              ROOT::VecOps::RVec<float> mu_phi, ROOT::VecOps::RVec<float> mu_mass,
                              int mu1idx, int mu2idx) {
    TLorentzVector mu1P;
    mu1P.SetPtEtaPhiM(mu_pt[mu1idx], mu_eta[mu1idx], mu_phi[mu1idx], mu_mass[mu1idx]);
    TLorentzVector mu2P;
    mu2P.SetPtEtaPhiM(mu_pt[mu2idx], mu_eta[mu2idx], mu_phi[mu2idx], mu_mass[mu2idx]);
    float y = (mu1P + mu2P).Rapidity();
    return y;
  };

  // careful: this requires opposite charge cut is applied!
  auto getByPosCharge = [](float var1, float var2, float charge1) {
    if (charge1 > 0)
      return var1;
    else
      return var2;
  };

  auto getByNegCharge = [](float var1, float var2, float charge1) {
    if (charge1 < 0)
      return var1;
    else
      return var2;
  };

  auto d1 = d.Define("Mu2_eta", getFromIdx, {"Muon_eta", "Idx_mu2"})
                .Define("Mu2_phi", getFromIdx, {"Muon_phi", "Idx_mu2"})
                .Define("Mu2_charge", getCharge, {"Muon_charge", "Idx_mu2"})
                .Define("Mu2_relIso", getFromIdx, {"Muon_pfRelIso04_all", "Idx_mu2"})
                .Define("Mu2_dz", getFromIdx, {"Muon_dz", "Idx_mu2"})
                .Define("Mu2_pt", getFromIdx, {"Muon_corrected_pt", "Idx_mu2"})
                .Define("Mu2_sip3d", getFromIdx, {"Muon_sip3d", "Idx_mu2"})
                .Define("Mu2_dxy", getFromIdx, {"Muon_dxy", "Idx_mu2"})
                .Define("Mu2_hasTriggerMatch", getIntFromIdx, {"Muon_hasTriggerMatch", "Idx_mu2"})
                .Define("dimuonMass", getdimuonMass, {"Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Idx_mu1", "Idx_mu2"})
                .Define("dimuonPt", getdimuonPt, {"Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Idx_mu1", "Idx_mu2"})
                .Define("dimuonY", getdimuonRapidity, {"Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass", "Idx_mu1", "Idx_mu2"})
                .Define("Mupos_pt", getByPosCharge, {"Mu1_pt", "Mu2_pt", "Mu1_charge"})
                .Define("Muneg_pt", getByNegCharge, {"Mu1_pt", "Mu2_pt", "Mu1_charge"})
                .Define("Mupos_eta", getByPosCharge, {"Mu1_eta", "Mu2_eta", "Mu1_charge"})
                .Define("Muneg_eta", getByNegCharge, {"Mu1_eta", "Mu2_eta", "Mu1_charge"});
  return d1;
}
