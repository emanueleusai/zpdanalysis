from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.General.requestName = 'metstudies3j_2'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = True

config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'MetStudies/python/ConfFile_cfg.py'
config.JobType.maxMemoryMB = 2500
config.JobType.outputFiles = ['metstudies_output.root']
#config.JobType.numCores = 4

config.Data.inputDataset = '/DYToLL-M-50_3J_14TeV-madgraphMLM-pythia8/PhaseIISpr18AODMiniAOD-PU200_93X_upgrade2023_realistic_v5-v1/MINIAODSIM'
#config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
config.Data.unitsPerJob = 1
config.Data.outLFNDirBase = '/store/user/%s/' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'metstudies3j_2'
config.Data.ignoreLocality = True
#config.Data.totalUnits = 100000
#config.Data.userInputFiles = open('step3_pigun01_list').readlines()
#Data.outputPrimaryDataset

config.Site.storageSite = 'T3_US_FNALLPC'
#config.Site.ignoreGlobalBlacklist = True
config.Site.whitelist = ['T2_*']
#config.Site.whitelist = ['T3_US_FNALLPC']
#config.Site.blacklist = ['T2_CN_Beijing']