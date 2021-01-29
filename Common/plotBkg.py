import os
import sys
sys.path.append('data/')
import h5py
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from binning import ptBins, etaBins, mTBins, isoBins, chargeBins
plt.style.use([hep.style.ROOT])
#hep.cms.label(loc=0, year=2016, lumi=35.9, data=True)
#hep.cms.text('Simulation')

folder = "../templateMaker/output_28_01_2021_18_20_54/"

# ewkFiles = ["DYJetsToLL_M10to50.hdf5", "ST_t-channel_antitop_4f_inclusiveDecays.hdf5","ST_tW_top_5f_inclusiveDecays.hdf5","TTJets_SingleLeptFromTbar.hdf5","WZ.hdf5",\
# "DYJetsToLL_M50.hdf5","ST_t-channel_top_4f_inclusiveDecays_13TeV.hdf5","TTJets_DiLept.hdf5","WJetsToLNu.hdf5","ZZ.hdf5",\
# "ST_s-channel_4f_leptonDecays.hdf5","ST_tW_antitop_5f_inclusiveDecays.hdf5","TTJets_SingleLeptFromT.hdf5","WW.hdf5"]

WFiles = ["WMinusJetsToMuNu.hdf5","WPlusJetsToTauNu.hdf5","WMinusJetsToTauNu.hdf5","WPlusJetsToMuNu.hdf5"]
DYFiles = ["DYJetsToMuMu_M50.hdf5","DYJetsToTauTau_M50.hdf5"]
TopFiles = ["ST_t-channel_muDecays.hdf5", "ST_t-channel_tauDecays.hdf5","ST_s-channel_4f_leptonDecays.hdf5","ST_t-channel_top_5f_InclusiveDecays.hdf5"]
DibosonFiles = ["WW.hdf5","WZ.hdf5"]

histonames = ['ewk', 'ewk_sumw2']

def haddFiles(fileList, fname, histonames, shape):

    f = h5py.File(folder+fname+'.hdf5', mode='w')
    for name in histonames:
        dset = f.create_dataset(name=name, shape=[shape], dtype='float64')
        tmp = np.zeros([shape],dtype='float64')
        for file in fileList:
            ftmp = h5py.File(folder+file, mode='r+')
            tmp += ftmp[name][:]
        dset[...] = tmp
    return

