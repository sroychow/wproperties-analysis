import os
import sys
sys.path.append('data/')
import h5py
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from binning import ptBins, etaBins, isoBins, zmassBins
plt.style.use([hep.style.ROOT])
#hep.cms.label(loc=0, year=2016, lumi=35.9, data=True)
#hep.cms.text('Simulation')

folder = "../templateMaker/outputDY_27_01_2021_23_31_36/"

fdata = h5py.File(folder+'data.hdf5', mode='r')
fDY = h5py.File(folder+'DYJetsToLL_M50.hdf5', mode='r')

hdata = np.array(fdata['data_obs'][:].reshape((len(zmassBins)-1,len(etaBins)-1,len(ptBins)-1,len(isoBins)-1,len(isoBins)-1),order='F'),order='C')
hDY = np.array(fDY['DY'][:].reshape((len(zmassBins)-1,len(etaBins)-1,len(ptBins)-1,len(isoBins)-1,len(isoBins)-1),order='F'),order='C')

#### mass
fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
ax1.set_title("mass_iso1_1_iso2_1", fontsize=18)
ax1.set_ylabel('number of events')
ax2.set_ylabel('data/prediction')
ax2.set_xlabel('dimuon mass')
massdata = np.sum(hdata,axis=(1,2,3,4))[:]
massDY = np.sum(hDY,axis=(1,2,3,4))[:]
hep.histplot([massdata],bins = zmassBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
hep.histplot([massDY],bins = zmassBins, histtype = 'fill',linestyle = 'solid', color =["orange"], label=["DY"], stack = True, ax=ax1)
ax2.set_ylim([0.9, 1.1])
hep.histplot([massdata/massDY], bins = zmassBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
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
hep.histplot([etadata],bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
hep.histplot([etaDY],bins = etaBins, histtype = 'fill',linestyle = 'solid', color =["orange"], label=["DY"], stack = True, ax=ax1)
ax2.set_ylim([0.9, 1.1])
hep.histplot([etadata/etaDY], bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
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
hep.histplot([ptdata],bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
hep.histplot([ptDY],bins = ptBins, histtype = 'fill',linestyle = 'solid', color =["orange"], label=["DY"], stack = True, ax=ax1)
ax2.set_ylim([0.9, 1.1])
hep.histplot([ptdata/ptDY], bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
ax1.legend(loc='upper right', frameon=True)
plt.savefig('pt_iso1_1_iso2_1.png')
plt.cla()
