#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "ROOT/RDF/RInterface.hxx"

ROOT::VecOps::RVec<float> dummy(ULong64_t event);
float getFromIdx(ROOT::VecOps::RVec<float> vec, int index);
int getIntFromIdx(ROOT::VecOps::RVec<int> vec, int index);
float deltaR(float eta1, float phi1, float eta2, float phi2);
float deltaR2(float eta1, float phi1, float eta2, float phi2);
float deltaPhi(float phi1, float phi2);
