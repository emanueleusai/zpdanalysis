from __future__ import print_function
from multiprocessing import Pool
import sys
import ROOT
from ROOT import TFile,TCanvas,gROOT,gStyle,TLegend,TGraphAsymmErrors,THStack,TIter,kRed,kYellow,kGray,kBlack,TLatex,kOrange,kAzure,TLine,kWhite,kBlue,kTRUE,kFALSE,TColor
import CMS_lumi
import math
import sys
from os import system

ROOT.gROOT.SetBatch()

hexcolor=["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2", "#7f7f7f", "#bcbd22", "#17becf"]
intcolor=[TColor.GetColor(i) for i in hexcolor]


folder='/eos/uscms/store/user/eusai/metstudies/'

delphes_files=['drellyan0','drellyan1','drellyan2','drellyan3']

fullsim_files=['drellyan0_fullsim','drellyan1_fullsim','drellyan2_fullsim','drellyan3_fullsim']

filenames = delphes_files+fullsim_files

maxevts =[2188734,2121821,692639,712575]

class histos:
	def __init__(self, selection, sample, outfile):
		outfile.cd()
		self.sample=sample
		self.histolist=[]

		self.weight = ROOT.TH1F("weight_"+selection,";Weight ;A.U.",5000 ,0 ,5 )
		self.weight.Sumw2()
		self.histolist.append('weight')

		setup_met_study(self,'met','p_{T}^{miss}')
		setup_met_study(self,'puppi_met','PUPPI p_{T}^{miss}')
		setup_met_study(self,'gen_met','gen p_{T}^{miss}')

		setup_met_study(self,'jetsum','#SigmaJet p_{T}')
		setup_met_study(self,'puppi_jetsum','PUPPI #SigmaJet p_{T}')
		setup_met_study(self,'gen_jetsum','gen #SigmaJet p_{T}')

		if 'fullsim' in self.sample:
			setup_met_study(self,'genpileup_met','noHF p_{T}^{miss}')
			setup_met_study(self,'pfsum','p_{T} of #SigmaPFCand')

			self.puppi_ht = ROOT.TH1F("puppi_ht_"+selection,";PUPPI HT ;A.U.",1000 ,0 ,1000)
			self.puppi_ht.Sumw2()
			self.histolist.append('puppi_ht')

			self.gen_ht = ROOT.TH1F("gen_ht_"+selection,";gen HT ;A.U.",1000 ,0 ,1000)
			self.gen_ht.Sumw2()
			self.histolist.append('gen_ht')
			
		else:
			setup_met_study(self,'genpileup_met','gen pileup p_{T}^{miss}')

		self.l1 = ROOT.TH1F("l1_"+selection,";leading lepton p_{T} ;A.U.",1000 ,0 ,1000)
		self.l1.Sumw2()
		self.histolist.append('l1')

		self.l2 = ROOT.TH1F("l2_"+selection,";subleading lepton p_{T} ;A.U.",1000 ,0 ,1000)
		self.l2.Sumw2()
		self.histolist.append('l2')

		self.median = ROOT.TH1F("median_"+selection,";Z p_{T} ;A.U.",1000 ,0 ,1000)
		self.median.Sumw2()
		self.histolist.append('median')

		self.l1_eta = ROOT.TH1F("l1_eta_"+selection,";leading lepton #eta ;A.U.",1000 ,0 ,1000)
		self.l1_eta.Sumw2()
		self.histolist.append('l1_eta')

		self.l2_eta = ROOT.TH1F("l2_eta_"+selection,";subleading lepton #eta ;A.U.",1000 ,0 ,1000)
		self.l2_eta.Sumw2()
		self.histolist.append('l2_eta')

		self.median_eta = ROOT.TH1F("median_eta_"+selection,";Z #eta ;A.U.",1000 ,0 ,1000)
		self.median_eta.Sumw2()
		self.histolist.append('median_eta')

		self.npv = ROOT.TH1F("npv_"+selection,";N_{PV} ;A.U.",300 ,0 ,300 )
		self.npv.Sumw2()
		self.histolist.append('npv')

		self.njet = ROOT.TH1F("njet_"+selection,";N_{jets} ;A.U.",100 ,0 ,100 )
		self.njet.Sumw2()
		self.histolist.append('njet')

		self.npuppijet = ROOT.TH1F("npuppijet_"+selection,";N_{PUPPI jets} ;A.U.",100 ,0 ,100 )
		self.npuppijet.Sumw2()
		self.histolist.append('npuppijet')

		self.ngenjet = ROOT.TH1F("ngenjet_"+selection,";N_{gen jets} ;A.U.",100 ,0 ,100 )
		self.ngenjet.Sumw2()
		self.histolist.append('ngenjet')

		self.ht = ROOT.TH1F("ht_"+selection,";HT ;A.U.",1000 ,0 ,1000)
		self.ht.Sumw2()
		self.histolist.append('ht')

		self.rho = ROOT.TH1F("rho_"+selection,";#rho ;A.U.",1000 ,0 ,100 )
		self.rho.Sumw2()
		self.histolist.append('rho')

		for i in self.histolist:
			getattr(self,i).Sumw2()



	def setup_met_study(self,name,title):
		setattr(self,name,ROOT.TH1F(name+"_"+selection,";"+title+" ;A.U.",1000 ,0 ,1000))
		setattr(self,name+"_t",ROOT.TH1F(name+"_t_"+selection,";transverse "+title+" ;A.U.",1000 ,0 ,1000))
		setattr(self,name+"_p",ROOT.TH1F(name+"_p_"+selection,";parallel "+title+" ;A.U.",1000 ,0 ,1000))
		setattr(self,name+"_t2",ROOT.TH1F(name+"_t2_"+selection,";transverse "+title+" ;A.U.",1000 ,0 ,1000))
		setattr(self,name+"_p2",ROOT.TH1F(name+"_p2_"+selection,";parallel "+title+" ;A.U.",1000 ,0 ,1000))

		setattr(self,name+"_vsgenmet",ROOT.TProfile(name+"_vsgenmet_"+selection,"; gen p_{T}^{miss};"+title,1000 ,0 ,1000))
		setattr(self,name+"_vsnpv",ROOT.TProfile(name+"_vsnpv_"+selection,"; N_{PV};"+title,1000 ,0 ,300))
		setattr(self,name+"_vsnjet",ROOT.TProfile(name+"_vsnjet_"+selection,"; N_{jets};"+title,1000 ,0 ,50))
		setattr(self,name+"_vspt",ROOT.TProfile(name+"_vspt_"+selection,"; p_{T}^{Z};"+title,1000 ,0 ,1000))
		setattr(self,name+"_vseta",ROOT.TProfile(name+"_vseta_"+selection,"; #eta_{Z};"+title,1000 ,-5 ,5))
		setattr(self,name+"_t2_vsgenmet",ROOT.TProfile(name+"_t2_vsgenmet_"+selection,"; gen p_{T}^{miss};transverse "+title,1000 ,0 ,1000))
		setattr(self,name+"_t2_vsnpv",ROOT.TProfile(name+"_t2_vsnpv_"+selection,"; N_{PV};transverse "+title,1000 ,0 ,300))
		setattr(self,name+"_t2_vsnjet",ROOT.TProfile(name+"_t2_vsnjet_"+selection,"; N_{jets};transverse "+title,1000 ,0 ,50))
		setattr(self,name+"_t2_vspt",ROOT.TProfile(name+"_t2_vspt_"+selection,"; p_{T}^{Z};transverse "+title,1000 ,0 ,1000))
		setattr(self,name+"_t2_vseta",ROOT.TProfile(name+"_t2_vseta_"+selection,"; #eta_{Z};transverse "+title,1000 ,-5 ,5))
		setattr(self,name+"_p2_vsgenmet",ROOT.TProfile(name+"_p2_vsgenmet_"+selection,"; gen p_{T}^{miss};parallel "+title,1000 ,0 ,1000))
		setattr(self,name+"_p2_vsnpv",ROOT.TProfile(name+"_p2_vsnpv_"+selection,"; N_{PV};parallel "+title,1000 ,0 ,300))
		setattr(self,name+"_p2_vsnjet",ROOT.TProfile(name+"_p2_vsnjet_"+selection,"; N_{jets};parallel "+title,1000 ,0 ,50))
		setattr(self,name+"_p2_vspt",ROOT.TProfile(name+"_p2_vspt_"+selection,"; p_{T}^{Z};parallel "+title,1000 ,0 ,1000))
		setattr(self,name+"_p2_vseta",ROOT.TProfile(name+"_p2_vseta_"+selection,"; #eta_{Z};parallel "+title,1000 ,-5 ,5))

		setattr(self,name+"_res_vsgenmet",ROOT.TProfile(name+"_res_vsgenmet_"+selection,"; gen p_{T}^{miss};"+title+" response",1000 ,0 ,1000))
		setattr(self,name+"_res_vsnpv",ROOT.TProfile(name+"_res_vsnpv_"+selection,"; N_{PV};"+title+" response",1000 ,0 ,300))
		setattr(self,name+"_res_vsnjet",ROOT.TProfile(name+"_res_vsnjet_"+selection,"; N_{jets};"+title+" response",1000 ,0 ,50))
		setattr(self,name+"_res_vspt",ROOT.TProfile(name+"_res_vspt_"+selection,"; p_{T}^{Z};"+title+" response",1000 ,0 ,1000))
		setattr(self,name+"_res_vseta",ROOT.TProfile(name+"_res_vseta_"+selection,"; #eta_{Z};"+title+" response",1000 ,-5 ,5))
		setattr(self,name+"_t2_res_vsgenmet",ROOT.TProfile(name+"_t2_res_vsgenmet_"+selection,"; gen p_{T}^{miss};transverse "+title+" response",1000 ,0 ,1000))
		setattr(self,name+"_t2_res_vsnpv",ROOT.TProfile(name+"_t2_res_vsnpv_"+selection,"; N_{PV};transverse "+title+" response",1000 ,0 ,300))
		setattr(self,name+"_t2_res_vsnjet",ROOT.TProfile(name+"_t2_res_vsnjet_"+selection,"; N_{jets};transverse "+title+" response",1000 ,0 ,50))
		setattr(self,name+"_t2_res_vspt",ROOT.TProfile(name+"_t2_res_vspt_"+selection,"; p_{T}^{Z};transverse "+title+" response",1000 ,0 ,1000))
		setattr(self,name+"_t2_res_vseta",ROOT.TProfile(name+"_t2_res_vseta_"+selection,"; #eta_{Z};transverse "+title+" response",1000 ,-5 ,5))
		setattr(self,name+"_p2_res_vsgenmet",ROOT.TProfile(name+"_p2_res_vsgenmet_"+selection,"; gen p_{T}^{miss};parallel "+title+" response",1000 ,0 ,1000))
		setattr(self,name+"_p2_res_vsnpv",ROOT.TProfile(name+"_p2_res_vsnpv_"+selection,"; N_{PV};parallel "+title+" response",1000 ,0 ,300))
		setattr(self,name+"_p2_res_vsnjet",ROOT.TProfile(name+"_p2_res_vsnjet_"+selection,"; N_{jets};parallel "+title+" response",1000 ,0 ,50))
		setattr(self,name+"_p2_res_vspt",ROOT.TProfile(name+"_p2_res_vspt_"+selection,"; p_{T}^{Z};parallel "+title+" response",1000 ,0 ,1000))
		setattr(self,name+"_p2_res_vseta",ROOT.TProfile(name+"_p2_res_vseta_"+selection,"; #eta_{Z};parallel "+title+" response",1000 ,-5 ,5))

	def fill_met_study(self,event,name):
		getattr(self,name).Fill(getattr(event,name).Pt(),weight)
		getattr(self,name+"_t").Fill(getattr(event,name+"_t"),weight)
		getattr(self,name+"_p").Fill(getattr(event,name+"_p"),weight)
		median_t=median
		median_t.SetZ(0)
		parallel=median_t.Vect().Unit()
		transverse=median_t.Vect().Orthogonal()
		t2 = transverse.Dot(getattr(event,name).Vect());
		p2 = parallel.Dot(getattr(event,name).Vect());
		getattr(self,name+"_t2").Fill(t2,weight)
		getattr(self,name+"_p2").Fill(p2,weight)

		getattr(self,name+"_vsgenmet").Fill(event.gen_met.Pt(),getattr(event,name).Pt(),weight)
		getattr(self,name+"_vsnpv").Fill(event.npv,getattr(event,name).Pt(),weight)
		getattr(self,name+"_vsnjet").Fill(event.njet,getattr(event,name).Pt(),weight)
		getattr(self,name+"_vspt").Fill(event.median.Pt(),getattr(event,name).Pt(),weight)
		getattr(self,name+"_vseta").Fill(event.median.Eta(),getattr(event,name).Pt(),weight)

		# getattr(self,name+"_t2_vsgenmet").Fill(,weight)
		# getattr(self,name+"_t2_vsnpv").Fill(,weight)
		# getattr(self,name+"_t2_vsnjet").Fill(,weight)
		# getattr(self,name+"_t2_vspt").Fill(,weight)
		# getattr(self,name+"_t2_vseta").Fill(,weight)

		# getattr(self,name+"_p2_vsgenmet").Fill(,weight)
		# getattr(self,name+"_p2_vsnpv").Fill(,weight)
		# getattr(self,name+"_p2_vsnjet").Fill(,weight)
		# getattr(self,name+"_p2_vspt").Fill(,weight)
		# getattr(self,name+"_p2_vseta").Fill(,weight)

		getattr(self,name+"_res_vsgenmet").Fill(,weight)
		getattr(self,name+"_res_vsnpv").Fill(,weight)
		getattr(self,name+"_res_vsnjet").Fill(,weight)
		getattr(self,name+"_res_vspt").Fill(,weight)
		getattr(self,name+"_res_vseta").Fill(,weight)
		# getattr(self,name+"_t2_res_vsgenmet").Fill(,weight)
		# getattr(self,name+"_t2_res_vsnpv").Fill(,weight)
		# getattr(self,name+"_t2_res_vsnjet").Fill(,weight)
		# getattr(self,name+"_t2_res_vspt").Fill(,weight)
		# getattr(self,name+"_t2_res_vseta").Fill(,weight)
		# getattr(self,name+"_p2_res_vsgenmet").Fill(,weight)
		# getattr(self,name+"_p2_res_vsnpv").Fill(,weight)
		# getattr(self,name+"_p2_res_vsnjet").Fill(,weight)
		# getattr(self,name+"_p2_res_vspt").Fill(,weight)
		# getattr(self,name+"_p2_res_vseta").Fill(,weight)


	def save(self):
		for i in self.histolist:
			getattr(self,i).Write(getattr(self,i).GetName())


	def print(self):
		for i in self.histolist:
			getattr(self,i).SaveAs('plots/'+getattr(self,i).GetName()+'.pdf')


	def fill(self, event):
		weight=event.weight
		# if hasweight[self.sample]:
		# 	weight = self.sample_weight*event.weight



		self.weight.Fill(event.weight,weight)

		fill_met_study(self,event,'met')
		fill_met_study(self,event,'puppi_met')
		fill_met_study(self,event,'gen_met')
		fill_met_study(self,event,'genpileup_met')
		fill_met_study(self,event,'jetsum')
		fill_met_study(self,event,'puppi_jetsum')
		fill_met_study(self,event,'gen_jetsum')

		if 'fullsim' in self.sample:
			self.puppi_ht.Fill(event.puppi_ht,weight)
			self.gen_ht.Fill(event.gen_ht,weight)
			fill_met_study(self,event,'pfsum')

		self.l1.Fill(event.l1.Pt(),weight)
		self.l2.Fill(event.l2.Pt(),weight)
		self.median.Fill(event.median.Pt(),weight)
		self.l1_eta.Fill(event.l1.Eta(),weight)
		self.l2_eta.Fill(event.l2.Eta(),weight)
		self.median_eta.Fill(event.median.Eta(),weight)
		self.npv.Fill(event.npv,weight)
		self.njet.Fill(event.njet,weight)
		self.npuppijet.Fill(event.npuppijet,weight)
		self.ngenjet.Fill(event.ngenjet,weight)
		self.ht.Fill(event.ht,weight)
		self.rho.Fill(event.rho,weight)

