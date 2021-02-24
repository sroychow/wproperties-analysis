#include "SF_ul.hpp"
#include "functions.hpp"
RNode SF_ul::run(RNode d)
{

    auto defineSFZ = [this](float pt1, float eta1, int charge1, bool istrigMatched1, float pt2, float eta2, int charge2) {
        /*
    @SRC Note: here we choose muon of one charge(set from config) as primary or preferred muon in 
    a dimuon event. This muon is trigger matched. All the SFs shall be applied for this muon. 
    Whereas, for the other muon, only the tracking and ID SF is appled.
    **The default charge is +ve;
      */
        float sf = 1.;
        sf *= getValFromTH2(*_tracking, eta1, pt1);
        sf *= getValFromTH2(*_idip, eta1, pt1);
        sf *= getValFromTH2(*_iso, eta1, pt1);

        if (charge1 > 0) sf *= getValFromTH2(*_trigger_plus, eta1, pt1);
        else sf *= getValFromTH2(*_trigger_minus, eta1, pt1);

        sf *= getValFromTH2(*_tracking, eta2, pt2);
        sf *= getValFromTH2(*_idip, eta2, pt2);
        sf *= getValFromTH2(*_iso_notrig, eta2, pt2);
    
        return sf;
    };

    auto defineSF = [this](float pt1, float eta1, float charge1, float iso1) {
        int binTracking1 = _tracking->FindBin(eta1, pt1);
        int binTrigger1 = _trigger_plus->FindBin(eta1, pt1);
        int binIso1 = _iso->FindBin(eta1, pt1);
        int binAntiiso1 = _antiiso->FindBin(eta1, pt1);
        int binIdip1 = _idip->FindBin(eta1, pt1);

        float SFiso1 = -9999999.;
        if (iso1 >= 0.15)
            SFiso1 = _antiiso->GetBinContent(binAntiiso1);
        else
            SFiso1 = _iso_notrig->GetBinContent(binIso1);

        float SFtrigger1 = -9999999.;
        if (charge1 > 0.)
            SFtrigger1 = _trigger_plus->GetBinContent(binTrigger1);
        else
            SFtrigger1 = _trigger_minus->GetBinContent(binTrigger1);

        float SFtracking1 = _tracking->GetBinContent(binTracking1);
        float SFidip1 = _idip->GetBinContent(binIdip1);

        return SFtracking1 * SFtrigger1 * SFidip1 * SFiso1;
    };

    if (_isZ)
    {
        auto d1 = d.Define("SF", defineSFZ, {"Mu1_pt", "Mu1_eta", "Mu1_charge", "Mu1_hasTriggerMatch", "Mu2_pt", "Mu2_eta", "Mu2_charge"});
        return d1;
    }
    else
    {
        auto d1 = d.Define("SF", defineSF, {"Mu1_pt", "Mu1_eta", "Mu1_charge", "Mu1_relIso"});
        return d1;
    }
}
