import ROOT

qtBins = ROOT.vector('float')([0., 4., 8., 12., 16., 20., 24., 28., 32., 40., 60., 100., 200.])
yBins = ROOT.vector('float')([0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 3.0, 6.0])
ptBins = ROOT.vector('float')([25.+i for i in range(31)])
#overflow-Bin
ptBins.push_back(65.)
etaBins = ROOT.vector('float')([-2.4+i*0.1 for i in range(49)])
chargeBins = ROOT.vector('float')(-2. +i*2. for i in range(3))
mTBins = ROOT.vector('float')([0.,30.,150.])
#mTBins = ROOT.vector('float')([i*2 for i in range(76)])
metBins = ROOT.vector('float')([i*2 for i in range(76)])
isoBins = ROOT.vector('float')([0.,0.15,1.])
#isoBins = ROOT.vector('float')([i*0.005 for i in range(41)])
zmassBins = ROOT.vector('float')([70 + i*1. for i in range(41)])
pvBins = ROOT.vector('float')([9.5 + i*1. for i in range(50)])