def doplots(sample):
	out = ROOT.TFile('plots/outfile_'+filenames[sample]+'.root','RECREATE')
	f = ROOT.TFile.Open(folder+filenames[sample]+'.root')

	# hist_dict={}
	# for i in selections:
	# 	hist_dict[i]={}
	# 	for j in target_lumi:
	hist_dict=histos('',filenames[sample],out)
	cnt=0
	tree=0
	if 'fullsim' in filenames[sample]:
		tree=f.s
	else:
		tree=f.Delphes
	lng=tree.GetEntries()
	maxentry=maxevts[int(filenames[sample][8])]
	#print(maxentry)
	for event in tree :
		cnt=cnt+1
		if cnt%100==0:
			print(filenames[sample]+': '+"{:.2f}".format(cnt*100.0/lng)+'%'+' '*10,end='\r')
			sys.stdout.flush()
		#fill preselection
		hist_dict.fill(event)
		if cnt==maxentry:
			break

	hist_dict.save()
	f.Close()
	out.Close()



def compare(name,file_list,name_list,legend_list,normalize=False,drawoption='hE',xtitle='',ytitle='',minx=0,maxx=0,rebin=1,miny=0,maxy=0,textsizefactor=1,logy=False,fit='',fitlow=0,fithigh=0,colors=[]):
  c=TCanvas(name,'',600,600)
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
    histo_list.append(file_list[i].Get(name_list[i]).Clone(name_list[i]+'_'+str(i)))
    #print(histo_list)
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
  #c.Write(name)
  c.SaveAs('pdf/'+name+'.pdf')
  #c.SaveAs(folder+name+'.png')

