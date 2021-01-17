#ifndef CUSTOMIZEFORUL_H
#define CUSTOMIZEFORUL_H

#include "module.hpp"

class customizeforUL : public Module
{

private:
    bool isMC_;
    bool isWJets_;

public:
    customizeforUL(bool isMC = 1, bool isWJets = true){
      isMC_ = isMC;
      isWJets_ = isWJets;
    };

    ~customizeforUL(){};

    RNode run(RNode) override;
};

#endif
