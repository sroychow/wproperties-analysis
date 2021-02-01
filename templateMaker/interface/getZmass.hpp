#ifndef GETZMASS_H
#define GETZMASS_H

#include "module.hpp"

class getZmass : public Module {

    private:

    bool _isData;
    public:
    getZmass(bool isData=false) {
        _isData = isData;
    };
    ~getZmass() {};
    RNode run(RNode) override;

};

#endif
