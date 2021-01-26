import ROOT

fileSFul = ROOT.TFile.Open("../Common/data/allSFs.root")
fileSF = ROOT.TFile.Open("../Common/data/ScaleFactors_OnTheFly.root")
filePt = ROOT.TFile.Open("../Common/data/histoUnfoldingSystPt_nsel2_dy3_rebin1_default.root")
fileY = ROOT.TFile.Open("../Common/data/histoUnfoldingSystRap_nsel2_dy3_rebin1_default.root")
