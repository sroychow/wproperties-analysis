#ifndef GETZMASS_H
#define GETZMASS_H

#include "module.hpp"

class getZmass : public Module {

    private:

    public:
    getZmass() {};
    ~getZmass() {};
    RNode run(RNode) override;

};

#endif
