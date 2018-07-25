import ROOT
from ROOT import TGraph
from array import array
import CMS_lumi
from operator import itemgetter
ROOT.gROOT.SetBatch()

x_th, y_th = array( 'd' ), array( 'd' )
x_th.append(1.000)
x_th.append(1.250)
x_th.append(1.500)
x_th.append(2.000)
x_th.append(2.500)
x_th.append(3.000)
x_th.append(3.500)
x_th.append(4.000)
x_th.append(4.500)
x_th.append(5.000)
x_th.append(6.000)

y_th.append(1.3*20.05)
y_th.append(1.3*7.92)
y_th.append(1.3*3.519)
y_th.append(1.3*0.9528)
y_th.append(1.3*0.3136)
y_th.append(1.3*0.1289)
y_th.append(1.3*0.05452)
y_th.append(1.3*0.02807)
y_th.append(1.3*0.01603)
y_th.append(1.3*0.009095)
y_th.append(0.00960796535494)

x=array('d',[2.000,3.000,4.000,5.000,6.000])

theory = TGraph( 11, x_th, y_th )
theory.SetLineWidth(3)
theory.SetLineColor(ROOT.kAzure)
theory.SetMarkerColor(ROOT.kAzure)

for lumi in ['300','1000','3000']:
	c=ROOT.TCanvas('unodlimit_'+lumi,'',1200,1000)
	c.SetLogy()
	margine=0.15
	c.SetRightMargin(0.10)
	c.SetLeftMargin(margine)
	c.SetTopMargin(0.10)
	c.SetBottomMargin(margine)
	theta_exp_result = open('plots/theta_'+lumi+'.txt','r')
	theta_exp_lines=theta_exp_result.readlines()
	lines_exp=[filter(None, i.split(' ')) for i in theta_exp_lines[1:] ]
	y_exp=array('d',[float(lines_exp[i][1]) for i in range(len(lines_exp))])
	y_err2down=array('d',[float(lines_exp[i][1])-float(lines_exp[i][2]) for i in range(len(lines_exp))])
	y_err1down=array('d',[float(lines_exp[i][1])-float(lines_exp[i][4]) for i in range(len(lines_exp))])
	y_err1up=array('d',[float(lines_exp[i][5])-float(lines_exp[i][1]) for i in range(len(lines_exp))])
	y_err2up=array('d',[float(lines_exp[i][3])-float(lines_exp[i][1]) for i in range(len(lines_exp))])
	zeros=array('d',[0]*len(lines_exp))

	exp1sigma=ROOT.TGraphAsymmErrors(5,x,y_exp,zeros,zeros,y_err1down,y_err1up)
	exp2sigma=ROOT.TGraphAsymmErrors(5,x,y_exp,zeros,zeros,y_err2down,y_err2up)
	explim=TGraph(5,x,y_exp)
	explim.SetLineWidth(2)
	explim.SetLineStyle(2)
	explim.SetTitle('')
	exp2sigma.SetTitle('')
	exp1sigma.SetTitle('')
	exp1sigma.SetFillColor(ROOT.kGreen+1)
	exp2sigma.SetFillColor(ROOT.kOrange)
	exp2sigma.SetMaximum(10000)

	exp2sigma.SetMinimum(0.0007)
	exp2sigma.Draw('a3lp')
	exp2sigma.GetXaxis().SetTitle("g_{KK} mass [TeV]")
	exp2sigma.GetXaxis().SetRangeUser(1500,6500)
	exp2sigma.GetYaxis().SetTitle("Upper cross section limit [pb]")

	sizefactor=1.5
	exp2sigma.GetXaxis().SetTitleSize(sizefactor*exp2sigma.GetXaxis().GetTitleSize())
	exp2sigma.GetYaxis().SetTitleSize(sizefactor*exp2sigma.GetYaxis().GetTitleSize())
	exp2sigma.GetXaxis().SetLabelSize(sizefactor*exp2sigma.GetXaxis().GetLabelSize())
	exp2sigma.GetYaxis().SetLabelSize(sizefactor*exp2sigma.GetYaxis().GetLabelSize())
	#exp2sigma.GetYaxis().SetMoreLogLabels(1)
	offset=1.2
	exp2sigma.GetXaxis().SetTitleOffset(offset*exp2sigma.GetXaxis().GetTitleOffset())
	exp2sigma.GetYaxis().SetTitleOffset(offset*exp2sigma.GetYaxis().GetTitleOffset())

	exp1sigma.Draw('3')
	explim.Draw('lp')
	theory.Draw('l')

	legend=ROOT.TLegend(0.335,0.55,0.9,0.9)
 	legend.SetTextSize(0.030)
  	legend.SetBorderSize(0)
  	legend.SetTextFont(42)
  	legend.SetLineColor(1)
  	legend.SetLineStyle(1)
  	legend.SetLineWidth(1)
  	legend.SetFillColor(0)
  	legend.SetFillStyle(0)
  	legend.SetHeader('g_{KK}#rightarrow t#bar{t}')
  	legend.AddEntry(explim,'Expected','l')
  	legend.AddEntry(exp1sigma,'#pm 1 std. deviation','f')
  	legend.AddEntry(exp2sigma,'#pm 2 std. deviation','f')
  	legend.AddEntry(theory,"g_{KK}#rightarrow t#bar{t}",'l')
  	legend.Draw()
  	if '3000' in lumi:
		CMS_lumi.CMS_lumi(c, 3, 11)
	elif '1000' in lumi:
		CMS_lumi.CMS_lumi(c, 2, 11)
	elif '300' in lumi:
		CMS_lumi.CMS_lumi(c, 1, 11)
	c.SaveAs('pdf/unodlimit_'+lumi+'.pdf')

	c2=ROOT.TCanvas('sigma_'+lumi,'',1200,1000)
	c2.SetLogy()
	c2.SetRightMargin(0.10)
	c2.SetLeftMargin(margine)
	c2.SetTopMargin(0.10)
	c2.SetBottomMargin(margine)
	sigma3_file = open('plots/theta_'+lumi+'_3sigmaSignif.txt','r')
	sigma5_file = open('plots/theta_'+lumi+'_5sigmaSignif.txt','r')
	sigma3_lines=sigma3_file.readlines()
	sigma5_lines=sigma5_file.readlines()
	sigma3_list=[[float(j) for j in filter(None, i.split(' '))] for i in sigma3_lines[1:] ]
	sigma5_list=[[float(j) for j in filter(None, i.split(' '))] for i in sigma5_lines[1:] ]
	sigma3_list=sorted(sigma3_list, key=itemgetter(0))
	sigma5_list=sorted(sigma5_list, key=itemgetter(0))
	y_sigma3=array('d',[sigma3_list[i][1] for i in range(len(sigma3_list))])
	y_sigma5=array('d',[sigma5_list[i][1] for i in range(len(sigma5_list))])
	sigma3=TGraph(5,x,y_sigma3)
	sigma5=TGraph(5,x,y_sigma5)

	sigma3.SetLineWidth(3)
	#sigma3.SetLineStyle(2)
	sigma3.SetTitle('')
	sigma3.SetLineColor(ROOT.kGreen+1)
	sigma5.SetLineWidth(3)
	#sigma5.SetLineStyle(2)
	sigma5.SetTitle('')
	sigma5.SetLineColor(ROOT.kRed+1)
	sigma3.SetMaximum(10000)
	sigma3.SetMinimum(0.0007)
	sigma3.Draw('al')
	sigma3.GetXaxis().SetTitle("g_{KK} mass [TeV]")
	sigma3.GetXaxis().SetRangeUser(1500,6500)
	sigma3.GetYaxis().SetTitle("Cross section [pb]")

	sigma3.GetXaxis().SetTitleSize(sizefactor*sigma3.GetXaxis().GetTitleSize())
	sigma3.GetYaxis().SetTitleSize(sizefactor*sigma3.GetYaxis().GetTitleSize())
	sigma3.GetXaxis().SetLabelSize(sizefactor*sigma3.GetXaxis().GetLabelSize())
	sigma3.GetYaxis().SetLabelSize(sizefactor*sigma3.GetYaxis().GetLabelSize())
	sigma3.GetXaxis().SetTitleOffset(offset*sigma3.GetXaxis().GetTitleOffset())
	sigma3.GetYaxis().SetTitleOffset(offset*sigma3.GetYaxis().GetTitleOffset())

	sigma5.Draw('l')
	theory.Draw('l')

	legend2=ROOT.TLegend(0.335,0.55,0.9,0.9)
 	legend2.SetTextSize(0.030)
  	legend2.SetBorderSize(0)
  	legend2.SetTextFont(42)
  	legend2.SetLineColor(1)
  	legend2.SetLineStyle(1)
  	legend2.SetLineWidth(1)
  	legend2.SetFillColor(0)
  	legend2.SetFillStyle(0)
  	legend2.SetHeader('g_{KK}#rightarrow t#bar{t}')
  	legend2.AddEntry(sigma3,'3#sigma significance','l')
  	legend2.AddEntry(sigma5,'5#sigma significance','l')
  	legend2.AddEntry(theory,"g_{KK}#rightarrow t#bar{t}",'l')
  	legend2.Draw()
  	if '3000' in lumi:
		CMS_lumi.CMS_lumi(c2, 3, 11)
	elif '1000' in lumi:
		CMS_lumi.CMS_lumi(c2, 2, 11)
	elif '300' in lumi:
		CMS_lumi.CMS_lumi(c2, 1, 11)
	c2.SaveAs('pdf/sigma_'+lumi+'.pdf')

