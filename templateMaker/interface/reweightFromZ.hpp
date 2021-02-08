#ifndef REWEIGHTFROMZ_H
#define REWEIGHTFROMZ_H

#include "module.hpp"

class reweightFromZ : public Module
{

private:
    TFile *_Pt;
    TFile *_Y;

    TH1F *_hPt;
    TH1F *_hY;

    bool _isWJets;
    bool _isUL;

public:
    reweightFromZ(TFile *Pt, TFile *Y, const bool WJets = false, const bool isUL = false)
    {
        _Pt = Pt;
        _Y = Y;

        _hPt = (TH1F *)_Pt->Get("unfold");
        TH1F *hPtMC = (TH1F *)_Pt->Get("hDDilPtLL");
        _hY = (TH1F *)_Y->Get("unfold");
        TH1F *hYMC = (TH1F *)_Y->Get("hDDilRapLL");

        hPtMC->Scale(_hPt->Integral() / hPtMC->Integral());
        _hPt->Divide(hPtMC);

        hYMC->Scale(_hY->Integral() / hYMC->Integral());
        _hY->Divide(hYMC);

        _isWJets = WJets;
        _isUL = isUL;
    };
    ~reweightFromZ(){};

    RNode run(RNode) override;
};

#endif
