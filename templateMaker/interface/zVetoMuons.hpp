#ifndef ZVETOMUONS_H
#define ZVETOMUONS_H

#include "module.hpp"

class zVetoMuons : public Module {

    public:
    zVetoMuons() {
    };
    ~zVetoMuons() {};
    RNode run(RNode) override;
};
#endif
