from __future__ import print_function
from multiprocessing import Pool
import sys
import ROOT
ROOT.gROOT.SetBatch()

filenames = [
'rsg2',
'rsg3',
'rsg4',
'rsg5',
'rsg6',
'ttbar',
#'qcd'
]

legends = [
'RSG 2TeV',
'RSG 3TeV',
'RSG 4TeV',
'RSG 5TeV',
'RSG 6TeV',
'ttbar',
'non-top multijet'
]

nevts=[
399988,
399992,
399990,
399989,
399987,
12769661,
19713175
]

xsecs=[
1000,
1000,
1000,
1000,
1000,
21270,
1253000
]

target_lumi = [
300,1000,3000
]

selections = [
'pre','full'
]

hasweight = [
False,
False,
False,
False,
False,
True,
False
]

#outfile = ROOT.TFile('outfile.root','RECREATE')
templates = ROOT.TFile('theta.root','RECREATE')

folder='output/'


class histos:
	def __init__(self, selection, sample, lumi, outfile):
		outfile.cd()
		self.sample=sample
		self.top1_pt = ROOT.TH1F("top1_pt_"+selection+"_"+filenames[sample]+'_'+str(lumi),";p_{T} leading jet;Events",100,0,4000)
		self.top1_eta = ROOT.TH1F("top1_eta_"+selection+"_"+filenames[sample]+'_'+str(lumi),";#eta leading jet;Events",100,-5,5)
		self.top1_phi = ROOT.TH1F("top1_phi_"+selection+"_"+filenames[sample]+'_'+str(lumi),";#phi leading jet;Events",100,-4,4)
		self.top1_sdmass = ROOT.TH1F("top1_sdmass_"+selection+"_"+filenames[sample]+'_'+str(lumi),";m_{SD} leading jet;Events",100,0,300)
		self.top1_tau32 = ROOT.TH1F("top1_tau32_"+selection+"_"+filenames[sample]+'_'+str(lumi),";#tau_{3}/#tau_2 leading jet;Events",100,0,1)
		self.top1_btag = ROOT.TH1F("top1_btag_"+selection+"_"+filenames[sample]+'_'+str(lumi),";b tag leading jet;Events",2,0,2)
		self.top2_pt = ROOT.TH1F("top2_pt_"+selection+"_"+filenames[sample]+'_'+str(lumi),";p_{T} subleading jet;Events",100,0,4000)
		self.top2_eta = ROOT.TH1F("top2_eta_"+selection+"_"+filenames[sample]+'_'+str(lumi),";#eta subleading jet;Events",100,-5,5)
		self.top2_phi = ROOT.TH1F("top2_phi_"+selection+"_"+filenames[sample]+'_'+str(lumi),";#phi subleading jet;Events",100,-4,4)
		self.top2_sdmass = ROOT.TH1F("top2_sdmass_"+selection+"_"+filenames[sample]+'_'+str(lumi),";m_{SD} subleading jet;Events",100,0,300)
		self.top2_tau32 = ROOT.TH1F("top2_tau32_"+selection+"_"+filenames[sample]+'_'+str(lumi),";#tau_{3}/#tau_2 subleading jet",100,0,1)
		self.top2_btag = ROOT.TH1F("top2_btag_"+selection+"_"+filenames[sample]+'_'+str(lumi),";b tag subleading jet;Events",2,0,2)
		self.zp_m = ROOT.TH1F("zp_m_"+selection+"_"+filenames[sample]+'_'+str(lumi),";m_{t\bar{t}};Events",100,0,4000)
		self.zp_dy = ROOT.TH1F("zp_dy_"+selection+"_"+filenames[sample]+'_'+str(lumi),";\Delta Y;Events",100,0,4)
		self.zp_eta = ROOT.TH1F("zp_eta_"+selection+"_"+filenames[sample]+'_'+str(lumi),";#eta_{t\bar{t}};Events",100,-5,5)
		self.zp_phi = ROOT.TH1F("zp_phi_"+selection+"_"+filenames[sample]+'_'+str(lumi),";#phi_{t\bar{t}};Events",100,-4,4)
		self.zp_pt = ROOT.TH1F("zp_pt_"+selection+"_"+filenames[sample]+'_'+str(lumi),";p_{T};t\bar{t}};Events",100,0,4000)
		self.zp_btag = ROOT.TH1F("zp_btag_"+selection+"_"+filenames[sample]+'_'+str(lumi),";total b tags;Events",3,0,3)

		self.zp_m_hdy_0b = ROOT.TH1F("zp_m_hdy_0b_"+selection+"_"+filenames[sample]+'_'+str(lumi),";m_{t\bar{t}};Events",100,0,4000)
		self.zp_m_hdy_1b = ROOT.TH1F("zp_m_hdy_1b_"+selection+"_"+filenames[sample]+'_'+str(lumi),";m_{t\bar{t}};Events",100,0,4000)
		self.zp_m_hdy_2b = ROOT.TH1F("zp_m_hdy_2b_"+selection+"_"+filenames[sample]+'_'+str(lumi),";m_{t\bar{t}};Events",100,0,4000)
		self.zp_m_ldy_0b = ROOT.TH1F("zp_m_ldy_0b_"+selection+"_"+filenames[sample]+'_'+str(lumi),";m_{t\bar{t}};Events",100,0,4000)
		self.zp_m_ldy_1b = ROOT.TH1F("zp_m_ldy_1b_"+selection+"_"+filenames[sample]+'_'+str(lumi),";m_{t\bar{t}};Events",100,0,4000)
		self.zp_m_ldy_2b = ROOT.TH1F("zp_m_ldy_2b_"+selection+"_"+filenames[sample]+'_'+str(lumi),";m_{t\bar{t}};Events",100,0,4000)

		self.zp_m_0b = ROOT.TH1F("zp_m_0b_"+selection+"_"+filenames[sample]+'_'+str(lumi),";m_{t\bar{t}};Events",100,0,4000)
		self.zp_m_1b = ROOT.TH1F("zp_m_1b_"+selection+"_"+filenames[sample]+'_'+str(lumi),";m_{t\bar{t}};Events",100,0,4000)
		self.zp_m_2b = ROOT.TH1F("zp_m_2b_"+selection+"_"+filenames[sample]+'_'+str(lumi),";m_{t\bar{t}};Events",100,0,4000)

		self.sample_weight = 1.0*lumi*xsecs[sample]/nevts[sample]

	def save(self):
		#outfile.cd()
		self.top1_pt.Write(self.top1_pt.GetName())
		self.top1_eta.Write(self.top1_eta.GetName())
		self.top1_phi.Write(self.top1_phi.GetName())
		self.top1_sdmass.Write(self.top1_sdmass.GetName())
		self.top1_tau32.Write(self.top1_tau32.GetName())
		self.top1_btag.Write(self.top1_btag.GetName())
		self.top2_pt.Write(self.top2_pt.GetName())
		self.top2_eta.Write(self.top2_eta.GetName())
		self.top2_phi.Write(self.top2_phi.GetName())
		self.top2_sdmass.Write(self.top2_sdmass.GetName())
		self.top2_tau32.Write(self.top2_tau32.GetName())
		self.top2_btag.Write(self.top2_btag.GetName())
		self.zp_m.Write(self.zp_m.GetName())
		self.zp_dy.Write(self.zp_dy.GetName())
		self.zp_eta.Write(self.zp_eta.GetName())
		self.zp_phi.Write(self.zp_phi.GetName())
		self.zp_pt.Write(self.zp_pt.GetName())
		self.zp_btag.Write(self.zp_btag.GetName())

		self.zp_m_hdy_0b.Write(self.zp_m_hdy_0b.GetName())
		self.zp_m_hdy_1b.Write(self.zp_m_hdy_1b.GetName())
		self.zp_m_hdy_2b.Write(self.zp_m_hdy_2b.GetName())
		self.zp_m_ldy_0b.Write(self.zp_m_ldy_0b.GetName())
		self.zp_m_ldy_1b.Write(self.zp_m_ldy_1b.GetName())
		self.zp_m_ldy_2b.Write(self.zp_m_ldy_2b.GetName())

		self.zp_m_0b.Write(self.zp_m_0b.GetName())
		self.zp_m_1b.Write(self.zp_m_1b.GetName())
		self.zp_m_2b.Write(self.zp_m_2b.GetName())

	def print(self):
		self.top1_pt.SaveAs('plots/'+self.top1_pt.GetName()+'.pdf')
		self.top1_eta.SaveAs('plots/'+self.top1_eta.GetName()+'.pdf')
		self.top1_phi.SaveAs('plots/'+self.top1_phi.GetName()+'.pdf')
		self.top1_sdmass.SaveAs('plots/'+self.top1_sdmass.GetName()+'.pdf')
		self.top1_tau32.SaveAs('plots/'+self.top1_tau32.GetName()+'.pdf')
		self.top1_btag.SaveAs('plots/'+self.top1_btag.GetName()+'.pdf')
		self.top2_pt.SaveAs('plots/'+self.top2_pt.GetName()+'.pdf')
		self.top2_eta.SaveAs('plots/'+self.top2_eta.GetName()+'.pdf')
		self.top2_phi.SaveAs('plots/'+self.top2_phi.GetName()+'.pdf')
		self.top2_sdmass.SaveAs('plots/'+self.top2_sdmass.GetName()+'.pdf')
		self.top2_tau32.SaveAs('plots/'+self.top2_tau32.GetName()+'.pdf')
		self.top2_btag.SaveAs('plots/'+self.top2_btag.GetName()+'.pdf')
		self.zp_m.SaveAs('plots/'+self.zp_m.GetName()+'.pdf')
		self.zp_dy.SaveAs('plots/'+self.zp_dy.GetName()+'.pdf')
		self.zp_eta.SaveAs('plots/'+self.zp_eta.GetName()+'.pdf')
		self.zp_phi.SaveAs('plots/'+self.zp_phi.GetName()+'.pdf')
		self.zp_pt.SaveAs('plots/'+self.zp_pt.GetName()+'.pdf')
		self.zp_btag.SaveAs('plots/'+self.zp_btag.GetName()+'.pdf')

		self.zp_m_hdy_0b.SaveAs('plots/'+self.zp_m_hdy_0b.GetName()+'.pdf')
		self.zp_m_hdy_1b.SaveAs('plots/'+self.zp_m_hdy_1b.GetName()+'.pdf')
		self.zp_m_hdy_2b.SaveAs('plots/'+self.zp_m_hdy_2b.GetName()+'.pdf')
		self.zp_m_ldy_0b.SaveAs('plots/'+self.zp_m_ldy_0b.GetName()+'.pdf')
		self.zp_m_ldy_1b.SaveAs('plots/'+self.zp_m_ldy_1b.GetName()+'.pdf')
		self.zp_m_ldy_2b.SaveAs('plots/'+self.zp_m_ldy_2b.GetName()+'.pdf')

		self.zp_m_0b.SaveAs('plots/'+self.zp_m_0b.GetName()+'.pdf')
		self.zp_m_1b.SaveAs('plots/'+self.zp_m_1b.GetName()+'.pdf')
		self.zp_m_2b.SaveAs('plots/'+self.zp_m_2b.GetName()+'.pdf')

	def fill(self, event):
		weight=self.sample_weight
		if hasweight[self.sample]:
			weight = self.sample_weight*event.weight

		self.top1_pt.Fill(event.top1_pt,weight)
		self.top1_eta.Fill(event.top1_eta,weight)
		self.top1_phi.Fill(event.top1_phi,weight)
		self.top1_sdmass.Fill(event.top1_sdmass,weight)
		self.top1_tau32.Fill(event.top1_tau32,weight)
		self.top1_btag.Fill(event.top1_btag,weight)
		self.top2_pt.Fill(event.top2_pt,weight)
		self.top2_eta.Fill(event.top2_eta,weight)
		self.top2_phi.Fill(event.top2_phi,weight)
		self.top2_sdmass.Fill(event.top2_sdmass,weight)
		self.top2_tau32.Fill(event.top2_tau32,weight)
		self.top2_btag.Fill(event.top2_btag,weight)
		self.zp_m.Fill(event.zp_m,weight)
		self.zp_dy.Fill(event.zp_dy,weight)
		self.zp_eta.Fill(event.zp_eta,weight)
		self.zp_phi.Fill(event.zp_phi,weight)
		self.zp_pt.Fill(event.zp_pt,weight)
		self.zp_btag.Fill(event.zp_btag,weight)

		if event.zp_dy>1.0:
			if event.zp_btag==0:
				self.zp_m_hdy_0b.Fill(event.zp_m,weight)
			elif event.zp_btag==1:
				self.zp_m_hdy_1b.Fill(event.zp_m,weight)
			elif event.zp_btag==2:
				self.zp_m_hdy_2b.Fill(event.zp_m,weight)
		else:
			if event.zp_btag==0:
				self.zp_m_ldy_0b.Fill(event.zp_m,weight)
			elif event.zp_btag==1:
				self.zp_m_ldy_1b.Fill(event.zp_m,weight)
			elif event.zp_btag==2:
				self.zp_m_ldy_2b.Fill(event.zp_m,weight)

		if event.zp_btag==0:
			self.zp_m_0b.Fill(event.zp_m,weight)
		elif event.zp_btag==1:
			self.zp_m_1b.Fill(event.zp_m,weight)
		elif event.zp_btag==2:
			self.zp_m_2b.Fill(event.zp_m,weight)

