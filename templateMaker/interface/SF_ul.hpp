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
    TH2D *_iso_notrig;
    TH2D *_antiiso;
    bool _isZ;
    //this is only relevant for Z studies
    int _prefCharge;

public:
  SF_ul(TFile *SF, bool isZ = false, int prefCharge = 1)
    {
        _SF = SF;
        _isZ = isZ;
        _tracking = (TH2D *)_SF->Get("SF2D_tracking_BtoH_both");
        _idip = (TH2D *)_SF->Get("SF2D_idip_BtoH_both");
        _trigger_plus = (TH2D *)_SF->Get("SF2D_trigger_BtoH_plus");
        _trigger_minus = (TH2D *)_SF->Get("SF2D_trigger_BtoH_minus");
        _iso = (TH2D *)_SF->Get("SF2D_iso_BtoH_both");
        _iso_notrig = (TH2D *)_SF->Get("SF2D_isonotrig_BtoH_both");
        _antiiso = (TH2D *)_SF->Get("SF2D_antiiso_BtoH_both");
	_prefCharge = prefCharge;
    };
    ~SF_ul(){};

    RNode run(RNode) override;
};

#endif
