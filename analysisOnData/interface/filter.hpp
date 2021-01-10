#ifndef FILTER_H
#define FILTER_H

#include "module.hpp"

class EventFilter : public Module
{

public:
    EventFilter(){
    };
    ~EventFilter(){};

    RNode run(RNode) override;

};

#endif
