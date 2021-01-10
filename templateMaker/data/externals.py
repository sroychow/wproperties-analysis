import ROOT

fileSF = ROOT.TFile.Open("data/ScaleFactors_OnTheFly.root")
filePt = ROOT.TFile.Open("data/histoUnfoldingSystPt_nsel2_dy3_rebin1_default.root")
fileY = ROOT.TFile.Open("data/histoUnfoldingSystRap_nsel2_dy3_rebin1_default.root")
