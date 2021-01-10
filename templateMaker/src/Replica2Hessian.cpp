#include "PDFWeightsHelper.hpp"
#include "Replica2Hessian.hpp"


RNode Replica2Hessian::run(RNode d)
{

  auto newPDFweights = [this](ROOT::VecOps::RVec<float> replicas, float lhenom, unsigned long long ev) {
    std::vector<float> raw_weights;

    for (unsigned int i = 0; i < nPdfWeights_; i++)
    {
      raw_weights.push_back(replicas[i] * lhenom);
    }
    std::vector<float> raw_Hessweights;
    raw_Hessweights.resize(nPdfEigWeights_);

    pdfweightshelper_.DoMC2Hessian(lhenom, raw_weights.data(), raw_Hessweights.data());
    raw_Hessweights.push_back(1.);
    for (unsigned int i = 1; i < nPdfEigWeights_ + 1; i++)
    {
      raw_Hessweights[i] = raw_Hessweights[i] / lhenom;
    }
    return ROOT::VecOps::RVec<float>(raw_Hessweights);
  };

  auto getalphaSvarVec = [this](float wup, float wdown) {
    ROOT::VecOps::RVec<float> alpS;
    alpS.emplace_back(1.);
    alpS.emplace_back(wup);
    alpS.emplace_back(wdown);
    return alpS;
  };

  auto d1 = d.Define("nLHEPdfWeightHess", [this]() { return nPdfEigWeights_ - 1; })
             .Define("LHEPdfWeightHess", newPDFweights, {"LHEPdfWeight", "LHEWeight_originalXWGTUP", "event"})
             .Define("alphaSUp", [this](ROOT::VecOps::RVec<float> pdfs, unsigned int npdfs) {return pdfs[npdfs-1];}, {"LHEPdfWeight", "nLHEPdfWeight"})
             .Define("alphaSDown", [this](ROOT::VecOps::RVec<float> pdfs, unsigned int npdfs) {return pdfs[npdfs-2];}, {"LHEPdfWeight", "nLHEPdfWeight"})
             .Define("alphaSVars", getalphaSvarVec, {"alphaSUp", "alphaSDown"});

  // add variations for PDF
  std::vector<std::string> PDFVars;
  PDFVars.push_back("");
  for(int i=1;i<61;i++) PDFVars.push_back("pdf_"+ std::to_string(i));
  Replica2Hessian::vary("LHEPdfWeightHess", true, PDFVars);

  // add variations for alphaS
  std::vector<std::string> alphaS = {"", "alphaSUp", "alphaSDown"};
  Replica2Hessian::vary("alphaSVars", true, alphaS);

  return d1;
}
