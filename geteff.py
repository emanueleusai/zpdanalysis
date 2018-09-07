import ROOT
from ROOT import TFile,gROOT
ROOT.gROOT.SetBatch()


gennames=[
'rsg2',
'rsg3',
'rsg4',
'rsg5',
'rsg6'
]

genfiles=['plots/outfile_'+gennames[i]+'.root' for i in range(len(gennames))]

nevts=[
399988,
399992,
399990,
399989,
399987,
]

def rounding(numero):
	return '%s' % float('%.2g' % float(numero))

for i in range(len(genfiles)):
	print gennames[i]
	f=TFile(genfiles[i],'READ')
	h=f.Get("zp_pt_full_3000")
	n=h.GetEntries()
	e=float(n)/nevts[i]*100
	print rounding(e)
	f.Close()


gennames=[
'2000',
'3000',
'4000',
'5000',
'6000'
]

hists=['zpMass_3000p0fbinv_isE_nT0_nB0__sig',
'zpMass_3000p0fbinv_isE_nT0_nB1__sig',
'zpMass_3000p0fbinv_isE_nT1_nB0__sig',
'zpMass_3000p0fbinv_isE_nT1_nB1__sig',

'zpMass_3000p0fbinv_isM_nT0_nB0__sig',
'zpMass_3000p0fbinv_isM_nT0_nB1__sig',
'zpMass_3000p0fbinv_isM_nT1_nB0__sig',
'zpMass_3000p0fbinv_isM_nT1_nB1__sig']


genfiles=['plots/templates_zpMass_ZpM'+gennames[i]+'_3000p0fbinv_rebinned_stat1p1.root' for i in range(len(gennames))]
for i in range(len(genfiles)):
	print gennames[i]
	f=TFile(genfiles[i],'READ')
	n=0
	for hn in hists:
		h=f.Get(hn)
		n=n+h.GetEntries()
	e=float(n)/nevts[i]*100
	print rounding(e)
	f.Close()