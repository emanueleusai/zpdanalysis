from __future__ import print_function
from multiprocessing import Pool
import sys
import ROOT
from ROOT import TFile,TCanvas,gROOT,gStyle,TLegend,TGraphAsymmErrors,THStack,TIter,kRed,kYellow,kGray,kBlack,TLatex,kOrange,kAzure,TLine,kWhite,kBlue,kTRUE,kFALSE,TColor
import CMS_lumi
import math
ROOT.gROOT.SetBatch()

hexcolor=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
intcolor=[TColor.GetColor(i) for i in hexcolor]

filenames = [
'rsg2',
'rsg3',
'rsg4',
'rsg5',
'rsg6',
'ttbar',
'qcd'
]

legends = [
'm_{g} = 2 TeV',
'm_{g} = 3 TeV',
'm_{g} = 4 TeV',
'm_{g} = 5 TeV',
'm_{g} = 6 TeV',
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

plots=[
'top1_pt',
'top1_eta',
'top1_phi',
'top1_sdmass',
'top1_tau32',
'top1_btag',
'top2_pt',
'top2_eta',
'top2_phi',
'top2_sdmass',
'top2_tau32',
'top2_btag',
'zp_m',
'zp_dy',
'zp_eta',
'zp_phi',
'zp_pt',
'zp_btag',

'zp_m_hdy_0b',
'zp_m_hdy_1b',
'zp_m_hdy_2b',
'zp_m_ldy_0b',
'zp_m_ldy_1b',
'zp_m_ldy_2b',

'zp_m_0b',
'zp_m_1b',
'zp_m_2b',
]

categories=[
'zp_m_hdy_0b',
'zp_m_hdy_1b',
'zp_m_hdy_2b',
'zp_m_ldy_0b',
'zp_m_ldy_1b',
'zp_m_ldy_2b'
]

categories_names=[
'hadh0',
'hadh1',
'hadh2',
'hadl0',
'hadl1',
'hadl2',
]

folder='output/'


class histos:
	def __init__(self, selection, sample, lumi, outfile):
		outfile.cd()
		self.sample=sample
		self.top1_pt = ROOT.TH1F("top1_pt_"+selection+'_'+str(lumi),";p_{T} leading jet [GeV];Events",100,0,4000)
		self.top1_eta = ROOT.TH1F("top1_eta_"+selection+'_'+str(lumi),";#eta leading jet;Events",100,-5,5)
		self.top1_phi = ROOT.TH1F("top1_phi_"+selection+'_'+str(lumi),";#phi leading jet;Events",100,-4,4)
		self.top1_sdmass = ROOT.TH1F("top1_sdmass_"+selection+'_'+str(lumi),";m_{SD} leading jet [GeV];Events",100,0,300)
		self.top1_tau32 = ROOT.TH1F("top1_tau32_"+selection+'_'+str(lumi),";#tau_{3}/#tau_{2} leading jet;Events",100,0,1)
		self.top1_btag = ROOT.TH1F("top1_btag_"+selection+'_'+str(lumi),";b tag leading jet;Events",2,0,2)
		self.top2_pt = ROOT.TH1F("top2_pt_"+selection+'_'+str(lumi),";p_{T} subleading jet [GeV];Events",100,0,4000)
		self.top2_eta = ROOT.TH1F("top2_eta_"+selection+'_'+str(lumi),";#eta subleading jet;Events",100,-5,5)
		self.top2_phi = ROOT.TH1F("top2_phi_"+selection+'_'+str(lumi),";#phi subleading jet;Events",100,-4,4)
		self.top2_sdmass = ROOT.TH1F("top2_sdmass_"+selection+'_'+str(lumi),";m_{SD} subleading jet [GeV];Events",100,0,300)
		self.top2_tau32 = ROOT.TH1F("top2_tau32_"+selection+'_'+str(lumi),";#tau_{3}/#tau_{2} subleading jet",100,0,1)
		self.top2_btag = ROOT.TH1F("top2_btag_"+selection+'_'+str(lumi),";b tag subleading jet;Events",2,0,2)
		self.zp_m = ROOT.TH1F("zp_m_"+selection+'_'+str(lumi),";m_{t#bar{t}} [GeV];Events",200,0,8000)
		self.zp_dy = ROOT.TH1F("zp_dy_"+selection+'_'+str(lumi),";#Delta Y;Events",100,0,4)
		self.zp_eta = ROOT.TH1F("zp_eta_"+selection+'_'+str(lumi),";#eta_{t#bar{t}};Events",100,-5,5)
		self.zp_phi = ROOT.TH1F("zp_phi_"+selection+'_'+str(lumi),";#phi_{t#bar{t}};Events",100,-4,4)
		self.zp_pt = ROOT.TH1F("zp_pt_"+selection+'_'+str(lumi),";p_{T,t#bar{t}} [GeV];Events",100,0,4000)
		self.zp_btag = ROOT.TH1F("zp_btag_"+selection+'_'+str(lumi),";total b tags;Events",3,0,3)

		self.zp_m_hdy_0b = ROOT.TH1F("zp_m_hdy_0b_"+selection+'_'+str(lumi),";m_{t#bar{t}} [GeV];Events",200,0,8000)
		self.zp_m_hdy_1b = ROOT.TH1F("zp_m_hdy_1b_"+selection+'_'+str(lumi),";m_{t#bar{t}} [GeV];Events",200,0,8000)
		self.zp_m_hdy_2b = ROOT.TH1F("zp_m_hdy_2b_"+selection+'_'+str(lumi),";m_{t#bar{t}} [GeV];Events",200,0,8000)
		self.zp_m_ldy_0b = ROOT.TH1F("zp_m_ldy_0b_"+selection+'_'+str(lumi),";m_{t#bar{t}} [GeV];Events",200,0,8000)
		self.zp_m_ldy_1b = ROOT.TH1F("zp_m_ldy_1b_"+selection+'_'+str(lumi),";m_{t#bar{t}} [GeV];Events",200,0,8000)
		self.zp_m_ldy_2b = ROOT.TH1F("zp_m_ldy_2b_"+selection+'_'+str(lumi),";m_{t#bar{t}} [GeV];Events",200,0,8000)

		self.zp_m_0b = ROOT.TH1F("zp_m_0b_"+selection+'_'+str(lumi),";m_{t#bar{t}} [GeV];Events",200,0,8000)
		self.zp_m_1b = ROOT.TH1F("zp_m_1b_"+selection+'_'+str(lumi),";m_{t#bar{t}} [GeV];Events",200,0,8000)
		self.zp_m_2b = ROOT.TH1F("zp_m_2b_"+selection+'_'+str(lumi),";m_{t#bar{t}} [GeV];Events",200,0,8000)

		self.top1_pt.Sumw2()
		self.top1_eta.Sumw2()
		self.top1_phi.Sumw2()
		self.top1_sdmass.Sumw2()
		self.top1_tau32.Sumw2()
		self.top1_btag.Sumw2()
		self.top2_pt.Sumw2()
		self.top2_eta.Sumw2()
		self.top2_phi.Sumw2()
		self.top2_sdmass.Sumw2()
		self.top2_tau32.Sumw2()
		self.top2_btag.Sumw2()
		self.zp_m.Sumw2()
		self.zp_dy.Sumw2()
		self.zp_eta.Sumw2()
		self.zp_phi.Sumw2()
		self.zp_pt.Sumw2()
		self.zp_btag.Sumw2()

		self.zp_m_hdy_0b.Sumw2()
		self.zp_m_hdy_1b.Sumw2()
		self.zp_m_hdy_2b.Sumw2()
		self.zp_m_ldy_0b.Sumw2()
		self.zp_m_ldy_1b.Sumw2()
		self.zp_m_ldy_2b.Sumw2()

		self.zp_m_0b.Sumw2()
		self.zp_m_1b.Sumw2()
		self.zp_m_2b.Sumw2()

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


def make_ratioplot(name, ttbar_file=0, qcd_file=0, signal_files=[], histo=0,rebin=1,minx=0,maxx=0,miny=0,maxy=0,logy=False,
                    xtitle='',ytitle='',textsizefactor=1,signal_legend=[],outfile=0,signal_colors=[], signal_zoom=1, qcd_zoom=1, ttbar_zoom=1,
                    ttbar_legend='t#bar{t}',qcd_legend='QCD from MC',dosys=False,docms=True,legendtitle=''):
  
  ###canvas setting up
  canvas=0
  canvas=TCanvas(name,'',0,0,600,600)
  canvas.SetLeftMargin(0.15)
  canvas.SetRightMargin(0.05)
  canvas.SetTopMargin(0.10)
  canvas.SetBottomMargin(0.10)
  charsize=0.04
  offset=1.9

  ###latex label
  latex=0
  latex=TLatex(0.6,0.7,'13 TeV, 2.69 fb^{-1}')
  latex.SetTextSize(charsize)
  latex.SetNDC(1)
  latex.SetTextFont(42)

  ###legend setting up
  #legend=TLegend(0.0,0.75,0.99,1.04)
  legend=TLegend(0.4,0.6,0.94,0.95)
  legend.SetNColumns(2)
  legend.SetHeader('')
  legend.SetFillStyle(0)
  legend.SetBorderSize(0)


  ###mc stack
  stack=THStack(name+'_stack','')
  
  qcd_histo=qcd_file.Get(histo).Clone(name+'_make_plot')
  qcd_histo.Rebin(rebin)
  ttbar_histo=ttbar_file.Get(histo).Clone()
  ttbar_histo.Rebin(rebin)
  ttbar_histo.SetFillColor(kAzure)
  ttbar_histo.SetLineColor(kAzure)
  ttbar_histo.SetMarkerColor(kAzure)
  if ttbar_zoom!=1:
    ttbar_histo.Scale(ttbar_zoom)  
  legend.AddEntry(ttbar_histo,ttbar_legend,'f')
  qcd_histo.SetFillColor(kOrange)
  qcd_histo.SetLineColor(kOrange)
  qcd_histo.SetMarkerColor(kOrange)
  if qcd_zoom!=1:
      qcd_histo.Scale(qcd_zoom)
  legend.AddEntry(qcd_histo,qcd_legend,'f')

  sum_mc=qcd_histo.Clone(histo+'tmp')
  sum_mc.Add(ttbar_histo)
  stack.Add(ttbar_histo)
  stack.Add(qcd_histo)
  
  sum_mc.SetLineColor(kBlack)
  sum_mc.SetFillStyle(0)
  err=TGraphAsymmErrors(sum_mc)
  legend.AddEntry(err,'Total uncertainty','f')

  if legendtitle=='':
    legend.AddEntry(0,"",'')
    legend.AddEntry(0,"g_{RS} #rightarrow t#bar{t} (2pb)",'')
  else:
    legend.AddEntry(0,"",'')
    legend.AddEntry(0,legendtitle,'')

  ###signal setting up
  signal_histos=[]
  colors=[30,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,55,56,57,58,59,60]
  styles=[5,7,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
  if signal_colors!=[]:
    colors=signal_colors
  for i in range(len(signal_files)):
    signal_histos.append(signal_files[i].Get(histo).Clone())
    signal_histos[i].SetLineWidth(3)
    signal_histos[i].SetLineStyle(styles[i])
    signal_histos[i].SetLineColor(colors[i])
    signal_histos[i].SetMarkerColor(colors[i])
    signal_histos[i].Rebin(rebin)
    if signal_zoom!=1:
      signal_histos[i].Scale(signal_zoom)
    legend.AddEntry(signal_histos[i],signal_legend[i],'l')

  ###mc shape line
  ttbar_line=0
  ttbar_line=ttbar_histo.Clone()
  ttbar_line.SetLineColor(kBlack)
  ttbar_line.SetFillStyle(0)

  ###mc errors
  if dosys:
    sys_diff_qcd=[]
    sys_diff_ttbar=[]
    for imtt in range(1,ttbar_histo.GetNbinsX()+1):
      sys_diff_qcd.append([])
      sys_diff_ttbar.append([])

    #adding stat uncertainties <--removed
    # for imtt in range(1,ttbar_histo.GetNbinsX()+1):
    #   sys_diff_ttbar[imtt-1].append(ttbar_histo.GetBinError(imtt))
    #   sys_diff_ttbar[imtt-1].append(-ttbar_histo.GetBinError(imtt))
    #   sys_diff_qcd[imtt-1].append(qcd_histo.GetBinError(imtt))
    #   sys_diff_qcd[imtt-1].append(-qcd_histo.GetBinError(imtt))
    #adding flat uncertainties
    for imtt in range(1,ttbar_histo.GetNbinsX()+1):
      #ttbar
      for i in [2.4,#pdf
                10.0,#mu
                3.0,#xsec
                6.0,#toppt
                1.0,#lumi
                3.5,#jec
                3.0,#jer
                10.0,#btag
                #3.0,#trig
                10.0,#toptag
                3.0]:#pileup
         sys_diff_ttbar[imtt-1].append(i/100.0*ttbar_histo.GetBinContent(imtt))
         sys_diff_ttbar[imtt-1].append(-i/100.0*ttbar_histo.GetBinContent(imtt))
      closureunc=5.0
      # if '1b' in histo:
      #   closureunc=5.0
      # elif '2b' in histo:
      #   closureunc=10.0
      for i in [2.0,#modmass
                closureunc]:#closure
         sys_diff_qcd[imtt-1].append(i/100.0*qcd_histo.GetBinContent(imtt))
         sys_diff_qcd[imtt-1].append(-i/100.0*qcd_histo.GetBinContent(imtt))
      # #3% trigger
      # sys_diff_ttbar[imtt-1].append(0.03*ttbar_histo.GetBinContent(imtt))
      # sys_diff_ttbar[imtt-1].append(-0.03*ttbar_histo.GetBinContent(imtt))
      # #2.7% lumi
      # sys_diff_ttbar[imtt-1].append(0.023*ttbar_histo.GetBinContent(imtt))
      # sys_diff_ttbar[imtt-1].append(-0.023*ttbar_histo.GetBinContent(imtt))
      # #15% ttbar
      # #sys_diff_ttbar[imtt-1].append(0.15*ttbar_histo.GetBinContent(imtt))
      # #sys_diff_ttbar[imtt-1].append(-0.15*ttbar_histo.GetBinContent(imtt))
      # #2.8% QCD
      # sys_diff_qcd[imtt-1].append(0.028*qcd_histo.GetBinContent(imtt))
      # sys_diff_qcd[imtt-1].append(-0.028*qcd_histo.GetBinContent(imtt))
    #combining uncertainties
    sys_tot_ttbar=[]
    sys_tot_qcd=[]
    sys_tot=[]
    sys_global_ttbar=[0.0,0.0]
    sys_global_qcd=[0.0,0.0]
    nevt_global=[0.0,0.0,0.0]
    for imtt in range(1,ttbar_histo.GetNbinsX()+1):
      uperr_qcd=0
      downerr_qcd=0
      uperr_ttbar=0
      downerr_ttbar=0
      for error in sys_diff_ttbar[imtt-1]:
        if error<0:
          downerr_ttbar=downerr_ttbar+error*error
        else:
          uperr_ttbar=uperr_ttbar+error*error
      for error in sys_diff_qcd[imtt-1]:
        if error<0:
          downerr_qcd=downerr_qcd+error*error
        else:
          uperr_qcd=uperr_qcd+error*error
      sys_tot_ttbar.append([math.sqrt(downerr_ttbar),math.sqrt(uperr_ttbar)])
      sys_tot_qcd.append([math.sqrt(downerr_qcd),math.sqrt(uperr_qcd)])
      sys_tot.append([math.sqrt(downerr_qcd+downerr_ttbar),math.sqrt(uperr_qcd+uperr_ttbar)])
      sys_global_qcd[0]=sys_global_qcd[0]+downerr_qcd
      sys_global_qcd[1]=sys_global_qcd[1]+uperr_qcd
      sys_global_ttbar[0]=sys_global_ttbar[0]+downerr_ttbar
      sys_global_ttbar[1]=sys_global_ttbar[1]+uperr_ttbar
      # nevt_global[0]=nevt_global[0]+data_histo.GetBinContent(imtt)
      nevt_global[1]=nevt_global[1]+qcd_histo.GetBinContent(imtt)
      nevt_global[2]=nevt_global[2]+ttbar_histo.GetBinContent(imtt)
      #print 'ttbar+qcd',math.sqrt(uperr_qcd+uperr_ttbar),math.sqrt(downerr_qcd+downerr_ttbar)
      #print 'qcd',math.sqrt(uperr_qcd),math.sqrt(downerr_qcd)
      #print 'ttbar',math.sqrt(uperr_ttbar),math.sqrt(downerr_ttbar)
      err.SetPointEYhigh(imtt-1,math.sqrt(uperr_qcd+uperr_ttbar))
      err.SetPointEYlow(imtt-1,math.sqrt(downerr_qcd+downerr_ttbar))
    sys_global=[0.0,0.0]
    sys_global[0]=math.sqrt(sys_global_qcd[0]+sys_global_ttbar[0])
    sys_global[1]=math.sqrt(sys_global_qcd[1]+sys_global_ttbar[1])
    sys_global_qcd[0]=math.sqrt(sys_global_qcd[0])
    sys_global_qcd[1]=math.sqrt(sys_global_qcd[1])
    sys_global_ttbar[0]=math.sqrt(sys_global_ttbar[0])
    sys_global_ttbar[1]=math.sqrt(sys_global_ttbar[1])
    # print name
    # print "\hline"
    # print "Multijet QCD & $%.0f^{+%.0f}_{-%.0f}$ \\\\" % (nevt_global[1],sys_global_qcd[1],sys_global_qcd[0])
    # print "SM ttbar & $%.0f^{+%.0f}_{-%.0f}$ \\\\" % (nevt_global[2],sys_global_ttbar[1],sys_global_ttbar[0])
    # print "\hline"
    # print "Total background & $%.0f^{+%.0f}_{-%.0f}$ \\\\" % (nevt_global[1]+nevt_global[2],sys_global[1],sys_global[0])
    # print 'DATA & %.0f' %nevt_global[0]


  err.SetFillStyle(3145)
  err.SetFillColor(kGray+1)

  ###drawing top
  canvas.cd()
  stack.Draw('hist')
  stack.GetXaxis().SetTitle(ttbar_histo.GetXaxis().GetTitle())
  stack.GetYaxis().SetTitle(ttbar_histo.GetYaxis().GetTitle())
  stack.GetXaxis().SetLabelSize(charsize)
  stack.GetXaxis().SetTitleSize(charsize)
  stack.GetYaxis().SetLabelSize(charsize)
  stack.GetYaxis().SetTitleSize(charsize)
  stack.GetYaxis().SetTitleOffset(offset)
  if minx!=0 or maxx!=0:
    stack.GetXaxis().SetRangeUser(minx,maxx)
  #else:
  #  stack.GetXaxis().SetRangeUser(0,4000)
  if miny!=0 or maxy!=0:
    stack.SetMaximum(maxy)
    stack.SetMinimum(miny)
  else:
    if logy:
      stack.SetMaximum(stack.GetMaximum()*10)
      stack.SetMinimum(0.2)
    else:
      stack.SetMaximum(stack.GetMaximum()*2.0)
      stack.SetMinimum(0.001)
  err.Draw('2')
  sum_mc.Draw('samehist')
  if ttbar_file!=0:
    ttbar_line.Draw('samehist')
  for i in signal_histos:
    i.Draw('samehist')
  if logy:
    canvas.SetLogy()
  legend.Draw()

  latex2text=''
  if   'ldy_0b' in name:
    latex2text='#Deltay < 1; 0 b tag'
  elif 'ldy_1b' in name:
    latex2text='#Deltay < 1; 1 b tag'
  elif 'ldy_2b' in name:
    latex2text='#Deltay < 1; 2 b tag'
  elif 'hdy_0b' in name:
    latex2text='#Deltay > 1; 0 b tag'
  elif 'hdy_1b' in name:
    latex2text='#Deltay > 1; 1 b tag'
  elif 'hdy_2b' in name:
    latex2text='#Deltay > 1; 2 b tag'
  latex2=TLatex(0.19,0.7,latex2text)
  latex2.SetTextSize(0.03)
  latex2.SetNDC(1)
  latex2.SetTextFont(42)
  latex2.Draw()

  if docms:
    if '3000' in name:
       CMS_lumi.CMS_lumi(canvas, 3, 11)
    elif '1000' in name:
       CMS_lumi.CMS_lumi(canvas, 2, 11)
    elif '300' in name:
       CMS_lumi.CMS_lumi(canvas, 1, 11)

  ###saving
  canvas.SaveAs('pdf/'+name+'.pdf')
  if outfile!=0:
      canvas.Write()


def compare(name,file_list,name_list,legend_list,normalize=False,drawoption='hE',xtitle='',ytitle='',minx=0,maxx=0,rebin=1,miny=0,maxy=0,textsizefactor=1,logy=False,fit='',fitlow=0,fithigh=0,colors=[]):
  c=TCanvas(name,'',600,600)
  # c.SetLeftMargin(0.15)#
  # c.SetRightMargin(0.05)#
  # # c.SetTopMargin(0.05)#
  # c.SetBottomMargin(0.10)
  # # if not useOutfile:
  # # legend=TLegend(0.7,0.7,0.95,0.95)
  # # else:
  # c.SetTopMargin(0.15)
  # legend=TLegend(0.0,0.85,0.99,0.99)
  # #legend=TLegend(0.35,0.2,0.85,0.5)



  c.SetLeftMargin(0.15)#
  c.SetRightMargin(0.05)#
  c.SetBottomMargin(0.11)
  c.SetTopMargin(0.25)
  legend=TLegend(0.0,0.76,0.99,1.04)


  legend.SetHeader('')
  #legend.SetTextSize(0.03)
  legend.SetBorderSize(0)
  legend.SetTextFont(42)
  legend.SetLineColor(1)
  legend.SetLineStyle(1)
  legend.SetLineWidth(1)
  legend.SetFillColor(0)
  legend.SetFillStyle(0)
  histo_list=[]
  # tfile_list=[]
  the_maxy=0
  widths=[]
  for i in range(len(name_list)):
    # tfile_list.append(TFile(file_list[i],'READ'))
    histo_list.append(file_list[i].Get(name_list[i]).Clone())
    print(legend_list[i],histo_list[-1].Integral())
    if normalize:
      histo_list[-1].Scale(1.0/(histo_list[-1].Integral()+0.00000001))
    if not histo_list[-1].ClassName()=='TGraphAsymmErrors':
      histo_list[-1].SetStats(0)
    histo_list[-1].SetLineWidth(3)
    if colors==[]:
      histo_list[-1].SetLineColor(i+1)
      if i>6:
        histo_list[-1].SetLineColor(i+4)
    else:
      histo_list[-1].SetLineColor(colors[i])
    histo_list[-1].SetTitle('')
    
    if rebin!=1:
      histo_list[-1].Rebin(rebin)
    if not histo_list[-1].ClassName()=='TGraphAsymmErrors':
      the_maxy=max(the_maxy,histo_list[-1].GetBinContent(histo_list[-1].GetMaximumBin())*1.05)
    if fit!='':
      if fitlow==0 and fithigh==0:
        histo_list[-1].Fit(fit)
      else:
        histo_list[-1].Fit(fit,'','',fitlow[i],fithigh[i])
      histo_list[-1].GetFunction("gaus").SetLineColor(i+1)
      gaus=histo_list[-1].GetFunction("gaus")
      print(i,gaus.GetParameter(0),gaus.GetParameter(1),gaus.GetParameter(2))
      widths.append(gaus.GetParameter(2))
    if fit=='':
      legend.AddEntry(histo_list[-1],legend_list[i],'l')
    else:
      legend.AddEntry(histo_list[-1],legend_list[i]+' FWHM='+ "%.2f [GeV]" % (2.354*widths[i]),'l')
  for i in range(len(name_list)):
    if i==0:
      if not histo_list[-1].ClassName()=='TGraphAsymmErrors':
        if miny!=0 or maxy!=0:
          histo_list[i].SetMaximum(maxy)
          histo_list[i].SetMinimum(miny)
        else:
          histo_list[i].SetMaximum(the_maxy)
          histo_list[i].SetMinimum(0.0001)
      else:
        histo_list[i].SetMaximum(1.05)
        histo_list[i].SetMinimum(0.0001)
      histo_list[i].Draw(drawoption)
      charsize=0.05*textsizefactor
      histo_list[i].GetYaxis().SetLabelSize(charsize)
      histo_list[i].GetYaxis().SetTitleSize(charsize)
      histo_list[i].GetYaxis().SetTitleOffset(1.6)
      histo_list[i].GetXaxis().SetLabelSize(charsize)
      histo_list[i].GetXaxis().SetTitleSize(charsize)
      histo_list[i].GetXaxis().SetTitleOffset(0.95)
      # if useOutfile:
      if xtitle!='':
        histo_list[i].GetXaxis().SetTitle(xtitle)
      if ytitle!='':  
        histo_list[i].GetYaxis().SetTitle(ytitle)
      if maxx!=0 or minx!=0:
        histo_list[i].GetXaxis().SetRangeUser(minx,maxx)
      #   histo_list[i].GetYaxis().SetTitle('Efficiency')
    else:
      if histo_list[-1].ClassName()=='TGraphAsymmErrors':
        drawoption= drawoption.replace("A", "")
      histo_list[i].Draw(drawoption+'SAME')
  if logy:
    c.SetLogy()
  legend.Draw()
  # outfile.cd()
  c.Write(name)
  c.SaveAs('pdf/'+name+'.pdf')
  #c.SaveAs(folder+name+'.png')





if __name__ == '__main__':
	
	#select steps
	histo_factory=False
	stacking=True
	theta=False


	if histo_factory:
		p = Pool(len(filenames))
		print(p.map(doplots, range(len(filenames))))

	files=[]
	for sample in range(len(filenames)):
		files.append(ROOT.TFile('plots/outfile_'+filenames[sample]+'.root',"READ"))


	if stacking:
		outfile = ROOT.TFile('plots/outfile.root','RECREATE')
		for lumi in target_lumi:
			for sel in selections:
				for histo in plots:
					rebin=1
					zoom=2
					if 'zp_m' in histo:
						rebin=2
					if 'pre' in sel:
						zoom=200
					make_ratioplot(histo+'_'+sel+'_'+str(lumi)+'_Stack', ttbar_file=files[5], qcd_file=files[6], signal_files=files[:-2], histo=histo+'_'+sel+'_'+str(lumi),rebin=rebin,minx=0,maxx=0,miny=0,maxy=0,logy=False,
						xtitle='',ytitle='',textsizefactor=1,signal_legend=legends[:-2],outfile=outfile,signal_colors=[],
						ttbar_legend='t#bar{t}',qcd_legend='NTMJ',dosys=True,docms=True,legendtitle='',signal_zoom=zoom)
		

		genfiles=['output/genrsg2.root','output/genrsg3.root','output/genrsg4.root','output/genrsg5.root','output/genrsg6.root']
		gennames=['2','3','4','5','6']
		for i in range(len(genfiles)):
			genfile=ROOT.TFile(genfiles[i],'READ')
			outfile.cd()
			genfile.Delphes.Draw('zp_m>>genrsg'+gennames[i])
			genplot=ROOT.gDirectory.Get('genrsg'+gennames[i])
			genplot.Write()

		compare(
		name='genmass',
		colors=intcolor,
		normalize=True,
		rebin=1,

		file_list=[outfile]*5,
		name_list=['genrsg6','genrsg5','genrsg4','genrsg3','genrsg2'],
		legend_list=['6 TeV','5 TeV','4 TeV','3 TeV','2 TeV'],
		drawoption='hist c',
		ytitle='A.U.',
		xtitle='m_{g} gen level [GeV]',
		minx=200,maxx=7000,
		#miny=0.3,maxy=1.1,rebin=1,
		textsizefactor=0.7)

		for sel in selections:
			for var in ['top1_pt','top2_pt']:
				compare(
				name=sel+'mass'+var,
				colors=intcolor,
				normalize=False,
				rebin=10,
				file_list=files[:-2],
				name_list=[var+"_"+sel+"_3000"]*5,
				legend_list=['2 TeV','3 TeV','4 TeV','5 TeV','6 TeV'],
				drawoption='hist c',
				ytitle='A.U.',
				xtitle='reconstructed m_{g} [GeV]',
				minx=600,maxx=7000,
				#miny=0.3,maxy=1.1,rebin=1,
				textsizefactor=0.7)
			for cat in ['0','1','2']:
				compare(
				name=sel+'mass'+cat,
				colors=intcolor,
				normalize=False,
				rebin=10,
				file_list=files[:-2],
				name_list=["zp_m_"+cat+"b_"+sel+"_3000"]*5,
				legend_list=['2 TeV','3 TeV','4 TeV','5 TeV','6 TeV'],
				drawoption='hist c',
				ytitle='A.U.',
				xtitle='reconstructed m_{g} [GeV]',
				minx=600,maxx=7000,
				#miny=0.3,maxy=1.1,rebin=1,
				textsizefactor=0.7)

		outfile.Close()

	if theta:
		for lumi in range(len(target_lumi)):
			template=ROOT.TFile('plots/theta_'+str(target_lumi[lumi])+'.root','RECREATE')
			for sample in range(len(filenames)):
				for cat in range(len(categories)):
					the_plot=files[sample].Get(categories[cat]+'_full_'+str(target_lumi[lumi])).Clone()
					the_plot.Rebin(2)
					the_plot.Write(categories_names[cat]+'__'+filenames[sample])
			template.Close()

	from ROOT import TGraph
	from array import array
	from math import log,exp
	x, y = array( 'd' ), array( 'd' )
	x.append(1000)
	x.append(1250)
	x.append(1500)
	x.append(2000)
	x.append(2500)
	x.append(3000)
	x.append(3500)
	x.append(4000)
	x.append(4500)
	x.append(5000)

	y.append(log(1.3*20.05))
	y.append(log(1.3*7.92))
	y.append(log(1.3*3.519))
	y.append(log(1.3*0.9528))
	y.append(log(1.3*0.3136))
	y.append(log(1.3*0.1289))
	y.append(log(1.3*0.05452))
	y.append(log(1.3*0.02807))
	y.append(log(1.3*0.01603))
	y.append(log(1.3*0.009095))
#0.00960796535494
	gr = TGraph( 10, x, y )
	gr.Fit('pol3')
	func=gr.GetFunction('pol3')
	print(exp(func.Eval(5000)))
	print(exp(func.Eval(6000)))

