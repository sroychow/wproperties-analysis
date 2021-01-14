#ifndef RECODEFINITIONS_H
#define RECODEFINITIONS_H

#include "module.hpp"

class recoDefinitions : public Module
{

private:
    bool _isMC;
    bool _isWjets;

public:
    recoDefinitions(bool isMC = 1, bool isWjets = 0){
      _isMC = isMC;
      _isWjets = isWjets;
    };
    ~recoDefinitions(){};

    RNode run(RNode) override;

};

#endif
