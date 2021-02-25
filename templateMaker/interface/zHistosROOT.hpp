#ifndef ZHISTOSROOT_H
#define ZHISTOSROOT_H

#include "module.hpp"
#include<map>
#include<vector>
//This is FOR QUICK Validation untill boost histo issue is fixed

class zHistosROOT : public Module {

    private:

    std::vector<std::string> _syst_name;
    std::string _syst_weight;

    std::string _weight;

    std::vector<float> _pTArr = std::vector<float>(41);
    std::vector<float> _etaArr = std::vector<float>(49);
    std::vector<float> _METArr = std::vector<float>(75);
    std::vector<float> _ZmassArr = std::vector<float>(60);
    std::vector<float> _qtArr = {0., 4., 8., 12., 16., 20., 24., 28., 32., 40., 60., 100., 200.};

    void setAxisarrays();

    public:
    
    zHistosROOT(std::string weight, std::vector<std::string> syst_name, std::string syst_weight){
        
        _weight = weight;
        _syst_name = syst_name;
        _syst_weight = syst_weight;
        setAxisarrays();

    };

    ~zHistosROOT() {};

    RNode run(RNode) override;
};

#endif
