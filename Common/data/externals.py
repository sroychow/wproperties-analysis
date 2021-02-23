import ROOT

#fileSFul = ROOT.TFile.Open("../Common/data/allSFs.root")
fileSFul = ROOT.TFile.Open("../Common/data/allSFs_eta0p1.root")
fileSF = ROOT.TFile.Open("../Common/data/ScaleFactors_OnTheFly.root")
filePt = ROOT.TFile.Open("../Common/data/histoUnfoldingSystPt_nsel2_dy3_rebin1_default.root")
fileY = ROOT.TFile.Open("../Common/data/histoUnfoldingSystRap_nsel2_dy3_rebin1_default.root")

pufile_mc_UL2016 = ROOT.TFile.Open("../Common/data/PileupMC_2016Legacy.root")
pufile_data_UL2016_allData = ROOT.TFile.Open("../Common/data/PileupData_2016Legacy_all2016.root")
pufile_data_UL2016_preVFP = ROOT.TFile.Open("../Common/data/PileupData_2016Legacy_upTo2016FwithHIPM.root")
pufile_data_UL2016_postVFP = ROOT.TFile.Open("../Common/data/PileupData_2016Legacy_FpostHIPMandGH.root")

