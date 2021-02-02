#include "recoDefinitions.hpp"
#include "functions.hpp"

RNode recoDefinitions::run(RNode d)
{
    //define all nominal quantities // true for data and MC

    auto d1 = d.Define("Mu1_eta", getFromIdx, {"Muon_eta", "Idx_mu1"})
                  .Define("Mu1_phi", getFromIdx, {"Muon_phi", "Idx_mu1"})
                  .Define("Mu1_charge", getCharge, {"Muon_charge", "Idx_mu1"})
                  .Define("Mu1_relIso", getFromIdx, {"Muon_pfRelIso04_all", "Idx_mu1"})
                  .Define("Mu1_dz", getFromIdx, {"Muon_dz", "Idx_mu1"})
                  .Define("Mu1_pt", getFromIdx, {"Muon_corrected_pt", "Idx_mu1"})
                  .Define("Mu1_sip3d", getFromIdx, {"Muon_sip3d", "Idx_mu1"})
                  .Define("Mu1_dxy", getFromIdx, {"Muon_dxy", "Idx_mu1"})
                  .Define("Mu1_hasTriggerMatch", getIntFromIdx, {"Muon_hasTriggerMatch", "Idx_mu1"})
                  .Define("MT", W_mt, {"Mu1_pt", "Mu1_phi", "MET_pt_nom", "MET_phi_nom"})
                  .Define("Recoil_pt", W_hpt, {"Mu1_pt", "Mu1_phi", "MET_pt_nom", "MET_phi_nom"});

    //at this point return the node in case of data
    if (!_isMC)
        return d1;

    //now get variations // true only for MC
    auto d1withCompvar = d1.Define("Mu1_pt_correctedDown", getFromIdx, {"Muon_correctedDown_pt", "Idx_mu1"})
                             .Define("Mu1_pt_correctedUp", getFromIdx, {"Muon_correctedUp_pt", "Idx_mu1"})
                             .Define("MT_correctedUp", W_mt, {"Mu1_pt_correctedUp", "Mu1_phi", "MET_pt_nom", "MET_phi_nom"})
                             .Define("MT_correctedDown", W_mt, {"Mu1_pt_correctedDown", "Mu1_phi", "MET_pt_nom", "MET_phi_nom"})
                             //   .Define("MT_jerUp", W_mt, {"Mu1_pt", "Mu1_phi", "MET_pt_jerUp", "MET_phi_jerUp"})
                             //   .Define("MT_jerDown", W_mt, {"Mu1_pt", "Mu1_phi", "MET_pt_jerDown", "MET_phi_jerDown"})
                             .Define("MT_jesTotalUp", W_mt, {"Mu1_pt", "Mu1_phi", "MET_pt_jesTotalUp", "MET_phi_jesTotalUp"})
                             .Define("MT_jesTotalDown", W_mt, {"Mu1_pt", "Mu1_phi", "MET_pt_jesTotalDown", "MET_phi_jesTotalDown"})
                             .Define("MT_unclustEnUp", W_mt, {"Mu1_pt", "Mu1_phi", "MET_pt_unclustEnUp", "MET_phi_unclustEnUp"})
                             .Define("MT_unclustEnDown", W_mt, {"Mu1_pt", "Mu1_phi", "MET_pt_unclustEnDown", "MET_phi_unclustEnDown"});

    std::vector<std::string> JMEVars = {"jesTotalUp", "jesTotalDown", "unclustEnUp", "unclustEnDown"};
    // recoDefinitions::vary("MTVars", false, JMEVars);
    d1withCompvar = d1withCompvar.Define("MTVars", float2vec, {"MT", "MT_jesTotalUp", "MT_jesTotalDown", "MT_unclustEnUp", "MT_unclustEnDown"});

    return d1withCompvar;
}
