#ifndef SF_UL_H
#define SF_UL_H

#include "module.hpp"

class SF_ul : public Module
{

private:
    TFile *_SF;
    TH2D *_tracking;
    TH2D *_idip;
    TH2D *_trigger_plus;
    TH2D *_trigger_minus;
    TH2D *_iso;
    TH2D *_antiiso;
    bool _isZ;
    //this is only relevant for Z studies
    int _prefCharge;

public:
  SF_ul(TFile *SF, bool isZ = false, int prefCharge = 1)
    {
        _SF = SF;
        _isZ = isZ;
        _tracking = (TH2D *)_SF->Get("SF2D_tracking_BtoF_both");
        _idip = (TH2D *)_SF->Get("SF2D_idip_BtoF_both");
        _trigger_plus = (TH2D *)_SF->Get("SF2D_trigger_BtoF_plus");
        _trigger_minus = (TH2D *)_SF->Get("SF2D_trigger_BtoF_minus");
        _iso = (TH2D *)_SF->Get("SF2D_iso_BtoF_both");
        _antiiso = (TH2D *)_SF->Get("SF2D_antiiso_BtoF_both");
	prefCharge = _prefCharge;
    };
    ~SF_ul(){};

    RNode run(RNode) override;
};

#endif