shape = (len(etaBins)-1) * (len(ptBins)-1) * (len(chargeBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)

haddFiles(WFiles,"W",histonames, shape)
haddFiles(DYFiles,"DY",histonames, shape)
haddFiles(TopFiles,"Top",histonames, shape)
haddFiles(DibosonFiles,"Diboson",histonames, shape)

fdata = h5py.File(folder+'data.hdf5', mode='r+')
fW = h5py.File(folder+'W.hdf5', mode='r+')
fDY = h5py.File(folder+'DY.hdf5', mode='r+')
fTop = h5py.File(folder+'Top.hdf5', mode='r+')
fDiboson = h5py.File(folder+'Diboson.hdf5', mode='r+')


hdata = np.array(fdata['data_obs'][:].reshape((len(etaBins)-1,len(ptBins)-1,len(chargeBins)-1,len(mTBins)-1,len(isoBins)-1),order='F'),order='C')
hdatasumw2 = np.array(fdata['data_obs_sumw2'][:].reshape((len(etaBins)-1,len(ptBins)-1,len(chargeBins)-1,len(mTBins)-1,len(isoBins)-1),order='F'),order='C')
hW = np.array(fW['ewk'][:].reshape((len(etaBins)-1,len(ptBins)-1,len(chargeBins)-1,len(mTBins)-1,len(isoBins)-1),order='F'),order='C')
hDY = np.array(fDY['ewk'][:].reshape((len(etaBins)-1,len(ptBins)-1,len(chargeBins)-1,len(mTBins)-1,len(isoBins)-1),order='F'),order='C')
hTop = np.array(fTop['ewk'][:].reshape((len(etaBins)-1,len(ptBins)-1,len(chargeBins)-1,len(mTBins)-1,len(isoBins)-1),order='F'),order='C')
hDiboson = np.array(fDiboson['ewk'][:].reshape((len(etaBins)-1,len(ptBins)-1,len(chargeBins)-1,len(mTBins)-1,len(isoBins)-1),order='F'),order='C')

hewk = hW+hDY+hTop+hDiboson

fbkg = h5py.File('bkgWplus.hdf5', mode='w')

dset = fbkg.create_dataset(name='data_obs', shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
dset[...] = hdata[:,:,-1,:,:].flatten() #select positive charge

dset = fbkg.create_dataset(name='ewk', shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
dset[...] = hewk[:,:,-1,:,:].flatten() #select positive charge

# dset = fbkg.create_dataset(name='ewk_sumw2', shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
# dset[...] = hewksumw2[:,:,-1,:,:].flatten() #select positive charge

hfakesLowMt = hdata[:,:,-1,:,:]-hewk[:,:,-1,:,:]
hfakesLowMt[:,:,1,:] = np.zeros([len(etaBins)-1,len(ptBins)-1,len(isoBins)-1], dtype='float64')
dset = fbkg.create_dataset(name='fakesLowMt', shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
dset[...] = hfakesLowMt.flatten()

# hfakesLowMtsumw2 = (hdatasumw2[:,:,-1,:,:]+hewksumw2[:,:,-1,:,:])
# hfakesLowMtsumw2[:,:,1,:] = np.zeros([len(etaBins)-1,len(ptBins)-1,len(isoBins)-1], dtype='float64')
# dset = fbkg.create_dataset(name='fakesLowMt_sumw2', shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
# dset[...] = hfakesLowMtsumw2.flatten()

hfakesHighMt = np.where(hdata[:,:,-1,:,:]-hewk[:,:,-1,:,:]>0, hdata[:,:,-1,:,:]-hewk[:,:,-1,:,:], 1)
hfakesHighMt[:,:,0,:] = np.zeros([len(etaBins)-1,len(ptBins)-1,len(isoBins)-1], dtype='float64')
# keep aiso/iso ratio constant
hfakesHighMt[:,:,1,0] = (hdata[:,:,-1,1,1]-hewk[:,:,-1,1,1]) * (hdata[:,:,-1,0,0]-hewk[:,:,-1,0,0])/(hdata[:,:,-1,0,1]-hewk[:,:,-1,0,1])
dset = fbkg.create_dataset(name='fakesHighMt', shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
dset[...] = hfakesHighMt.flatten()

# hfakesHighMtsumw2 = hdatasumw2[:,:,-1,:,:]+hewksumw2[:,:,-1,:,:]
# hfakesHighMtsumw2[:,:,0,:] = np.zeros([len(etaBins)-1,len(ptBins)-1,len(isoBins)-1], dtype='float64')
# dset = fbkg.create_dataset(name='fakesHighMt_sumw2', shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
# dset[...] = hfakesHighMtsumw2.flatten()

# # build mask
# print("building shapes")
# for i in range(hfakesLowMt.shape[0]*hfakesLowMt.shape[1]):
#     mask = np.zeros(hfakesLowMt.shape)
#     mask = mask.reshape((hfakesLowMt.shape[0]*hfakesLowMt.shape[1], hfakesLowMt.shape[2], hfakesLowMt.shape[3]))
#     mask[i,...]=1
#     mask = mask.reshape(hfakesLowMt.shape)

#     # nuisance for changing the normalisations independently

#     hfakesLowMtVarUp = np.where(mask==0, hfakesLowMt, hfakesLowMt+0.5*hfakesLowMt)
#     dset = fbkg.create_dataset(name='fakesLowMt_fakeNormLowMtBin{}Up'.format(i), shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
#     dset[...] = hfakesLowMtVarUp.flatten()
#     hfakesLowMtVarDown = np.where(mask==0, hfakesLowMt, hfakesLowMt-0.5*hfakesLowMt)
#     dset = fbkg.create_dataset(name='fakesLowMt_fakeNormLowMtBin{}Down'.format(i), shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
#     dset[...] = hfakesLowMtVarDown.flatten()

#     hfakesHighMtVarUp = np.where(mask==0, hfakesHighMt, hfakesHighMt+0.5*hfakesHighMt)
#     dset = fbkg.create_dataset(name='fakesHighMt_fakeNormHighMtBin{}Up'.format(i), shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
#     dset[...] = hfakesHighMtVarUp.flatten()
#     hfakesHighMtVarDown = np.where(mask==0, hfakesHighMt, hfakesHighMt-0.5*hfakesHighMt)
#     dset = fbkg.create_dataset(name='fakesHighMt_fakeNormHighMtBin{}Down'.format(i), shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
#     dset[...] = hfakesHighMtVarDown.flatten()

#     # common nuisance for changing fake shape
    
#     norm = np.sum(hfakesLowMt[:,:,0,:],axis=2)
#     ratio = hfakesLowMt[:,:,0,0]/norm #ratio iso/iso+aiso
#     rate_var = 2.
#     var_idx = np.nonzero(mask)
#     # set to nominal
#     hfakesLowMtVarUp = hfakesLowMt
#     hfakesLowMtVarDown = hfakesLowMt
#     # apply variation to isolated part
#     hfakesLowMtVarUp[var_idx[0],var_idx[1],0, 0] = (rate_var*ratio*norm)[var_idx[0],var_idx[1]]
#     hfakesLowMtVarDown[var_idx[0],var_idx[1],0, 0] = ((1./rate_var)*ratio*norm)[var_idx[0],var_idx[1]]
#     # apply variation to anti-isolated part
#     hfakesLowMtVarUp[var_idx[0],var_idx[1],0, 1] = ((1-rate_var*ratio)*norm)[var_idx[0],var_idx[1]]
#     hfakesLowMtVarDown[var_idx[0],var_idx[1],0, 1] = ((1-(1./rate_var)*ratio)*norm)[var_idx[0],var_idx[1]]
    
#     dset = fbkg.create_dataset(name='fakesLowMt_fakeShapeBin{}Up'.format(i), shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
#     dset[...] = hfakesLowMtVarUp.flatten()
#     dset = fbkg.create_dataset(name='fakesLowMt_fakeShapeBin{}Down'.format(i), shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
#     dset[...] = hfakesLowMtVarDown.flatten()

#     norm = np.sum(hfakesHighMt[:,:,1,:],axis=2)
#     ratio = hfakesHighMt[:,:,1,0]/norm #ratio iso/iso+aiso
#     rate_var = 1.2
#     var_idx = np.nonzero(mask)
#     # set to nominal
#     hfakesHighMtVarUp = hfakesHighMt
#     hfakesHighMtVarDown = hfakesHighMt
#     # apply variation to isolated part
#     hfakesHighMtVarUp[var_idx[0],var_idx[1],1, 0] = (rate_var*ratio*norm)[var_idx[0],var_idx[1]]
#     hfakesHighMtVarDown[var_idx[0],var_idx[1],1, 0] = ((1./rate_var)*ratio*norm)[var_idx[0],var_idx[1]]
#     # apply variation to anti-isolated part
#     hfakesHighMtVarUp[var_idx[0],var_idx[1],1, 1] = ((1-rate_var*ratio)*norm)[var_idx[0],var_idx[1]]
#     hfakesHighMtVarDown[var_idx[0],var_idx[1],1, 1] = ((1-(1./rate_var)*ratio)*norm)[var_idx[0],var_idx[1]]
    
#     dset = fbkg.create_dataset(name='fakesHighMt_fakeShapeBin{}Up'.format(i), shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
#     dset[...] = hfakesHighMtVarUp.flatten()
#     dset = fbkg.create_dataset(name='fakesHighMt_fakeShapeBin{}Down'.format(i), shape=[(len(etaBins)-1) * (len(ptBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)], dtype='float64')
#     dset[...] = hfakesHighMtVarDown.flatten()

# plot pt, eta and mt in isolated and antiisolated region

for i in range(2):
    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    ax1.set_title("eta_iso{}_highMt".format(i), fontsize=18)
    ax1.set_ylabel('number of events')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('muon $\eta$')
    etadata = np.sum(hdata,axis=1)[:,-1,-1,i]
    etaewk = np.sum(hewk,axis=1)[:,-1,-1,i]
    etaW = np.sum(hW,axis=1)[:,-1,-1,i]
    etaDY = np.sum(hDY,axis=1)[:,-1,-1,i]
    etaTop = np.sum(hTop,axis=1)[:,-1,-1,i]
    etaDiboson = np.sum(hDiboson,axis=1)[:,-1,-1,i]
    etafake = np.sum(hfakesHighMt,axis=1)[:,-1,i]
    hep.histplot([etadata],bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
    hep.histplot([etafake,etaDiboson,etaTop,etaDY,etaW],bins = etaBins, histtype = 'fill',linestyle = 'solid', color =["grey","magenta","orange","blue","red"], label=["fake","Diboson","Top","DY","W"], stack = True, ax=ax1)
    ax2.set_ylim([0.7, 1.3])
    hep.histplot([etadata/(etafake+etaewk)], bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.savefig('eta_iso{}_highMt.png'.format(i))
    plt.cla()

    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    ax1.set_title("pt_iso{}_highMt".format(i), fontsize=18)
    ax1.set_ylabel('number of events')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('muon $p_T$')
    ptdata = np.sum(hdata,axis=0)[:,-1,-1,i]
    ptewk = np.sum(hewk,axis=0)[:,-1,-1,i]
    ptW = np.sum(hW,axis=0)[:,-1,-1,i]
    ptDY = np.sum(hDY,axis=0)[:,-1,-1,i]
    ptTop = np.sum(hTop,axis=0)[:,-1,-1,i]
    ptDiboson = np.sum(hDiboson,axis=0)[:,-1,-1,i]
    ptfake = np.sum(hfakesHighMt,axis=0)[:,-1,i]
    hep.histplot([ptdata],bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1,label = ["data"])
    hep.histplot([ptfake,ptDiboson,ptTop,ptDY,ptW],bins = ptBins, histtype = 'fill',linestyle = 'solid', color =["grey","magenta","orange","blue","red"], label=["fake","Diboson","Top","DY","W"], stack = True, ax=ax1)
    ax2.set_ylim([0.7, 1.3])
    hep.histplot([ptdata/(ptfake+ptewk)],bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.savefig('pt_iso{}_highMt.png'.format(i))
    plt.cla()

    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    ax1.set_title("eta_iso{}_lowMt".format(i), fontsize=18)
    ax1.set_ylabel('number of events')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('muon $\eta$')
    etadata = np.sum(hdata,axis=1)[:,-1,0,i]
    etaewk = np.sum(hewk,axis=1)[:,-1,0,i]
    etaW = np.sum(hW,axis=1)[:,-1,0,i]
    etaDY = np.sum(hDY,axis=1)[:,-1,0,i]
    etaTop = np.sum(hTop,axis=1)[:,-1,0,i]
    etaDiboson = np.sum(hDiboson,axis=1)[:,-1,0,i]
    etafake = np.sum(hfakesLowMt,axis=1)[:,0,i]
    hep.histplot([etadata],bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1,label = ["data"])
    hep.histplot([etafake,etaDiboson,etaTop,etaDY,etaW],bins = etaBins, histtype = 'fill',linestyle = 'solid', color =["grey","magenta","orange","blue","red"], label=["fake","Diboson","Top","DY","W"], stack = True, ax=ax1)
    ax2.set_ylim([0.7, 1.3])
    hep.histplot([etadata/(etafake+etaewk)],bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.savefig('eta_iso{}_lowMt.png'.format(i))
    plt.cla()

    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    ax1.set_title("pt_iso{}_lowMt".format(i), fontsize=18)
    ax1.set_ylabel('number of events')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('muon $p_T$')
    ptdata = np.sum(hdata,axis=0)[:,-1,0,i]
    ptewk = np.sum(hewk,axis=0)[:,-1,0,i]
    ptW = np.sum(hW,axis=0)[:,-1,0,i]
    ptDY = np.sum(hDY,axis=0)[:,-1,0,i]
    ptTop = np.sum(hTop,axis=0)[:,-1,0,i]
    ptDiboson = np.sum(hDiboson,axis=0)[:,-1,0,i]
    ptfake = np.sum(hfakesLowMt,axis=0)[:,0,i]
    hep.histplot([ptdata],bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1,label = ["data"])
    hep.histplot([ptfake,ptDiboson,ptTop,ptDY,ptW],bins = ptBins, histtype = 'fill',linestyle = 'solid', color =["grey","magenta","orange","blue","red"], label=["fake","Diboson","Top","DY","W"], stack = True, ax=ax1)
    ax2.set_ylim([0.7, 1.3])
    hep.histplot([ptdata/(ptfake+ptewk)],bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.savefig('pt_iso{}_lowMt.png'.format(i))
    plt.cla()