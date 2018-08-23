import FWCore.ParameterSet.Config as cms

process = cms.Process("MetStudies")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
    # replace 'myfile.root' with the source file you want to use
    fileNames = cms.untracked.vstring(
        'file:/afs/cern.ch/work/e/eusai/public/phase2/CMSSW_9_3_5/src/PhaseTwoAnalysis/0C1CCD87-9346-E811-99E8-0025905A6056.root'
    )
)

process.metstudies = cms.EDAnalyzer('MetStudies'
)
# process.options = cms.untracked.PSet( wantSummary = cms.untracked.bool(True))
# process.options.numberOfThreads=cms.untracked.uint32(8)
# process.options.numberOfStreams=cms.untracked.uint32(0)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.p = cms.Path(process.metstudies)
