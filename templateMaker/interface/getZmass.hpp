#ifndef GETZMASS_H
#define GETZMASS_H

#include "module.hpp"

class getZmass : public Module {

    private:

    bool _isData;
    public:
    getZmass() {};
    ~getZmass() {};
    RNode run(RNode) override;

};

#endif
