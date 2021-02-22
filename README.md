# wproperties-analysis
Git repo gathering all submodules in the w properties analysis in CMS

## how to get this repository

```
git clone --recursive https://github.com/emanca/wproperties-analysis.git wproperties-analysis
cd wproperties-analysis/RDFprocessor/framework
```

## source root master nightlies slc7

`source /cvmfs/sft-nightlies.cern.ch/lcg/views/dev3/latest/x86_64-centos7-gcc8-opt/setup.sh`

`pip install --user -e .`

## How to run the analysis

Preliminary compile subpackages :
```
cd wproperties-analysis/
source setpath.sh
make -j 8
```

Brief description of packages:

* `nanotools`: 
  ** `puWeightProducer`: module which produces putWeight column for MC
  ** `trigObjMatchProducer`: module which creates a selected array of Trigger Objects
  ** `nanoSequence.py` : config file which contains the nanotools sequence for samples
* `templateMaker`: contains all the modules related to event selection
  ** `dySequence.py`: defines the sequence for dimuon event selection
* `config`: directory with final executable configs for various sequences


To run the Z workflow:
```
cd config/
python runZ_fromNANO.py
```

More explanation coming soon!!!