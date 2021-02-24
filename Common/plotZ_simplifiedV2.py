import os
import sys
sys.path.append('../Common/data/')
import h5py
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
from binning import ptBins, etaBins, isoBins, zmassBins, qtBins, pvBins, metBins
plt.style.use([hep.style.ROOT])
#hep.cms.label(loc=0, year=2016, lumi=35.9, data=True)
#hep.cms.text('Simulation')


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


def drawMuons(folder, DYFiles, TopFiles, DibosonFiles,logyscale):
    histonames = ['DY_muons']
    shape = ((len(zmassBins)-1)*(len(etaBins)-1)*(len(ptBins)-1)*(len(etaBins)-1)*(len(ptBins)-1))
    ytag=""
    if logyscale : ytag="log y"
    haddFiles(DYFiles,"DY",histonames, shape)

    fdata = h5py.File(folder+'data.hdf5', mode='r+')
    fDY = h5py.File(folder+'DY.hdf5', mode='r+')
    
    hdata = np.array(fdata['data_muons'][:].reshape((len(zmassBins)-1,len(etaBins)-1,len(ptBins)-1,len(etaBins)-1,len(ptBins)-1),order='F'),order='C')
    hDY = np.array(fDY['DY_muons'][:].reshape((len(zmassBins)-1,len(etaBins)-1,len(ptBins)-1,len(etaBins)-1,len(ptBins)-1),order='F'),order='C')


    hewk = hDY

    #### mass
    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    ax1.set_title("mass", fontsize=18)
    ax1.set_ylabel('number of events')
    if logyscale: ax1.set_yscale('log')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('dimuon  mass')

    zmassdata = np.sum(hdata,axis=(1,2,3,4))[:]
    zmassDY = np.sum(hDY,axis=(1,2,3,4))[:]
    zmassewk = np.sum(hewk,axis=(1,2,3,4))[:]
    hep.histplot([zmassdata],bins = zmassBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
    hep.histplot([zmassDY],bins = zmassBins, histtype = 'fill',linestyle = 'solid', color =["orange"], label=["DY"], stack = True, ax=ax1)
    ax2.set_ylim([0.9, 1.1])
    hep.histplot([zmassdata/zmassewk], bins = zmassBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.savefig('{}/zmass_muons1{}.png'.format(folder,ytag))
    plt.cla()

    
    #### eta 1
    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    ax1.set_title("eta1", fontsize=18)
    ax1.set_ylabel('number of events')
    if logyscale: ax1.set_yscale('log')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('muon1 $\eta$')
    etadata = np.sum(hdata,axis=(0,2,3,4))[:]
    etaDY = np.sum(hDY,axis=(0,2,3,4))[:]
    etaewk = np.sum(hewk,axis=(0,2,3,4))[:]
    hep.histplot([etadata],bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
    hep.histplot([etaDY],bins = etaBins, histtype = 'fill',linestyle = 'solid', color =["orange"], label=["DY"], stack = True, ax=ax1)
    ax2.set_ylim([0.9, 1.1])
    hep.histplot([etadata/etaewk], bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.savefig('{}/eta1{}.png'.format(folder,ytag))
    plt.cla()
    
    #### pt 1
    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    ax1.set_title("pt1", fontsize=18)
    ax1.set_ylabel('number of events')
    if logyscale: ax1.set_yscale('log')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('muon1 $p_T$')
    ptdata = np.sum(hdata,axis=(0,1,3,4))[:]
    ptDY = np.sum(hDY,axis=(0,1,3,4))[:]
    ptewk = np.sum(hewk,axis=(0,1,3,4))[:]
    ptBinsNew=ptBins
    ptBinsNew[31]=56.
    hep.histplot([ptdata],bins = ptBinsNew, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
    hep.histplot([ptDY],bins = ptBinsNew, histtype = 'fill',linestyle = 'solid', color =["orange"], label=["DY"], stack = True, ax=ax1)
    ax2.set_ylim([0.9, 1.1])
    hep.histplot([ptdata/ptDY], bins = ptBinsNew, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.savefig('{}/pt1{}.png'.format(folder,ytag))
    plt.cla()

    
    #### eta 2
    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    #ax1.set_title("eta2", fontsize=18)
    ax1.set_ylabel('number of events')
    if logyscale: ax1.set_yscale('log')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('muon2 $\eta$')
    etadata = np.sum(hdata,axis=(0,1,2,4))[:]
    etaDY = np.sum(hDY,axis=(0,1,2,4))[:]
    etaewk = np.sum(hewk,axis=(0,1,2,4))[:]
    hep.histplot([etadata],bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
    hep.histplot([etaDY],bins = etaBins, histtype = 'fill',linestyle = 'solid', color =["orange"], label=["DY"], stack = True, ax=ax1)
    ax2.set_ylim([0.9, 1.1])
    hep.histplot([etadata/etaewk], bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.savefig('{}/eta2{}.png'.format(folder,ytag))
    plt.cla()

    #### pt 2
    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    #ax1.set_title("pt1", fontsize=18)
    ax1.set_ylabel('number of events')
    if logyscale: ax1.set_yscale('log')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('muon2 $p_T$')
    ptdata = np.sum(hdata,axis=(0,1,2,3))[:]
    ptDY = np.sum(hDY,axis=(0,1,2,3))[:]
    ptewk = np.sum(hewk,axis=(0,1,2,3))[:]
    hep.histplot([ptdata],bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
    hep.histplot([ptDY],bins = ptBins, histtype = 'fill',linestyle = 'solid', color =["orange"], label=["DY"], stack = True, ax=ax1)
    ax2.set_ylim([0.9, 1.1])
    hep.histplot([ptdata/ptDY], bins = ptBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.savefig('{}/pt2{}.png'.format(folder,ytag))
    plt.cla()
    fdata.close()
    fDY.close()

def drawDiMuon(folder, DYFiles, TopFiles, DibosonFiles, logyscale):
    histonames = ['DY_dimuon']
    #zmassBins,qtBins, etaBins,metBins
    shape = ((len(zmassBins)-1)*(len(qtBins)-1)*(len(etaBins)-1)*(len(metBins)-1))
    ytag=""
    if logyscale : ytag="log y"
    haddFiles(DYFiles,"DY",histonames, shape)
    
    fdata = h5py.File(folder+'data.hdf5', mode='r+')
    fDY = h5py.File(folder+'DY.hdf5', mode='r+')
    
    hdata = np.array(fdata['data_dimuon'][:].reshape((len(zmassBins)-1,len(qtBins)-1,len(etaBins)-1,len(metBins)-1),order='F'),order='C')
    hDY = np.array(fDY['DY_dimuon'][:].reshape((len(zmassBins)-1,len(qtBins)-1,len(etaBins)-1,len(metBins)-1),order='F'),order='C')

    hewk = hDY

    #### mass
    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    #ax1.set_title("mass", fontsize=18)
    ax1.set_ylabel('number of events')
    if logyscale: ax1.set_yscale('log')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('dimuon  mass')
    zmassdata = np.sum(hdata,axis=(1,2,3))[:]
    zmassDY = np.sum(hDY,axis=(1,2,3))[:]
    zmassewk = np.sum(hewk,axis=(1,2,3))[:]
    hep.histplot([zmassdata],bins = zmassBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
    hep.histplot([zmassDY],bins = zmassBins, histtype = 'fill',linestyle = 'solid', color =["orange"], label=["DY"], stack = True, ax=ax1)
    ax2.set_ylim([0.9, 1.1])
    hep.histplot([zmassdata/zmassewk], bins = zmassBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.savefig('{}/zmass_crosscheck{}.png'.format(folder,ytag))
    plt.cla()

    #### pt 1
    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    #ax1.set_title("pt1", fontsize=18)
    ax1.set_ylabel('number of events')
    if logyscale: ax1.set_yscale('log')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('dimuon $q_T$')
    qtdata = np.sum(hdata,axis=(0,2,3))[:]
    qtDY = np.sum(hDY,axis=(0,2,3))[:]
    qtewk = np.sum(hewk,axis=(0,2,3))[:]
    hep.histplot([qtdata],bins = qtBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
    hep.histplot([qtDY],bins = qtBins, histtype = 'fill',linestyle = 'solid', color =["orange"], label=["DY"], stack = True, ax=ax1)
    ax2.set_ylim([0.9, 1.1])
    hep.histplot([qtdata/qtDY], bins = qtBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.savefig('{}/qtZ{}.png'.format(folder,ytag))
    plt.cla()

    #### rapidity
    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    #ax1.set_title("eta1", fontsize=18)
    ax1.set_ylabel('number of events')
    if logyscale: ax1.set_yscale('log')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('dimuon rapidity')
    rapdata = np.sum(hdata,axis=(0,1,3))[:]
    rapDY = np.sum(hDY,axis=(0,1,3))[:]
    #rapTop = np.sum(hTop,axis=(0,1,3))[:]
    #rapDiboson = np.sum(hDiboson,axis=(0,1,3))[:]
    rapewk = np.sum(hewk,axis=(0,1,3))[:]
    hep.histplot([rapdata],bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
    hep.histplot([rapDY],bins = etaBins, histtype = 'fill',linestyle = 'solid', color =["orange"], label=["DY"], stack = True, ax=ax1)
    ax2.set_ylim([0.9, 1.1])
    hep.histplot([rapdata/rapewk], bins = etaBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.savefig('{}/rapidityZ{}.png'.format(folder,ytag))
    plt.cla()

    #### MET
    fig, (ax1, ax2) = plt.subplots(nrows=2,gridspec_kw={'height_ratios': [3, 1]})
    #ax1.set_title("met1", fontsize=18)
    ax1.set_ylabel('number of events')
    if logyscale: ax1.set_yscale('log')
    ax2.set_ylabel('data/prediction')
    ax2.set_xlabel('MET')
    metdata = np.sum(hdata,axis=(0,1,2))[:]
    metDY = np.sum(hDY,axis=(0,1,2))[:]
    #metTop = np.sum(hTop,axis=(0,1,2))[:]
    #metDiboson = np.sum(hDiboson,axis=(0,1,2))[:]
    metewk = np.sum(hewk,axis=(0,1,2))[:]
    hep.histplot([metdata],bins = metBins, histtype = 'errorbar', color = "k", stack = False, ax=ax1, label = ["data"])
    hep.histplot([metDY],bins = metBins, histtype = 'fill',linestyle = 'solid', color =["orange"], label=["DY"], stack = True, ax=ax1)
    ax2.set_ylim([0.9, 1.1])
    hep.histplot([metdata/metewk], bins = metBins, histtype = 'errorbar', color = "k", stack = False, ax=ax2)
    ax1.legend(loc='upper right', frameon=True)
    plt.savefig('{}/met{}.png'.format(folder,ytag))
    plt.cla()
    fdata.close()
    fDY.close()
    #fTop.close()
    #fDiboson.close()

print(sys.argv)
folder = sys.argv[1]
logyscale=False
if len(sys.argv) > 2:
    logyscale=int(sys.argv[2])

print("Logy=",logyscale)


DYFiles = ["DYJetsToMuMu_M50.hdf5"]#,"DYJetsToTauTau_M50.hdf5"]
TopFiles = ["ST_t-channel_muDecays.hdf5", "ST_t-channel_tauDecays.hdf5","ST_s-channel_4f_leptonDecays.hdf5","ST_t-channel_top_5f_InclusiveDecays.hdf5","TTToSemiLeptonic.hdf5", "TTTo2L2Nu.hdf5"]
DibosonFiles = ["WW.hdf5","WZ.hdf5"]


drawMuons(folder, DYFiles, TopFiles, DibosonFiles, logyscale)
drawDiMuon(folder, DYFiles, TopFiles, DibosonFiles, logyscale)
#drawPV(folder, DYFiles, TopFiles, DibosonFiles)


########NPV