def hadd(path_base,inputlist,outputname,force=True,merge=True):
  command_list='hadd -f '+path_base+outputname+'.root'#-v 0
  if not force:
    command_list='hadd '+path_base+outputname+'.root'#-v 0
  for i in inputlist:
    command_list+=' '+path_base+i+'.root'
  if merge:
    system(command_list)
  return path_base+outputname+'.root'

if __name__ == '__main__':
	 
	#select steps
	histo_factory=False
	plotting=True

	for sample in range(len(filenames)):
		f = ROOT.TFile.Open(folder+filenames[sample]+'.root')
		if 'fullsim' in filenames[sample]:
			lng=f.s.GetEntries()
			print(filenames[sample],lng)
		else:
			lng=f.Delphes.GetEntries()
			print(filenames[sample],lng)
		f.Close()


	if histo_factory:
		p = Pool(len(filenames))
		p.map(doplots, range(len(filenames)))
	#doplots(0)

	de=hadd('plots/',['outfile_drellyan0','outfile_drellyan1','outfile_drellyan2','outfile_drellyan3'],'dy_delphes')
	fs=hadd('plots/',['outfile_drellyan0_fullsim','outfile_drellyan1_fullsim','outfile_drellyan2_fullsim','outfile_drellyan3_fullsim'],'dy_fullsim')

	files=[ROOT.TFile(de,"READ"),ROOT.TFile(fs,"READ")]

	histnames=[
		'met',
		'met_t',
		'met_p',
		'puppi_met',
		'puppi_met_t',
		'puppi_met_p',
		'gen_met',
		'gen_met_t',
		'gen_met_p',

		'l1',
		'l2',
		'median',
		'l1_eta',
		'l2_eta',
		'median_eta',

		'npv',
		'njet',
		'npuppijet',
		'ngenjet',
		'ht',
		'rho',

		'jetsum',
		'jetsum_t',
		'jetsum_p',
		'puppi_jetsum',
		'puppi_jetsum_t',
		'puppi_jetsum_p',
		'gen_jetsum',
		'gen_jetsum_t',
		'gen_jetsum_p'
		]


	histnames2=[
		'puppi_ht',
		'gen_ht',
		'pfsum',
		'pfsum_t',
		'pfsum_p',
	]

	histnames3=[
			'genpileup_met',
		'genpileup_met_t',
		'genpileup_met_p'
	]

	if plotting:
		for i in histnames:
			compare(
		name=i+'_comp',
		colors=intcolor,
		normalize=True,
		rebin=10,

		file_list=files,
		name_list=[i+'_']*2,
		legend_list=['Delphes','Full Sim'],
		#drawoption='hist c',
		# ytitle='A.U.',
		# xtitle='m_{g} gen level [GeV]',
		# minx=200,maxx=7000,
		#miny=0.3,maxy=1.1,rebin=1,
		textsizefactor=0.7)

