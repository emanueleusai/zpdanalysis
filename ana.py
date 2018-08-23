# Auto generated configuration file
# using: 
# Revision: 1.381.2.7 
# Source: /local/reps/CMSSW/CMSSW/Configuration/PyReleaseValidation/python/ConfigBuilder.py,v 
# with command line options: Configuration/GenProduction/python/EightTeV/Hadronizer_MgmMatchTuneZ2star_8TeV_madgraph_tauola_cff.py --step GEN --beamspot Realistic8TeVCollision --conditions START52_V9::All --pileup NoPileUp --datamix NODATAMIXER --eventcontent RAWSIM --datatier GEN -n -1 --python_filename=Temp_Hadronizer_5498_1.py --filein root://eoscms//eos/cms//store/lhe/5498/DY1JetsToLL_M-50_8TeV-madgraph_10001.lhe --no_output --no_exec
import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
options = VarParsing ('analysis')
options.parseArguments()

process = cms.Process('ANA')

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedRealistic8TeVCollision_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:mc', '')
process.maxEvents = cms.untracked.PSet(
    # input = cms.untracked.int32(options.maxEvents)
    input = cms.untracked.int32(-1)
)

process.MessageLogger.cerr.FwkReport.reportEvery = 10000

process.source = cms.Source(
    "PoolSource",
    # fileNames  = cms.untracked.vstring(options.inputFiles),
    fileNames  = cms.untracked.vstring(
'/store/mc/PhaseIISummer17GenOnly/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/GEN/93X_upgrade2023_realistic_v5-v1/10000/FEE92466-C749-E811-ACA1-FA163EACCAC4.root',
'/store/mc/PhaseIISummer17GenOnly/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/GEN/93X_upgrade2023_realistic_v5-v1/10000/FED25C10-E849-E811-B909-FA163EBCBFA4.root',
'/store/mc/PhaseIISummer17GenOnly/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/GEN/93X_upgrade2023_realistic_v5-v1/10000/FE990FC5-3B4A-E811-A3F8-44A842B4CC98.root',
'/store/mc/PhaseIISummer17GenOnly/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/GEN/93X_upgrade2023_realistic_v5-v1/10000/FE909EDB-BD49-E811-9DB3-14DDA9243247.root',
'/store/mc/PhaseIISummer17GenOnly/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/GEN/93X_upgrade2023_realistic_v5-v1/10000/FE77A672-5A4A-E811-801C-FA163E454E85.root',
'/store/mc/PhaseIISummer17GenOnly/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/GEN/93X_upgrade2023_realistic_v5-v1/10000/FE257A04-ED49-E811-B913-02163E019F62.root',
'/store/mc/PhaseIISummer17GenOnly/QCD_Mdijet-1000toInf_TuneCUETP8M1_14TeV-pythia8/GEN/93X_upgrade2023_realistic_v5-v1/10000/FE20F29F-294A-E811-A5D2-FA163EF29411.root'
    	),
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)


process.dummy2 = cms.EDAnalyzer("GenXSecAnalyzer")



# Path and EndPath definitions
process.ana = cms.Path(process.dummy2)
# Schedule definition
process.schedule = cms.Schedule(process.ana)
