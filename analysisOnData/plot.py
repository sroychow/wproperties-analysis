import h5py
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
plt.style.use([hep.style.ROOT, hep.style.firamath])
#hep.cms.label(loc=0)
hep.cms.text('Simulation')

ptBins = [25.+i*0.5 for i in range(61)]
etaBins = [-2.4+i*0.1 for i in range(49)]
chargeBins = [-2. +i*2. for i in range(3)]
mTBins = [0.,30.,40.,2000.]
isoBins = [0.,0.15,1.]

ewkFiles = ["output/DYJetsToLL_M10to50.hdf5", "output/ST_t-channel_antitop_4f_inclusiveDecays.hdf5","output/ST_tW_top_5f_inclusiveDecays.hdf5","output/TTJets_SingleLeptFromTbar.hdf5","output/WZ.hdf5",\
"output/DYJetsToLL_M50.hdf5","output/ST_t-channel_top_4f_inclusiveDecays_13TeV.hdf5","output/TTJets_DiLept.hdf5","output/WJetsToLNu.hdf5","output/ZZ.hdf5",\
"output/ST_s-channel_4f_leptonDecays.hdf5","output/ST_tW_antitop_5f_inclusiveDecays.hdf5","output/TTJets_SingleLeptFromT.hdf5","output/WW.hdf5"]

histonames = ['test', 'test_sumw2']

def haddFiles(fileList, histonames, shape):

    f = h5py.File('output/ewk.hdf5', mode='w')
    for name in histonames:
        #print(name, shape)
        dset = f.create_dataset(name=name, shape=[shape], dtype='float64')
        tmp = np.zeros([shape],dtype='float64')
        for file in fileList:
            ftmp = h5py.File(file, mode='r+')
            tmp += ftmp[name][:]
        dset[...] = tmp
    return

shape = (len(etaBins)-1) * (len(ptBins)-1) * (len(chargeBins)-1) * (len(mTBins)-1) * (len(isoBins)-1)
haddFiles(ewkFiles, histonames, shape)

fdata = h5py.File('output/data.hdf5', mode='r+')
fewk = h5py.File('output/WJetsToLNu.hdf5', mode='r+')

hdata = np.array(fdata['test'][:].reshape((len(etaBins)-1,len(ptBins)-1,len(chargeBins)-1,len(mTBins)-1,len(isoBins)-1),order='F'),order='C')
hewk = np.array(fewk['test'][:].reshape((len(etaBins)-1,len(ptBins)-1,len(chargeBins)-1,len(mTBins)-1,len(isoBins)-1),order='F'),order='C')

etadata = np.sum(hdata,axis=1)[:,-1,-1,0]
etaewk = np.sum(hewk,axis=1)[:,-1,-1,0]
print(np.sum(etaewk))

hep.histplot([etadata,etaewk],etaBins)
#hep.histplot([etaewk],etaBins)

plt.show()


