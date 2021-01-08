#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"
#include "interface/getWeights.hpp"

RNode getWeights::run(RNode d)
{

    auto getNorm = [](float Wpt, float Wrap, const ROOT::VecOps::RVec<float> &AngCoeff, ROOT::VecOps::RVec<float> harmonicsVec, float totMap) {
        
        float norm = 0.;
        for (unsigned int i = 1; i < harmonicsVec.size(); i++) //remove nom from loop
        { //loop over angular coefficients
            norm += (AngCoeff[i - 1] * harmonicsVec[i] * totMap); //sum Ai*Pi
        }

        float fact = 3. / (16. * TMath::Pi());
        norm *= fact;
        return norm;
    };

    auto getWeights = [](float norm, const ROOT::VecOps::RVec<float> &AngCoeff, const ROOT::VecOps::RVec<float> &harmonicsVec, float totMap) {
        
        ROOT::VecOps::RVec<float> harmweights;
        harmweights.push_back(1.); //nominal first
        
        float fact = 3. / (16. * TMath::Pi());
        for (unsigned int i = 1; i < harmonicsVec.size(); i++) //remove nom from loop
        {
            harmweights.push_back(fact * totMap * AngCoeff[i-1] * harmonicsVec[i] / norm);
        }
        return harmweights;
    };
    auto d1 = d.Define("norm", getNorm, {"Wpt_preFSR", "Wrap_preFSR_abs", "AngCoeffVec", "harmonicsVec", "totMap"})
                  .Define("harmonicsWeights", getWeights, {"norm", "AngCoeffVec", "harmonicsVec", "totMap"});

    //add weights as variations
    std::vector<std::string> helXsecs = {"", "L", "I", "T", "A", "P", "7", "8", "9", "UL"};
    getWeights::vary("harmonicsWeights", true, helXsecs);

    return d1;
}
