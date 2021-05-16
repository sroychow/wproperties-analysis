#include "mtDefinitions.hpp"
#include "functions.hpp"

RNode mtDefinitions::run(RNode d)
{
    //define all nominal quantities // true for data and MC

   auto d1 = d.Define("MT", W_mt, {"Mu1_pt", "Mu1_phi", "MET_T1_pt", "MET_T1_phi"});
   if(!_isMC)
     return d1;

    // //now get variations // true only for MC
   auto d1withCompvar = d1.Define("MT_jerUp", W_mt, {"Mu1_pt", "Mu1_phi", "MET_T1_pt_jerUp", "MET_T1_phi_jerUp"})
                          .Define("MT_jerDown", W_mt, {"Mu1_pt", "Mu1_phi", "MET_T1_pt_jerDown", "MET_T1_phi_jerDown"})
                          .Define("MT_jesTotalUp", W_mt, {"Mu1_pt", "Mu1_phi", "MET_T1_pt_jesTotalUp", "MET_T1_phi_jesTotalUp"})
                          .Define("MT_jesTotalDown", W_mt, {"Mu1_pt", "Mu1_phi", "MET_T1_pt_jesTotalDown", "MET_T1_phi_jesTotalDown"})
                          .Define("MT_unclustEnUp", W_mt, {"Mu1_pt", "Mu1_phi", "MET_T1_pt_unclustEnUp", "MET_T1_phi_unclustEnUp"})
                          .Define("MT_unclustEnDown", W_mt, {"Mu1_pt", "Mu1_phi", "MET_T1_pt_unclustEnDown", "MET_T1_phi_unclustEnDown"});
   return d1withCompvar;
}
