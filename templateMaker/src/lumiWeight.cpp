#include "lumiWeight.hpp"

RNode lumiWeight::run(RNode d)
{
    auto clipGenWeight = [](float Gen_weight) {
        float sign = Gen_weight / abs(Gen_weight);
        float new_weight = std::min(fabs(Gen_weight), float(50000.));
        return sign * new_weight;
    };

    float genEventSumw = d.Define("Generator_weight_clipped", clipGenWeight, {"Generator_weight"}).Sum("Generator_weight_clipped").GetValue();

    auto d1 = d.Define("Generator_weight_clipped", clipGenWeight, {"Generator_weight"}).Define("lumiweight", Form("float((%f*%f*Generator_weight_clipped)/(%f))", _targetLumi, _xsec, genEventSumw));

    return d1;
}