import os
import sys
sys.path.append('data/')
import h5py
from math import pi, sqrt
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from binning import ptBins, etaBins, isoBins, chargeBins, metBins, mTBins, yBins, qtBins
# from binning import mTBinsFull as mTBins
plt.style.use([hep.style.ROOT])
#hep.cms.label(loc=0, year=2016, lumi=35.9, data=True)
#hep.cms.text('Simulation')

folder_preVFP = "../config/outputW_preVFP/"
folder_postVFP = "../config/outputW_postVFP/"

WMuFiles = ["WPlusJetsToMuNu.hdf5"]
WTauFiles = ["WPlusJetsToTauNu.hdf5","WMinusJetsToTauNu.hdf5"]
DYFiles = ["DYJetsToMuMu_M50.hdf5","DYJetsToTauTau_M50.hdf5"]
TopFiles = ["ST_t-channel_muDecays.hdf5", "ST_t-channel_tauDecays.hdf5","ST_s-channel_4f_leptonDecays.hdf5","ST_t-channel_top_5f_InclusiveDecays.hdf5","TTToSemiLeptonic.hdf5", "TTTo2L2Nu.hdf5"]
DibosonFiles = ["WW.hdf5","WZ.hdf5"]
dataFiles = ["data.hdf5"]

# hadd files to bkg categories - sum preVFP and postVFP
histonames = ['ewk', 'ewk_sumw2']

def haddFiles(fileList, fname, histonames, shape):
    folders = [folder_preVFP, folder_postVFP]
    f = h5py.File('./'+fname+'.hdf5', mode='w')
    for name in histonames:
        dset = f.create_dataset(name=name, shape=shape, dtype='float64')
        tmp = np.zeros(shape,dtype='float64')
        for file in fileList:
            for folder in folders:
                ftmp = h5py.File(folder+file, mode='r+')
                tmp += ftmp[name][:]
        dset[...] = tmp
    return

shape = (len(etaBins)-1,len(ptBins)-1,len(chargeBins)-1,len(mTBins)-1,len(isoBins)-1)
haddFiles(dataFiles,"data",["data_obs"], shape)
haddFiles(WMuFiles,"Wmu",histonames, shape)
haddFiles(WTauFiles,"Wtau",histonames, shape)
haddFiles(DYFiles,"DY",histonames, shape)
haddFiles(TopFiles,"Top",histonames, shape)
haddFiles(DibosonFiles,"Diboson",histonames, shape)

fdata = h5py.File('./data.hdf5', mode='r+')
fWmu = h5py.File('./Wmu.hdf5', mode='r+')
fWtau = h5py.File('./Wtau.hdf5', mode='r+')
fDY = h5py.File('./DY.hdf5', mode='r+')
fTop = h5py.File('./Top.hdf5', mode='r+')
fDiboson = h5py.File('./Diboson.hdf5', mode='r+')

hdata = np.array(fdata['data_obs'][:])
# hWmu = np.array(fWmu['ewk'][:])
hWtau = np.array(fWtau['ewk'][:])
hWtau_sumw2 = np.array(fWtau['ewk_sumw2'][:])
hDY = np.array(fDY['ewk'][:])
hDY_sumw2 = np.array(fDY['ewk_sumw2'][:])
hTop = np.array(fTop['ewk'][:])
hTop_sumw2 = np.array(fTop['ewk_sumw2'][:])
hDiboson = np.array(fDiboson['ewk'][:])
hDiboson_sumw2 = np.array(fDiboson['ewk_sumw2'][:])

# write down shapes as fit input
fshapes = h5py.File('shapesWplus.hdf5', mode='w')

dset = fshapes.create_dataset(name='data_obs', shape=(len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1), dtype='float64')
dset[...] = hdata[:,:,-1,:,:] #select positive charge

dset = fshapes.create_dataset(name='Wtau', shape=(len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1), dtype='float64')
dset[...] = hWtau[:,:,-1,:,:] #select positive charge

dset = fshapes.create_dataset(name='Wtau_sumw2', shape=(len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1), dtype='float64')
dset[...] = hWtau_sumw2[:,:,-1,:,:] #select positive charge

dset = fshapes.create_dataset(name='DY', shape=(len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1), dtype='float64')
dset[...] = hDY[:,:,-1,:,:] #select positive charge

dset = fshapes.create_dataset(name='DY_sumw2', shape=(len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1), dtype='float64')
dset[...] = hDY_sumw2[:,:,-1,:,:] #select positive charge

