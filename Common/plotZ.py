import os
import sys
sys.path.append('data/')
import h5py
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from binning import ptBins, etaBins, isoBins, zmassBins, qtBins
plt.style.use([hep.style.ROOT])
#hep.cms.label(loc=0, year=2016, lumi=35.9, data=True)
#hep.cms.text('Simulation')

folder = "../templateMaker/outputDY_31_01_2021_17_59_44/"

histonames = ['DY', 'DY_sumw2']
shape = ((len(zmassBins)-1)*(len(etaBins)-1)*(len(ptBins)-1)*(len(qtBins)-1)*(len(etaBins)-1))
DYFiles = ["DYJetsToMuMu_M50.hdf5","DYJetsToTauTau_M50.hdf5"]
TopFiles = ["ST_t-channel_muDecays.hdf5", "ST_t-channel_tauDecays.hdf5","ST_s-channel_4f_leptonDecays.hdf5","ST_t-channel_top_5f_InclusiveDecays.hdf5","TTToSemiLeptonic.hdf5", "TTTo2L2Nu.hdf5"]
DibosonFiles = ["WW.hdf5","WZ.hdf5"]

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

haddFiles(DYFiles,"DY",histonames, shape)
# haddFiles(TopFiles,"Top",histonames, shape)
# haddFiles(DibosonFiles,"Diboson",histonames, shape)

fdata = h5py.File(folder+'data.hdf5', mode='r+')
fDY = h5py.File(folder+'DY.hdf5', mode='r+')
# fTop = h5py.File(folder+'Top.hdf5', mode='r+')
# fDiboson = h5py.File(folder+'Diboson.hdf5', mode='r+')

hdata = np.array(fdata['data_obs'][:].reshape((len(zmassBins)-1,len(etaBins)-1,len(ptBins)-1,len(qtBins)-1,len(etaBins)-1),order='F'),order='C')
hDY = np.array(fDY['DY'][:].reshape((len(zmassBins)-1,len(etaBins)-1,len(ptBins)-1,len(qtBins)-1,len(etaBins)-1),order='F'),order='C')
# hTop = np.array(fTop['DY'][:].reshape((len(zmassBins)-1,len(etaBins)-1,len(ptBins)-1,len(qtBins)-1,len(etaBins)-1),order='F'),order='C')
# hDiboson = np.array(fDiboson['DY'][:].reshape((len(zmassBins)-1,len(etaBins)-1,len(ptBins)-1,len(qtBins)-1,len(etaBins)-1),order='F'),order='C')
hTop = np.zeros(hdata.shape)
hDiboson = np.zeros(hdata.shape)

