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
  std::vector<float> _METArr = std::vector<float>(76);
  std::vector<float> _ZmassArr = std::vector<float>(61);
  std::vector<float> _qtArr = {0., 4., 8., 12., 16., 20., 24., 28., 32., 40., 60., 100., 200.};
  std::vector<float> _gwArr = std::vector<float>(201); 
  std::vector<float> _cosThetaBins = {-1.0, -0.98, -0.96, -0.94, -0.92, -0.9, -0.88, -0.86, -0.84, -0.82, -0.8, -0.78, -0.76, -0.74, -0.72, -0.7, -0.68, -0.66, -0.64, -0.62, -0.6, -0.58, -0.56, -0.54, -0.52, -0.5, -0.48, -0.46, -0.44, -0.42, -0.4, -0.38, -0.36, -0.34, -0.32, -0.3, -0.28, -0.26, -0.24, -0.22, -0.2, -0.18, -0.16, -0.14, -0.12, -0.1, -0.08, -0.06, -0.04, -0.02, 0.0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.22, 0.24, 0.26, 0.28, 0.3, 0.32, 0.34, 0.36, 0.38, 0.4, 0.42, 0.44, 0.46, 0.48, 0.5, 0.52, 0.54, 0.56, 0.58, 0.6, 0.62, 0.64, 0.66, 0.68, 0.7, 0.72, 0.74, 0.76, 0.78, 0.8, 0.82, 0.84, 0.86, 0.88, 0.9, 0.92, 0.94, 0.96, 0.98, 1.0};

  std::vector<float> _phiBins = {0.0, 0.06, 0.13, 0.19, 0.25, 0.31, 0.38, 0.44, 0.5, 0.57, 0.63, 0.69, 0.75, 0.82, 0.88, 0.94, 1.01, 1.07, 1.13, 1.19, 1.26, 1.32, 1.38, 1.45, 1.51, 1.57, 1.63, 1.7, 1.76, 1.82, 1.88, 1.95, 2.01, 2.07, 2.14, 2.2, 2.26, 2.32, 2.39, 2.45, 2.51, 2.58, 2.64, 2.7, 2.76, 2.83, 2.89, 2.95, 3.02, 3.08, 3.14, 3.2, 3.27, 3.33, 3.39, 3.46, 3.52, 3.58, 3.64, 3.71, 3.77, 3.83, 3.9, 3.96, 4.02, 4.08, 4.15, 4.21, 4.27, 4.34, 4.4, 4.46, 4.52, 4.59, 4.65, 4.71, 4.78, 4.84, 4.9, 4.96, 5.03, 5.09, 5.15, 5.22, 5.28, 5.34, 5.4, 5.47, 5.53, 5.59, 5.65, 5.72, 5.78, 5.84, 5.91, 5.97, 6.03, 6.09, 6.16, 6.22, 6.28};

  
  void setAxisarrays();
  bool _isMC;
  
public:
  
  zHistosROOT(std::string weight, std::vector<std::string> syst_name, std::string syst_weight, bool isMC=true){
    
    _weight = weight;
    _syst_name = syst_name;
    _syst_weight = syst_weight;
    setAxisarrays();
    _isMC=isMC;
    
  };
  
  ~zHistosROOT() {};
  
  RNode run(RNode) override;
};

#endif
