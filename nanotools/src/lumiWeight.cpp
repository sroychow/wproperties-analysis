#include "lumiWeight.hpp"

RNode lumiWeight::run(RNode d)
{
    auto clipGenWeight = [](float Gen_weight) {
        float sign = Gen_weight / abs(Gen_weight);
        float new_weight = std::min(fabs(Gen_weight), float(50118.72));
        return sign * new_weight;
    };

    if(_clip){
        auto d1 = d.Define("Generator_weight_clipped", clipGenWeight, {"genWeight"}).Define("lumiweight", Form("float((%f*%f*Generator_weight_clipped)/(%f))", _targetLumi, _xsec, _genEventSumw));
        return d1;
    }
    else{
        auto d1 = d.Define("lumiweight", Form("float((%f*%f*Generator_weight)/(%f))", _targetLumi, _xsec, _genEventSumw));
        return d1;
    }
}