hewk = hDY+hTop+hDiboson
#### mass
fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
ax1.set_title("mass_iso1_1_iso2_1", fontsize=18)
ax1.set_ylabel('number of events')
ax2.set_ylabel('data/prediction')
ax2.set_xlabel('dimuon mass')
massdata = np.sum(hdata,axis=(1,2,3,4))[:]
massDY = np.sum(hDY,axis=(1,2,3,4))[:]
massTop = np.sum(hTop,axis=(1,2,3,4))[:]
massDiboson = np.sum(hDiboson,axis=(1,2,3,4))[:]
massewk = np.sum(hewk,axis=(1,2,3,4))[:]
hep.histplot([massdata],bins = zmassBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
hep.histplot([massDiboson,massTop,massDY],bins = zmassBins, histtype = 'fill',linestyle = 'solid', color =["magenta","green","orange"], label=["Diboson","Top","DY"], stack = True, ax=ax1)
ax2.set_ylim([0.7, 1.3])
hep.histplot([massdata/massewk], bins = zmassBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
ax1.legend(loc='upper right', frameon=True)
plt.savefig('mass_iso1_1_iso2_1.png')
plt.cla()

#### eta 
fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
ax1.set_title("eta_iso1_1_iso2_1", fontsize=18)
ax1.set_ylabel('number of events')
ax2.set_ylabel('data/prediction')
ax2.set_xlabel('muon $\eta$')
etadata = np.sum(hdata,axis=(0,2,3,4))[:]
etaDY = np.sum(hDY,axis=(0,2,3,4))[:]
etaTop = np.sum(hTop,axis=(0,2,3,4))[:]
etaDiboson = np.sum(hDiboson,axis=(0,2,3,4))[:]
etaewk = np.sum(hewk,axis=(0,2,3,4))[:]
hep.histplot([etadata],bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
hep.histplot([etaDiboson,etaTop,etaDY],bins = etaBins, histtype = 'fill',linestyle = 'solid', color =["magenta","green","orange"], label=["Diboson","Top","DY"], stack = True, ax=ax1)
ax2.set_ylim([0.7, 1.3])
hep.histplot([etadata/etaewk], bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
ax1.legend(loc='upper right', frameon=True)
plt.savefig('eta_iso1_1_iso2_1.png')
plt.cla()

#### pt 
fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
ax1.set_title("pt_iso1_1_iso2_1", fontsize=18)
ax1.set_ylabel('number of events')
ax2.set_ylabel('data/prediction')
ax2.set_xlabel('muon $p_T$')
ptdata = np.sum(hdata,axis=(0,1,3,4))[:]
ptDY = np.sum(hDY,axis=(0,1,3,4))[:]
ptTop = np.sum(hTop,axis=(0,1,3,4))[:]
ptDiboson = np.sum(hDiboson,axis=(0,1,3,4))[:]
ptewk = np.sum(hewk,axis=(0,1,3,4))[:]
hep.histplot([ptdata],bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
hep.histplot([ptDiboson,ptTop,ptDY],bins = ptBins, histtype = 'fill',linestyle = 'solid', color =["magenta","green","orange"], label=["Diboson","Top","DY"], stack = True, ax=ax1)
ax2.set_ylim([0.7, 1.3])
hep.histplot([ptdata/ptDY], bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
ax1.legend(loc='upper right', frameon=True)
plt.savefig('pt_iso1_1_iso2_1.png')
plt.cla()

#### z pt 
fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
ax1.set_title("qt_iso1_1_iso2_1", fontsize=18)
ax1.set_ylabel('number of events')
ax2.set_ylabel('data/prediction')
ax2.set_xlabel('dimuon $p_T$')
qtdata = np.sum(hdata,axis=(0,1,2,4))[:]
qtDY = np.sum(hDY,axis=(0,1,2,4))[:]
qtTop = np.sum(hTop,axis=(0,1,2,4))[:]
qtDiboson = np.sum(hDiboson,axis=(0,1,2,4))[:]
qtewk = np.sum(hewk,axis=(0,1,2,4))[:]
hep.histplot([qtdata],bins = qtBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
hep.histplot([qtDiboson,qtTop,qtDY],bins = qtBins, histtype = 'fill',linestyle = 'solid', color =["magenta","green","orange"], label=["Diboson","Top","DY"], stack = True, ax=ax1)
ax2.set_ylim([0.7, 1.3])
hep.histplot([qtdata/qtDY], bins = qtBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
ax1.legend(loc='upper right', frameon=True)
plt.savefig('qt_iso1_1_iso2_1.png')
plt.cla()

#### z y 
fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
ax1.set_title("y_iso1_1_iso2_1", fontsize=18)
ax1.set_ylabel('number of events')
ax2.set_ylabel('data/prediction')
ax2.set_xlabel('dimuon rapidity')
ydata = np.sum(hdata,axis=(0,1,2,3))[:]
yDY = np.sum(hDY,axis=(0,1,2,3))[:]
yTop = np.sum(hTop,axis=(0,1,2,3))[:]
yDiboson = np.sum(hDiboson,axis=(0,1,2,3))[:]
yewk = np.sum(hewk,axis=(0,1,2,3))[:]
hep.histplot([ydata],bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
hep.histplot([yDiboson,yTop,yDY],bins = etaBins, histtype = 'fill',linestyle = 'solid', color =["magenta","green","orange"], label=["Diboson","Top","DY"], stack = True, ax=ax1)
ax2.set_ylim([0.7, 1.3])
hep.histplot([ydata/yDY], bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
ax1.legend(loc='upper right', frameon=True)
plt.savefig('y_iso1_1_iso2_1.png')
plt.cla()
