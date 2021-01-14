#ifndef GENDEFINITIONS_H
#define GENDEFINITIONS_H

#include "module.hpp"

class genDefinitions : public Module
{

private:

public:

    ~genDefinitions(){};

    RNode run(RNode) override;
};
#endif
