#ifndef LUMIWEIGHT_H
#define LUMIWEIGHT_H

#include "module.hpp"

class lumiWeight : public Module
{

private:
    float _targetLumi;
    float _xsec;

public:
    lumiWeight(float xsec, float targetLumi = 35.9)
    {
        _targetLumi = targetLumi;
        _xsec = xsec/ 0.001;
    };

    ~lumiWeight(){};

    RNode run(RNode) override;
};

#endif
