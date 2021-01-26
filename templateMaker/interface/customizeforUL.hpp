#ifndef CUSTOMIZEFORUL_H
#define CUSTOMIZEFORUL_H

#include "module.hpp"

class customizeforUL : public Module
{

private:
    bool isMC_;
    bool isWorZMC_;

public:
  customizeforUL(bool isMC = true, bool isWorZMC = false)//changing isWorZMC to false so that we are aware in the configs!
  {
    isMC_ = isMC;
    isWorZMC_ = isWorZMC;
  };

    ~customizeforUL(){};

    RNode run(RNode) override;
};

#endif