dset = fshapes.create_dataset(name='Top', shape=(len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1), dtype='float64')
dset[...] = hTop[:,:,-1,:,:] #select positive charge

dset = fshapes.create_dataset(name='Top_sumw2', shape=(len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1), dtype='float64')
dset[...] = hTop_sumw2[:,:,-1,:,:] #select positive charge

dset = fshapes.create_dataset(name='Diboson', shape=(len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1), dtype='float64')
dset[...] = hDiboson[:,:,-1,:,:] #select positive charge

dset = fshapes.create_dataset(name='Diboson_sumw2', shape=(len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1), dtype='float64')
dset[...] = hDiboson_sumw2[:,:,-1,:,:] #select positive charge

# now hadd and write down W differential signal

shape = (len(etaBins)-1,len(ptBins)-1,len(chargeBins)-1,len(mTBins)-1,len(isoBins)-1, len(yBins)-1, len(qtBins)-1, 9)
histonames = ['signalTemplates', 'signalTemplates_sumw2']
haddFiles(WMuFiles,"WmuSignal",histonames, shape)

fsignal = h5py.File('./WmuSignal.hdf5', mode='r+')

threshold_y = np.digitize(2.4,yBins)-1
threshold_qt = np.digitize(60.,qtBins)-1

# signal: differential in y,pt and helicity
hsignal = np.array(fsignal['signalTemplates'][:])[:,:,-1,...,:threshold_y+1,:threshold_qt+1,:]
hsignal_sumw2 = np.array(fsignal['signalTemplates_sumw2'][:])[:,:,-1,...,:threshold_y+1,:threshold_qt+1,:]

# sum of all helicities = total diff xsec
hdifftot = np.sum(np.array(fsignal['signalTemplates'][:]),axis=-1)
hdifftot_sumw2 = np.sum(np.array(fsignal['signalTemplates_sumw2'][:]),axis=-1)

hWmu = np.sum(np.array(hdifftot[...,:threshold_y,:threshold_qt]),axis=(5,6))

# events falling out of fit range
hlowacc = np.sum(hdifftot[...,threshold_y:,threshold_qt:],axis=(-1,-2))+np.sum(hdifftot[...,threshold_y:,:threshold_qt],axis=(-1,-2))+np.sum(hdifftot[...,:threshold_y,threshold_qt:],axis=(-1,-2))
hlowacc_sumw2 = np.sum(hdifftot_sumw2[...,threshold_y:,threshold_qt:],axis=(-1,-2))+np.sum(hdifftot_sumw2[...,threshold_y:,:threshold_qt],axis=(-1,-2))+np.sum(hdifftot_sumw2[...,:threshold_y,threshold_qt:],axis=(-1,-2))

print(hWmu.shape, hlowacc.shape, hWtau.shape)
hewk = hWmu+hlowacc+hWtau+hDY+hTop+hDiboson

fig, ax1 = plt.subplots()
ax1.set_title("total xsec closure", fontsize=18)
hep.hist2dplot(np.sum(hdifftot,axis=(5,6))[:,:,-1,1,0],etaBins,ptBins)
plt.savefig("testprefit/total_xsec_clos")
plt.clf()
fig, ax1 = plt.subplots()
ax1.set_title("total xsec closure", fontsize=18)
hep.hist2dplot(hsignal[:,:,1,0,0,2,-1],etaBins,ptBins)
plt.savefig("testprefit/templ")
plt.clf()
fig, ax1 = plt.subplots()
ax1.set_title("total xsec closure", fontsize=18)
hep.histplot(np.sum(hdifftot,axis=(1,5,6))[:,-1,1,0],etaBins)
plt.savefig("testprefit/total_xsec_clos_eta")
plt.clf()
fig, ax1 = plt.subplots()
ax1.set_title("total xsec closure", fontsize=18)
hep.histplot(np.sum(hdifftot,axis=(0,5,6))[:,-1,1,0],ptBins)
plt.savefig("testprefit/total_xsec_clos_pt")
plt.clf()

dset = fshapes.create_dataset(name='template', shape=hsignal.shape, dtype='float64')
dset[...] = hsignal #select positive charge

dset = fshapes.create_dataset(name='template_sumw2', shape=hsignal.shape, dtype='float64')
dset[...] = hsignal_sumw2 #select positive charge

dset = fshapes.create_dataset(name='lowacc', shape=(len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1), dtype='float64')
dset[...] = hlowacc[:,:,-1,:,:] #select positive charge

