#ifndef GETACVALUES_H
#define GETACVALUES_H

#include "module.hpp"

class getACValues : public Module
{

private:
  TFile *_AChistos_plus;
  TH2D *_hA0_plus;
  TH2D *_hA1_plus;
  TH2D *_hA2_plus;
  TH2D *_hA3_plus;
  TH2D *_hA4_plus;
  TH2D *_hA5_plus;
  TH2D *_hA6_plus;
  TH2D *_hA7_plus;
  TH2D *_hAUL_plus;
  TH2D *_htotMap_plus;

  TFile *_AChistos_minus;
  TH2D *_hA0_minus;
  TH2D *_hA1_minus;
  TH2D *_hA2_minus;
  TH2D *_hA3_minus;
  TH2D *_hA4_minus;
  TH2D *_hA5_minus;
  TH2D *_hA6_minus;
  TH2D *_hA7_minus;
  TH2D *_hAUL_minus;
  TH2D *_htotMap_minus;

public:
  getACValues(TFile *AChistos_plus, TFile *AChistos_minus)
  {
    _AChistos_plus = AChistos_plus;
    _hA0_plus = (TH2D *)_AChistos_plus->Get("xsecs_P0");
    _hA1_plus = (TH2D *)_AChistos_plus->Get("xsecs_P1");
    _hA2_plus = (TH2D *)_AChistos_plus->Get("xsecs_P2");
    _hA3_plus = (TH2D *)_AChistos_plus->Get("xsecs_P3");
    _hA4_plus = (TH2D *)_AChistos_plus->Get("xsecs_P4");
    _hA5_plus = (TH2D *)_AChistos_plus->Get("xsecs_P5");
    _hA6_plus = (TH2D *)_AChistos_plus->Get("xsecs_P6");
    _hA7_plus = (TH2D *)_AChistos_plus->Get("xsecs_P7");
    _htotMap_plus = (TH2D *)_AChistos_plus->Get("xsecs");

    _AChistos_minus = AChistos_minus;
    _hA0_minus = (TH2D *)_AChistos_minus->Get("xsecs_P0");
    _hA1_minus = (TH2D *)_AChistos_minus->Get("xsecs_P1");
    _hA2_minus = (TH2D *)_AChistos_minus->Get("xsecs_P2");
    _hA3_minus = (TH2D *)_AChistos_minus->Get("xsecs_P3");
    _hA4_minus = (TH2D *)_AChistos_minus->Get("xsecs_P4");
    _hA5_minus = (TH2D *)_AChistos_minus->Get("xsecs_P5");
    _hA6_minus = (TH2D *)_AChistos_minus->Get("xsecs_P6");
    _hA7_minus = (TH2D *)_AChistos_minus->Get("xsecs_P7");
    _htotMap_minus = (TH2D *)_AChistos_minus->Get("xsecs");
  };
  
  ~getACValues(){};

  RNode run(RNode) override;
  void getAngCoeff();
};

#endif
