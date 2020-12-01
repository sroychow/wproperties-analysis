#include "interface/templates.hpp"
#include "interface/functions.hpp"
#include "interface/boostHweightsHelper.hpp"
#include "interface/TH3weightsHelper.hpp"

RNode templates::run(RNode d)
{

    auto d1 = d.Define("weight", _weight);
    if (_hcat == HistoCategory::Nominal)
        return bookNominalhistos(d1);
    else if (_hcat == HistoCategory::Corrected)
        return bookptCorrectedhistos(d1);
    else if (_hcat == HistoCategory::JME)
        return bookJMEvarhistos(d1);
    else
        std::cout << "Warning!! Histocategory undefined!!\n";
    return d1;
}

RNode templates::bookNominalhistos(RNode df)
{
   
    boostHweightsHelper helper(_name, _syst_name, _etaArr, _pTArr, _chargeArr, _mTArr, _isoArr);
    
    auto vec = [](float var1, float var2, float var3, float var4, float var5) { 
        ROOT::VecOps::RVec<float> vec;
        vec.emplace_back(var1);
        vec.emplace_back(var2);
        vec.emplace_back(var3);
        vec.emplace_back(var4);
        vec.emplace_back(var5);
        return vec; };
    
    auto templ = df.Define("vec", vec, {"Mu1_eta", "Mu1_pt", "Mu1_charge", "MT", "Mu1_relIso"})
                     .Book<ROOT::VecOps::RVec<float>, float, ROOT::VecOps::RVec<float>>(std::move(helper), {"vec", "weight", _syst_weight});
    _hNGroup.push_back(templ);

    return df;
}
//muon pt corrections affect both pt and MT
RNode templates::bookptCorrectedhistos(RNode df)
{
    for (unsigned int i = 0; i < _colvarvec.size(); i++)
    {
        TH3weightsHelper helper_Pt(std::string("templates" + _colvarvec[i]), std::string(" ; muon #{eta}; muon p_{T} (Rochester corr.); muon charge"), _etaArr.size() - 1, _etaArr, _pTArr.size() - 1, _pTArr, _chargeArr.size() - 1, _chargeArr, _syst_name);
        _h3Group.emplace_back(df.Filter(_filtervec[i]).Book<float, float, float, float, ROOT::VecOps::RVec<float>>(std::move(helper_Pt), {"Mu1_eta", "Mu1_pt" + _colvarvec[i], "Mu1_charge", "weight", "Nom"}));
    }
    return df;
}

//jme variations affect only MT
RNode templates::bookJMEvarhistos(RNode df)
{
    for (unsigned int i = 0; i < _colvarvec.size(); i++)
    {
        TH3weightsHelper helper_JME(std::string("templates" + _colvarvec[i]), std::string(" ; muon #{eta}; muon p_{T} (Rochester corr.); muon charge"), _etaArr.size() - 1, _etaArr, _pTArr.size() - 1, _pTArr, _chargeArr.size() - 1, _chargeArr, _syst_name);
        _h3Group.emplace_back(df.Filter(_filtervec[i]).Book<float, float, float, float, ROOT::VecOps::RVec<float>>(std::move(helper_JME), {"Mu1_eta", "Mu1_pt", "Mu1_charge", "weight", "Nom"}));
    }
    return df;
}

void templates::setAxisarrays()
{
    for (unsigned int i = 0; i < 61; i++)
    {
        float binSize = (55. - 25.) / 60;
        _pTArr[i] = 25. + i * binSize;
    }
    for (unsigned int i = 0; i < 49; i++){
        _etaArr[i] = -2.4 + i * 4.8 / 48;
    }
    for (int i = 0; i < 3; i++){
        _chargeArr[i] = -2. + i * 2.;
    }
    _mTArr[0]=0.;
    _mTArr[1]=30.;
    _mTArr[2]=40.;
    _mTArr[3]=200.;
    _isoArr[0]=0.;
    _isoArr[1]=0.15;
    _isoArr[2]=1.;
}