dset = fshapes.create_dataset(name='lowacc_sumw2', shape=(len(etaBins)-1,len(ptBins)-1,len(mTBins)-1,len(isoBins)-1), dtype='float64')
dset[...] = hlowacc_sumw2[:,:,-1,:,:] #select positive charge

# helicity xsecs without acceptance cuts for unfolding
file_preVFP = '../config/outputW_preVFP/WPlusJetsToMuNu_helweights.hdf5'
file_postVFP = '../config/outputW_postVFP/WPlusJetsToMuNu_helweights.hdf5'

f_preVFP = h5py.File(file_preVFP, mode='r+')
f_postVFP = h5py.File(file_postVFP, mode='r+')

# merge pre and post VFP xsecs
htot_preVFP = f_preVFP['totxsecs'][:]
htot_postVFP = f_postVFP['totxsecs'][:]
h_preVFP = f_preVFP['xsecs'][:]
h_postVFP = f_postVFP['xsecs'][:]

yBins = f_preVFP['edges_totxsecs_0'][:]
qtBins = f_preVFP['edges_totxsecs_1'][:]

htot = htot_preVFP+htot_postVFP
h = h_preVFP+h_postVFP
factors = np.array([[20./3., 1./10],[5.,0.],[20.,0.],[4.,0.],[4.,0.],[5.,0.],[5.,0.],[4.,0.],[1.,0.]])
factors = factors[np.newaxis,np.newaxis,...]
print(factors.shape)
h = (h/htot[...,np.newaxis]+factors[...,1])*factors[...,0]

factors_hel = np.array([2.,2*sqrt(2),4.,4.*sqrt(2),2.,2.,2.*sqrt(2),4.*sqrt(2),1.])
factors_hel = factors_hel[np.newaxis,np.newaxis,...]
h = 3./(16.*pi)*h*htot[...,np.newaxis]/factors_hel[...,:threshold_y+1,:threshold_qt+1,:]

dset = fshapes.create_dataset(name='helicity', shape=h.shape, dtype='float64')
dset[...] = h #select positive charge

# get prefit estimate of shape and normalisation of QCD bkg

