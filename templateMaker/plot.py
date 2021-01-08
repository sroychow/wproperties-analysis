import h5py
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import ROOT
from root_numpy import array2hist
from array import array
plt.style.use([hep.style.ROOT, hep.style.firamath])
#hep.cms.label(loc=0)
hep.cms.text('Simulation')

qtBins = ROOT.vector('float')([0., 4., 8., 12., 16., 20., 24., 28., 32., 40., 60., 100., 200.])
yBins = ROOT.vector('float')([0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 3.0, 6.0])
ptBins = ROOT.vector('float')([25.+i*0.5 for i in range(61)])
etaBins = ROOT.vector('float')([-2.4+i*0.1 for i in range(49)])

fewk = h5py.File('PLOTS/SignalTemplates.hdf5', mode='r+')
helxsecs = ["L", "I", "T", "A", "P", "7", "8", "9", "UL"]
for hel in helxsecs:
    h = np.array(fewk['xsecs_{}'.format(hel)][:].reshape((len(etaBins)-1,len(ptBins)-1,len(yBins)-1,len(qtBins)-1),order='F'),order='C')
    hep.hist2dplot(np.sum(h,axis=(0,1))[:,:], yBins, qtBins)
    plt.savefig('PLOTS/xsecs_{}.png'.format(hel))
    plt.clf()
    

#plt.show()


