#ifndef GETZMASSV2_H
#define GETZMASSV2_H

#include "module.hpp"

class getZmassV2 : public Module {

    private:

    bool _isData;
    public:
    getZmassV2(bool isData=false) {
        _isData = isData;
    };
    ~getZmassV2() {};
    RNode run(RNode) override;

};

#endif
