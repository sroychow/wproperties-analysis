#ifndef FUNCTIONS_H
#include "functions.hpp"
#include "TMath.h"

float getFromIdx(ROOT::VecOps::RVec<float> vec, int index){
	return vec[index];
}

int getIntFromIdx(ROOT::VecOps::RVec<int> vec, int index){
	return vec[index];
}

float deltaR(float eta1, float phi1, float eta2, float phi2)
{
  return std::sqrt(deltaR2(eta1, phi1, eta2, phi2));
}

float deltaR2(float eta1, float phi1, float eta2, float phi2)
{
  float deta = eta1 - eta2;
  float dphi = deltaPhi(phi1, phi2);
  return deta * deta + dphi * dphi;
}

float deltaPhi(float phi1, float phi2)
{
  float result = phi1 - phi2;
  while (result > float(M_PI))
    result -= float(2 * M_PI);
  while (result <= -float(M_PI))
    result += float(2 * M_PI);
  return result;
}
#endif

