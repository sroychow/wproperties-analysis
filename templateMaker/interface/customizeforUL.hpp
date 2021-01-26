#ifndef CUSTOMIZEFORUL_H
#define CUSTOMIZEFORUL_H

#include "module.hpp"

class customizeforUL : public Module
{

private:
    bool isWorZMC_;

public:
  customizeforUL(bool isWorZMC = true)
  {
    isWorZMC_ = isWorZMC;
  };

    ~customizeforUL(){};

    RNode run(RNode) override;
};

#endif
