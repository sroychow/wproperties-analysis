#ifndef MTDEFINITIONS_H
#define MTDEFINITIONS_H

#include "module.hpp"

class mtDefinitions : public Module
{

private:
    bool _isMC;

public:
    mtDefinitions(bool isMC = 1){
      _isMC = isMC;
    };
    ~mtDefinitions(){};

    RNode run(RNode) override;

};

#endif
