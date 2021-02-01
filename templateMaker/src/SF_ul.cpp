#include "SF_ul.hpp"
#include "functions.hpp"
RNode SF_ul::run(RNode d){

  auto defineSFZ = [this](float pt1, float eta1, float charge1, float iso1, int istrigMatched1, float pt2, float eta2, float charge2, float iso2, int istrigMatched2) {
      /*
	@SRC Note: here we choose muon of one charge(set from config) as primary or preferred muon in 
	a dimuon event. This muon is trigger matched. All the SFs shall be applied for this muon. 
	Whereas, for the other muon, only the tracking and ID SF is appled.
	**The default charge is +ve;
      */

      int binTracking1 = _tracking->FindBin(eta1, pt1);
      int binIdip1 = _idip->FindBin(eta1, pt1);
      int binTracking2 = _tracking->FindBin(eta2, pt2);
      int binIdip2 = _idip->FindBin(eta2, pt2);
      //this is always applied
      float combinedSF=_tracking->GetBinContent(binTracking1) * _idip->GetBinContent(binIdip1);
      combinedSF=_tracking->GetBinContent(binTracking2)*_idip->GetBinContent(binIdip2);

      if(_prefCharge == charge1 && istrigMatched1 > 0) {
	int binTrigger1 = _trigger_plus->FindBin(eta1, pt1);
	int binIso1 = _iso->FindBin(eta1, pt1);
        if (charge1 > 0.)
            combinedSF *= _trigger_plus->GetBinContent(binTrigger1);
        else
            combinedSF *= _trigger_minus->GetBinContent(binTrigger1);   
	
	combinedSF *= _iso->GetBinContent(binIso1);
      } else if(_prefCharge == charge2 && istrigMatched2 > 0) {
	int binTrigger2 = _trigger_plus->FindBin(eta2, pt2);
        int binIso2 = _iso->FindBin(eta2, pt2);	
        if (charge2 > 0.)
            combinedSF *= _trigger_plus->GetBinContent(binTrigger2);
        else
	  combinedSF *= _trigger_minus->GetBinContent(binTrigger2);
	combinedSF *=_iso->GetBinContent(binIso2);
      }
 
      //return SFtracking1 * SFtrigger1 * SFidip1 * SFiso1 * SFtracking2 * SFtrigger2 * SFidip2 * SFiso2;
      return combinedSF;
    };

    auto defineSF = [this](float pt1, float eta1, float charge1, float iso1){
        int binTracking1 = _tracking->FindBin(eta1, pt1);
        int binTrigger1 = _trigger_plus->FindBin(eta1, pt1);
        int binIso1 = _iso->FindBin(eta1, pt1);
        int binAntiiso1 = _antiiso->FindBin(eta1, pt1);
        int binIdip1 = _idip->FindBin(eta1, pt1);

        float SFiso1 = -9999999.;
        if (iso1 >= 0.15)
            SFiso1 = _antiiso->GetBinContent(binAntiiso1);
        else
            SFiso1 = _iso->GetBinContent(binIso1);

        float SFtrigger1 = -9999999.;
        if (charge1 > 0.)
            SFtrigger1 = _trigger_plus->GetBinContent(binTrigger1);
        else
            SFtrigger1 = _trigger_minus->GetBinContent(binTrigger1);

        float SFtracking1 = _tracking->GetBinContent(binTracking1);
        float SFidip1 = _idip->GetBinContent(binIdip1);

        return SFtracking1 * SFtrigger1 * SFidip1 * SFiso1;
    };

    if(_isZ){
        auto d1 = d.Define("SF", defineSFZ, {"Mu1_pt", "Mu1_eta", "Mu1_charge", "Mu1_relIso", "Mu1_hasTriggerMatch", "Mu2_pt", "Mu2_eta", "Mu2_charge", "Mu2_relIso", "Mu2_hasTriggerMatch"});
        return d1;
    }
    else{
        auto d1 = d.Define("SF", defineSF, {"Mu1_pt", "Mu1_eta", "Mu1_charge", "Mu1_relIso"});
        return d1;
    }
}