def doplots(sample):
	out = ROOT.TFile('plots/outfile_'+filenames[sample]+'.root','RECREATE')
	f = ROOT.TFile.Open(folder+filenames[sample]+'.root')

	hist_dict={}
	for i in selections:
		hist_dict[i]={}
		for j in target_lumi:
			hist_dict[i][j]=histos(i,sample,j,out)
	cnt=0
	lng=f.Delphes.GetEntries()
	for event in f.Delphes :
		cnt=cnt+1
		if cnt%100==0:
			print(legends[sample]+': '+"{:.2f}".format(cnt*100.0/lng)+'%'+' '*10,end='\r')
			sys.stdout.flush()
		#fill preselection
		for j in target_lumi:
			hist_dict['pre'][j].fill(event)

		#fill selection
		if (event.top1_sdmass>105 and event.top1_sdmass<210 and #mass top1
			event.top2_sdmass>105 and event.top2_sdmass<210 and #mass top2
			event.top1_tau32<0.65 and event.top2_tau32<0.65): #nsub top1+top2
			for j in target_lumi:
				hist_dict['full'][j].fill(event)

	for i in selections:
		for j in target_lumi:
			hist_dict[i][j].save()
	f.Close()
	out.Close()

if __name__ == '__main__':
	# doplots(1)
    p = Pool(len(filenames))
    print(p.map(doplots, range(len(filenames))))
