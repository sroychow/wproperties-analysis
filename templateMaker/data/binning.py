import ROOT

qtBins = ROOT.vector('float')([0., 4., 8., 12., 16., 20., 24., 28., 32., 40., 60., 100., 200.])
yBins = ROOT.vector('float')([0, 0.4, 0.8, 1.2, 1.6, 2.0, 2.4, 3.0, 6.0])
ptBins = ROOT.vector('float')([25.+i*0.5 for i in range(61)])
etaBins = ROOT.vector('float')([-2.4+i*0.1 for i in range(49)])