hfakesLowMt = hdata[:,:,-1,:,:]-hewk[:,:,-1,:,:]
hfakesLowMt[:,:,1,:] = np.zeros([len(etaBins)-1,len(ptBins)-1,len(isoBins)-1], dtype='float64')
dset = fshapes.create_dataset(name='fakesLowMt', shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
dset[...] = hfakesLowMt.flatten()

dset = fshapes.create_dataset(name='fakesLowMt_sumw2', shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
dset[...] = np.zeros_like(hfakesLowMt.flatten())

threshold = np.digitize(30.,mTBins)
# fR is computed in low-mt region
# fR = np.sum(hdata[:,:,-1,:threshold-1,0]-hewk[:,:,-1,:threshold-1,0], axis=2)/np.sum(hdata[:,:,-1,:threshold-1,1]-hewk[:,:,-1,:threshold-1,1],axis=2)
fR =(hdata[:,:,-1,0,0]-hewk[:,:,-1,0,0])/(hdata[:,:,-1,0,1]-hewk[:,:,-1,0,1])

hfakesHighMt = np.where(hdata[:,:,-1,:,:]-hewk[:,:,-1,:,:]>0, hdata[:,:,-1,:,:]-hewk[:,:,-1,:,:], 1)
hfakesHighMt[:,:,0,:] = np.zeros([len(etaBins)-1,len(ptBins)-1,len(isoBins)-1], dtype='float64')
# keep aiso/iso ratio constant
hfakesHighMt[:,:,1,0] = (hdata[:,:,-1,1,1]-hewk[:,:,-1,1,1]) * fR
dset = fshapes.create_dataset(name='fakesHighMt', shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
dset[...] = hfakesHighMt.flatten()

dset = fshapes.create_dataset(name='fakesHighMt_sumw2', shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
dset[...] = np.zeros_like(hfakesHighMt.flatten())

# build mask
print("building shapes")
for i in range(hfakesLowMt.shape[0]*hfakesLowMt.shape[1]):
    mask = np.zeros(hfakesLowMt.shape[0]*hfakesLowMt.shape[1])
    mask[i,...]=1
    mask = mask.reshape((hfakesLowMt.shape[0],hfakesLowMt.shape[1]))[...,np.newaxis,np.newaxis]
    # nuisance for changing the normalisations independently

    hfakesLowMtVarUp = np.where(mask==0, hfakesLowMt, hfakesLowMt+0.5*hfakesLowMt)
    dset = fshapes.create_dataset(name='fakesLowMt_fakeNormLowMtBin{}Up'.format(i), shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
    dset[...] = hfakesLowMtVarUp.flatten()
    hfakesLowMtVarDown = np.where(mask==0, hfakesLowMt, hfakesLowMt-0.5*hfakesLowMt)
    dset = fshapes.create_dataset(name='fakesLowMt_fakeNormLowMtBin{}Down'.format(i), shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
    dset[...] = hfakesLowMtVarDown.flatten()

    hfakesHighMtVarUp = np.where(mask==0, hfakesHighMt, hfakesHighMt+0.5*hfakesHighMt)
    dset = fshapes.create_dataset(name='fakesHighMt_fakeNormHighMtBin{}Up'.format(i), shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
    dset[...] = hfakesHighMtVarUp.flatten()
    hfakesHighMtVarDown = np.where(mask==0, hfakesHighMt, hfakesHighMt-0.5*hfakesHighMt)
    dset = fshapes.create_dataset(name='fakesHighMt_fakeNormHighMtBin{}Down'.format(i), shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
    dset[...] = hfakesHighMtVarDown.flatten()

    # print('checking if any zero or negative yields for bin {}'.format(i))
    # print(np.any((hfakesLowMtVarUp+hfakesHighMtVarUp)<=0.))
    # print(np.any((hfakesLowMtVarDown+hfakesHighMtVarDown)<=0.))

    # common nuisance for changing fake shape
    
    norm = np.sum(hfakesLowMt[:,:,0,:],axis=2)
    ratio = hfakesLowMt[:,:,0,0]/norm #ratio iso/iso+aiso
    rate_var = 2.
    var_idx = np.nonzero(mask)
    # set to nominal
    hfakesLowMtVarUp = np.empty_like(hfakesLowMt)
    hfakesLowMtVarDown = np.empty_like(hfakesLowMt)
    np.copyto(hfakesLowMtVarUp, hfakesLowMt) # (dst, src)
    np.copyto(hfakesLowMtVarDown, hfakesLowMt) # (dst, src)
    # apply variation to isolated part
    hfakesLowMtVarUp[var_idx[0],var_idx[1],0, 0] = (rate_var*ratio*norm)[var_idx[0],var_idx[1]]
    hfakesLowMtVarDown[var_idx[0],var_idx[1],0, 0] = ((1./rate_var)*ratio*norm)[var_idx[0],var_idx[1]]
    # apply variation to anti-isolated part
    hfakesLowMtVarUp[var_idx[0],var_idx[1],0, 1] = ((1-rate_var*ratio)*norm)[var_idx[0],var_idx[1]]
    hfakesLowMtVarDown[var_idx[0],var_idx[1],0, 1] = ((1-(1./rate_var)*ratio)*norm)[var_idx[0],var_idx[1]]
    
    dset = fshapes.create_dataset(name='fakesLowMt_fakeShapeBin{}Up'.format(i), shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
    dset[...] = hfakesLowMtVarUp.flatten()
    dset = fshapes.create_dataset(name='fakesLowMt_fakeShapeBin{}Down'.format(i), shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
    dset[...] = hfakesLowMtVarDown.flatten()

    norm = np.sum(hfakesHighMt[:,:,1,:],axis=2)
    ratio = hfakesHighMt[:,:,1,0]/norm #ratio iso/iso+aiso
    rate_var = 1.2
    var_idx = np.nonzero(mask)
    # set to nominal
    hfakesHighMtVarUp = np.empty_like(hfakesHighMt)
    hfakesHighMtVarDown = np.empty_like(hfakesHighMt)
    np.copyto(hfakesHighMtVarUp, hfakesHighMt) # (dst, src)
    np.copyto(hfakesHighMtVarDown, hfakesHighMt) # (dst, src)
    # apply variation to isolated part
    hfakesHighMtVarUp[var_idx[0],var_idx[1],1, 0] = (rate_var*ratio*norm)[var_idx[0],var_idx[1]]
    hfakesHighMtVarDown[var_idx[0],var_idx[1],1, 0] = ((1./rate_var)*ratio*norm)[var_idx[0],var_idx[1]]
    # apply variation to anti-isolated part
    hfakesHighMtVarUp[var_idx[0],var_idx[1],1, 1] = ((1-rate_var*ratio)*norm)[var_idx[0],var_idx[1]]
    hfakesHighMtVarDown[var_idx[0],var_idx[1],1, 1] = ((1-(1./rate_var)*ratio)*norm)[var_idx[0],var_idx[1]]
    
    dset = fshapes.create_dataset(name='fakesHighMt_fakeShapeBin{}Up'.format(i), shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
    dset[...] = hfakesHighMtVarUp.flatten()
    dset = fshapes.create_dataset(name='fakesHighMt_fakeShapeBin{}Down'.format(i), shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
    dset[...] = hfakesHighMtVarDown.flatten()

    # print('checking if any zero or negative yields for bin {}'.format(i))
    # print(np.any((hfakesLowMtVarUp+hfakesHighMtVarUp)<=0.))
    # print(np.any((hfakesLowMtVarDown+hfakesHighMtVarDown)<=0.))

# plot pt, eta and mt in isolated and antiisolated region
for i in range(2):
    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    ax1.set_title("eta_iso{}_highMt".format(i), fontsize=18)
    ax1.set_ylabel('number of events')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('muon $\eta$')
    etadata = np.sum(hdata,axis=1)[:,-1,-1,i]
    etaewk = np.sum(hewk,axis=1)[:,-1,-1,i]
    etaWmu = np.sum(hWmu,axis=1)[:,-1,-1,i]
    etaWtau = np.sum(hWtau,axis=1)[:,-1,-1,i]
    etaDY = np.sum(hDY,axis=1)[:,-1,-1,i]
    etaTop = np.sum(hTop,axis=1)[:,-1,-1,i]
    etaDiboson = np.sum(hDiboson,axis=1)[:,-1,-1,i]
    etafake = np.sum(hfakesHighMt,axis=1)[:,-1,i]
    etalowacc = np.sum(hlowacc,axis=1)[:,-1,-1,i]
    hep.histplot([etadata],bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
    hep.histplot([etaDiboson,etaTop,etaDY,etaWtau,etafake,etalowacc,etaWmu],bins = etaBins, histtype = 'fill',linestyle = 'solid', color =["grey","magenta","orange","green","blue","aqua","red"], label=["Diboson","Top","DY",r'$W->\tau\nu$',"fakes","low acc",r'$W->\mu\nu$'], stack = True, ax=ax1)
    ax2.set_ylim([0.9, 1.1])
    hep.histplot([etadata/(etafake+etaewk)], bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    plt.savefig('testprefit/eta_iso{}_highMt.png'.format(i))
    plt.cla()

    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    ax1.set_title("pt_iso{}_highMt".format(i), fontsize=18)
    ax1.set_ylabel('number of events')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('muon $p_T$')
    ptdata = np.sum(hdata,axis=0)[:,-1,-1,i]
    ptewk = np.sum(hewk,axis=0)[:,-1,-1,i]
    ptWmu = np.sum(hWmu,axis=0)[:,-1,-1,i]
    ptWtau = np.sum(hWtau,axis=0)[:,-1,-1,i]
    ptDY = np.sum(hDY,axis=0)[:,-1,-1,i]
    ptTop = np.sum(hTop,axis=0)[:,-1,-1,i]
    ptDiboson = np.sum(hDiboson,axis=0)[:,-1,-1,i]
    ptfake = np.sum(hfakesHighMt,axis=0)[:,-1,i]
    ptlowacc = np.sum(hlowacc,axis=0)[:,-1,-1,i]
    hep.histplot([ptdata],bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1,label = ["data"])
    hep.histplot([ptDiboson,ptTop,ptDY,ptWtau,ptfake,ptlowacc,ptWmu],bins = ptBins, histtype = 'fill',linestyle = 'solid', color =["grey","magenta","orange","green","blue","aqua","red"], label=["Diboson","Top","DY",r'$W->\tau\nu$',"fakes","low acc",r'$W->\mu\nu$'], stack = True, ax=ax1)
    ax2.set_ylim([0.9, 1.1])
    hep.histplot([ptdata/(ptfake+ptewk)],bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    plt.savefig('testprefit/pt_iso{}_highMt.png'.format(i))
    plt.cla()

    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    ax1.set_title("eta_iso{}_lowMt".format(i), fontsize=18)
    ax1.set_ylabel('number of events')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('muon $\eta$')
    etadata = np.sum(hdata,axis=1)[:,-1,0,i]
    etaewk = np.sum(hewk,axis=1)[:,-1,0,i]
    etaWmu = np.sum(hWmu,axis=1)[:,-1,0,i]
    etaWtau = np.sum(hWtau,axis=1)[:,-1,0,i]
    etaDY = np.sum(hDY,axis=1)[:,-1,0,i]
    etaTop = np.sum(hTop,axis=1)[:,-1,0,i]
    etaDiboson = np.sum(hDiboson,axis=1)[:,-1,0,i]
    etafake = np.sum(hfakesLowMt,axis=1)[:,0,i]
    etalowacc = np.sum(hlowacc,axis=1)[:,-1,0,i]
    hep.histplot([etadata],bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1,label = ["data"])
    hep.histplot([etaDiboson,etaTop,etaDY,etaWtau,etafake,etalowacc,etaWmu],bins = etaBins, histtype = 'fill',linestyle = 'solid', color =["grey","magenta","orange","green","blue","aqua","red"], label=["Diboson","Top","DY",r'$W->\tau\nu$',"fakes","low acc",r'$W->\mu\nu$'], stack = True, ax=ax1)
    ax2.set_ylim([0.9, 1.1])
    hep.histplot([etadata/(etafake+etaewk)],bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    plt.savefig('testprefit/eta_iso{}_lowMt.png'.format(i))
    plt.cla()

    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    ax1.set_title("pt_iso{}_lowMt".format(i), fontsize=18)
    ax1.set_ylabel('number of events')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('muon $p_T$')
    ptdata = np.sum(hdata,axis=0)[:,-1,0,i]
    ptewk = np.sum(hewk,axis=0)[:,-1,0,i]
    ptWmu = np.sum(hWmu,axis=0)[:,-1,0,i]
    ptWtau = np.sum(hWtau,axis=0)[:,-1,0,i]
    ptDY = np.sum(hDY,axis=0)[:,-1,0,i]
    ptTop = np.sum(hTop,axis=0)[:,-1,0,i]
    ptDiboson = np.sum(hDiboson,axis=0)[:,-1,0,i]
    ptfake = np.sum(hfakesLowMt,axis=0)[:,0,i]
    ptlowacc = np.sum(hlowacc,axis=0)[:,-1,0,i]
    hep.histplot([ptdata],bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1,label = ["data"])
    hep.histplot([ptDiboson,ptTop,ptDY,ptWtau,ptfake,ptlowacc,ptWmu],bins = ptBins, histtype = 'fill',linestyle = 'solid', color =["grey","magenta","orange","green","blue","aqua","red"], label=["Diboson","Top","DY",r'$W->\tau\nu$',"fakes","low acc",r'$W->\mu\nu$'], stack = True, ax=ax1)
    ax2.set_ylim([0.9, 1.1])
    hep.histplot([ptdata/(ptfake+ptewk)],bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    plt.savefig('testprefit/pt_iso{}_lowMt.png'.format(i))
    plt.cla()

# fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
# ax1.set_title("mt", fontsize=18)
# ax1.set_ylabel('number of events')
# ax2.set_ylabel('data/prediction')
# ax2.set_xlabel('$m_T$')
# mtdata = np.sum(hdata[:,:,-1,:,0],axis=(0,1))
# mtewk = np.sum(hewk[:,:,-1,:,0],axis=(0,1))
# mtW = np.sum(hW[:,:,-1,:,0],axis=(0,1))
# mtDY = np.sum(hDY[:,:,-1,:,0],axis=(0,1))
# mtTop = np.sum(hTop[:,:,-1,:,0],axis=(0,1))
# mtDiboson = np.sum(hDiboson[:,:,-1,:,0],axis=(0,1))
# mtfake = np.einsum('kmi,km->i',hdata[:,:,-1,:,1]-hewk[:,:,-1,:,1],fR)

# hep.histplot([mtdata],bins = mTBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1,label = ["data"])
# hep.histplot([mtDiboson,mtTop,mtDY,mtfake,mtW],bins = mTBins, histtype = 'fill',linestyle = 'solid', color =["grey","magenta","orange","green","blue","aqua","red"], label=["Diboson","Top","DY",r'$W->\tau\nu$',"fakes","low acc",r'$W->\mu\nu$'], stack = True, ax=ax1)
# ax2.set_ylim([0.9, 1.1])
# hep.histplot([mtdata/(mtfake+mtewk)],bins = mTBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
# ax1.legend(loc='upper right', frameon=True)
# plt.tight_layout()
# plt.savefig('testprefit/mt.png')
# plt.cla()