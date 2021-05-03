#ifndef LUMIWEIGHT_H
#define LUMIWEIGHT_H

#include "module.hpp"

class lumiWeight : public Module
{

private:
    float _targetLumi;
    float _xsec;
    double _genEventSumw;
    bool _clip;

public:
  lumiWeight(float xsec, double sumw, float targetLumi = 35.9, bool clip=false)
    {
        _targetLumi = targetLumi;
        _xsec = xsec/ 0.001;
        _genEventSumw = sumw;
        _clip = clip;
    };

    ~lumiWeight(){};

    RNode run(RNode) override;
};

#endif
