#include "filter.hpp"

RNode EventFilter::run(RNode d)
{
  auto d1 = d
    .Filter("(Vtype==0 || Vtype==1)", "Vtype selection")
    .Filter("HLT_SingleMu24", "Pass HLT")
    .Filter("MET_filters==1", "Pass MET filter")
    .Filter("nVetoElectrons==0", "Electron veto")
    .Filter("Idx_mu1>-1", "Event has atleast 1 muon");
  return d1;
                  
}
