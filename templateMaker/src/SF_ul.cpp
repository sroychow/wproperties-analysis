#include "SF_ul.hpp"
#include "functions.hpp"
RNode SF_ul::run(RNode d){

    auto defineSFZ = [this](float pt1, float eta1, float charge1, float iso1, float pt2, float eta2, float charge2, float iso2) {
        int binTracking1 = _tracking->FindBin(eta1, pt1);
        int binTrigger1 = _trigger_plus->FindBin(eta1, pt1);
        int binIso1 = _iso->FindBin(eta1, pt1);
        int binIdip1 = _idip->FindBin(eta1, pt1);

        int binTracking2 = _tracking->FindBin(eta2, pt2);
        int binTrigger2 = _trigger_plus->FindBin(eta2, pt2);
        int binIso2 = _iso->FindBin(eta2, pt2);
        int binIdip2 = _idip->FindBin(eta2, pt2);

        float SFiso1 = -9999999.;
        if (iso1 > 0.15)
            SFiso1 = 1. - _iso->GetBinContent(binIso1);
        else
            SFiso1 = _iso->GetBinContent(binIso1);
        float SFiso2 = -9999999.;
        if (iso2 > 0.15)
            SFiso2 = 1. - _iso->GetBinContent(binIso2);
        else SFiso2 = _iso->GetBinContent(binIso2);

        float SFtrigger1 = -9999999.;
        if (charge1 > 0.)
            SFtrigger1 = _trigger_plus->GetBinContent(binTrigger1);
        else
            SFtrigger1 = _trigger_minus->GetBinContent(binTrigger1);

        float SFtrigger2 = -9999999.;
        if (charge2 > 0.)
            SFtrigger2 = _trigger_plus->GetBinContent(binTrigger2);
        else
            SFtrigger2 = _trigger_minus->GetBinContent(binTrigger2);

        float SFtracking1 = _tracking->GetBinContent(binTracking1);
        float SFidip1 = _idip->GetBinContent(binIdip1);
        float SFtracking2 = _tracking->GetBinContent(binTracking2);
        float SFidip2 = _idip->GetBinContent(binIdip2);

        return SFtracking1 * SFtrigger1 * SFidip1 * SFiso1 * SFtracking2 * SFtrigger2 * SFidip2 * SFiso2;
    };

    auto defineSF = [this](float pt1, float eta1, float charge1, float iso1){
        int binTracking1 = _tracking->FindBin(eta1, pt1);
        int binTrigger1 = _trigger_plus->FindBin(eta1, pt1);
        int binIso1 = _iso->FindBin(eta1, pt1);
        int binAntiiso1 = _antiiso->FindBin(eta1, pt1);
        int binIdip1 = _idip->FindBin(eta1, pt1);

        float SFiso1 = -9999999.;
        if (iso1 > 0.15)
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
        auto d1 = d.Define("SF", defineSFZ, {"Mu1_pt", "Mu1_eta", "Mu1_charge", "Mu1_relIso", "Mu2_pt", "Mu2_eta", "Mu2_charge", "Mu2_relIso"});
        return d1;
    }
    else{
        auto d1 = d.Define("SF", defineSF, {"Mu1_pt", "Mu1_eta", "Mu1_charge", "Mu1_relIso"});
        return d1;
    }
}
