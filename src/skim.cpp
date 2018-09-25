/*
 * skim.cpp
 *
 *  Created on: 24 Aug 2016
 *      Author: jkiesele
 */

#include "interface/skim.h"

#include "TRandom3.h"  
TRandom3* r = new TRandom3();
 double getEff_b(double ptin, double etain, const int pu) {

  double pt=0.,eta=0.,ptwidth=0.,etawidth=0.,eff=0.; 
    
   etain = abs(etain);
    if (ptin > 3000.) ptin = 2999.99;

    TFile f("beff_200PU_WPM.root");
     TH1F *heff = (TH1F*)f.Get("heff");
      int x_range=(heff->GetNbinsX());
       int y_range=(heff->GetNbinsY());
           for(int i=1; i < x_range+1; i++){
             for(int j=1; j < y_range+1; j++){
                pt= heff->GetXaxis()->GetBinLowEdge(i);
                 eta= heff->GetYaxis()->GetBinLowEdge(j);
            ptwidth  = heff->GetXaxis()->GetBinWidth(i);
             etawidth = heff->GetYaxis()->GetBinWidth(j);
               if (pt <= ptin && ptin < (pt+ptwidth)){
          if (eta <= etain && etain < (eta+etawidth)){
                     eff=heff->GetBinContent(i,j);
                                }
                                     }
                                               }
                                      }
                                                                                                                                                     return eff; 
                                                                                                                                                        }
 
 bool isBTagged(const double pt, const double eta, const int pu, const int fl) {
  bool isBTagged(0);
 
   if (fl == 5) {
     double eff = getEff_b(pt, eta, pu);  
     double rand = r->Rndm();

   if (eff > rand) isBTagged = 1;
     else isBTagged = 0;
   }
 
 else 
 { 
    double rand = r->Rndm();

  if (0.01 > rand) isBTagged = 1;   // mistag eff = 0.01
     else isBTagged = 0;
  }

  return isBTagged;

 } 


void skim::analyze(size_t childid /* this info can be used for printouts */){

	/*
	 * This skeleton analyser runs directly on the Delphes output.
	 * It can be used to create histograms directly or a skim.
	 * If a skim is created, a new input configuration will be written automatically
	 * and stored in the output directory together with the ntuples.
	 * The skim can contain delphes objects again or can be flat. This is up
	 * to the user.
	 * Examples for both are given here.
	 *
	 * The same skeleton can be used to read the skim. Please refer to the comments
	 * marked with "==SKIM=="
	 *
	 * These parts are commented, since the code is supposed to work as an example without
	 * modifications on Delphes output directly.
	 */



	/*
	 * Define the branches that are to be considered for the analysis
	 * This branch handler (notice the "d")
	 * is used to run directly in Delphes output.
	 * For skimmed ntuples, see below
	 */
//	d_ana::dBranchHandler<Electron> elecs(tree(),"Electron");
	/*
	 * Other branches might be the following
	 * (for a full list, please inspect the Delphes sample root file with root)
	 * For the Delphes class description, see $DELPHES_PATH/classes/DelphesClasses.h
	 */
	//
//	d_ana::dBranchHandler<HepMCEvent>  event(tree(),"Event");
	d_ana::dBranchHandler<GenParticle> genpart(tree(),"Particle");
//	d_ana::dBranchHandler<Jet>         genjet(tree(),"GenJet");
	d_ana::dBranchHandler<Weight>      weights(tree(),"Weight");
	d_ana::dBranchHandler<Jet>         jets(tree(),"JetPUPPIAK8");
//	d_ana::dBranchHandler<Jet>         small_jets(tree(),"JetPUPPI");
//	d_ana::dBranchHandler<Muon>        muontight(tree(),"MuonTight");
//	d_ana::dBranchHandler<Muon>        muonloose(tree(),"MuonLoose");
//	d_ana::dBranchHandler<Photon>      photon(tree(),"Photon");
//	d_ana::dBranchHandler<MissingET>   met(tree(),"MissingET");

	const int pu = 200;
        int sj00BTagged, sj10BTagged, sj01BTagged, sj11BTagged;


	/* ==SKIM==
	 *
	 * If a skim of the Delphes outout was created in a way indicated
	 * further below, use the tBranchHandler (please notive the "t")
	 * to access vectors of objects...
	 *
	 */
	// d_ana::tBranchHandler<std::vector<Electron> > electrons(tree(),"Electrons");

	/*==SKIM==
	 *
	 * Or an object directly
	 *
	 */
	//d_ana::tBranchHandler<MissingET> met(tree(),"MET");



	/*
	 * Always use this function to add a new histogram (can also be 2D)!
	 * Histograms created this way are automatically added to the output file
	 */
	TH1* histo=addPlot(new TH1D("count","count",1,0,1),"count","events");


	/*
	 * If (optionally) a skim or a flat ntuple is to be created, please use the following function to initialize
	 * the tree.
	 * The output files will be written automatically, and a config file will be created.
	 */
	TTree* myskim=addTree();
	/*
	 * Add a simple branch to the skim
	 */
	// Double_t elecPt=0;
	// myskim->Branch("elecPt", &elecPt);
	Double_t top1_pt = 0;
	Double_t top1_eta = 0;
	Double_t top1_phi = 0;
	Double_t top1_sdmass = 0;
	Double_t top1_tau32 = 0;
	Int_t top1_btag;
	Double_t top2_pt = 0;
	Double_t top2_eta = 0;
	Double_t top2_phi = 0;
	Double_t top2_sdmass = 0;
	Double_t top2_tau32 = 0;
	Int_t top2_btag;
	Double_t zp_m = 0;
	Double_t zp_m2 = 0;
	Double_t zp_m3 = 0;
	Double_t zp_dy = 0;
	Double_t zp_eta = 0;
	Double_t zp_phi = 0;
	Double_t zp_pt = 0;
	Double_t zp_btag = 0;
	Double_t zp_m_gen = 0;

//	Double_t weight = 1;

	// Double_t met = 0;
	// Double_t met_eta = 0;
	// Double_t met_phi = 0;

	// Double_t met_t = 0;
	// Double_t met_p = 0;

//	myskim->Branch("weight",&weight);

	myskim->Branch("top1_pt",&top1_pt);
	myskim->Branch("top1_eta",&top1_eta);
	myskim->Branch("top1_phi",&top1_phi);
	myskim->Branch("top1_sdmass",&top1_sdmass);
	myskim->Branch("top1_tau32",&top1_tau32);
	myskim->Branch("top1_btag",&top1_btag);
	myskim->Branch("top2_pt",&top2_pt);
	myskim->Branch("top2_eta",&top2_eta);
	myskim->Branch("top2_phi",&top2_phi);
	myskim->Branch("top2_sdmass",&top2_sdmass);
	myskim->Branch("top2_tau32",&top2_tau32);
	myskim->Branch("top2_btag",&top2_btag);
	myskim->Branch("zp_m",&zp_m);
	myskim->Branch("zp_m2",&zp_m2);
	myskim->Branch("zp_m3",&zp_m3);
	myskim->Branch("zp_dy",&zp_dy);
	myskim->Branch("zp_eta",&zp_eta);
	myskim->Branch("zp_phi",&zp_phi);
	myskim->Branch("zp_pt",&zp_pt);
	myskim->Branch("zp_btag",&zp_btag);
	myskim->Branch("zp_m_gen",&zp_m_gen);

	/*
	 * Or store a vector of objects (also possible to store only one object)
	 */
	// std::vector<Electron> skimmedelecs;
	// myskim->Branch("Electrons",&skimmedelecs);



	size_t nevents=tree()->entries();
	if(isTestMode())
		nevents/=100;
	for(size_t eventno=0;eventno<nevents;eventno++){
		/*
		 * The following two lines report the status and set the event link
		 * Do not remove!
		 */
		reportStatus(eventno,nevents);
		tree()->setEntry(eventno);

		histo->Fill(0.5);

		// /*
		//  * Begin the event-by-event analysis
		//  */
		// for(size_t i=0;i<elecs.size();i++){
		// 	histo->Fill(elecs.at(i)->PT);
		// }

		// /*
		//  * Or to fill the skim
		//  */
		// skimmedelecs.clear();
		// for(size_t i=0;i<elecs.size();i++){
		// 	//flat info
		// 	elecPt=elecs.at(i)->PT;
		// 	if(elecs.at(i)->PT < 20) continue;
		// 	//or objects
		// 	skimmedelecs.push_back(*elecs.at(i));
		// }

		top1_pt = 0;
		top1_eta = 0;
		top1_phi = 0;
		top1_sdmass = 0;
		top1_tau32 = 0;
		top1_btag = 0;
		top2_pt = 0;
		top2_eta = 0;
		top2_phi = 0;
		top2_sdmass = 0;
		top2_tau32 = 0;
		top2_btag = 0;
		zp_m = 0;
		zp_m2 = 0;
		zp_m3 = 0;
		zp_dy = 0;
		zp_eta = 0;
		zp_phi = 0;
		zp_pt = 0;
		zp_btag = 0;

		//weight = 1;
		zp_m_gen = 0;

		//std::cout<<jets.size()<<std::endl;
		// for (int i =0; i<jets.size(); i++)
		// {

		// }
		if (jets.size()<2) continue;
		//ht
   		std::vector<Jet> good_jets;
   		std::vector<int> btags;
		for (unsigned int i = 0; i<jets.size(); i++)
		{
			if(jets.at(i)->PT>400.0 &&
			fabs(jets.at(i)->Eta)<4.0 &&
			jets.at(i)->SoftDroppedJet.M()>105.0 &&
			jets.at(i)->SoftDroppedJet.M()<210.0 &&
			jets.at(i)->Tau[2]/jets.at(i)->Tau[1]<0.65)
			{
				good_jets.push_back(*jets.at(i));
	//			int btag=0;
	//			for (unsigned int j = 0; j<small_jets.size(); j++)
	//			{
	//				if (jets.at(i)->P4().DeltaR(small_jets.at(j)->P4())<0.8 && (small_jets.at(j)->BTag & (1 << 1) ) )
	//				{
	//					btag=1;
	//					break;
	//				}
	//			}
	//			btags.push_back(btag);
	//			//std::cout<<jets.at(i)->Flavor<<" "<<jets.at(i)->BTag<<" "<<btag<<std::endl;
			}
			if (good_jets.size()>1) break;
		}
		if (good_jets.size()<2) continue;

		// if (jets.at(0)->PT<400.0 ||
		// 	jets.at(1)->PT<400.0 ||
		// 	fabs(jets.at(0)->Eta)>4.0 ||
		// 	fabs(jets.at(1)->Eta)>4.0 ||
		// 	jets.at(0)->SoftDroppedJet.M()<50.0 ||
		// 	jets.at(1)->SoftDroppedJet.M()<50.0 
		// 	) continue;

		//weight = weights.at(0)->Weight;
		
		 // subjet Btagging
  	TLorentzVector p4_sj0_ak8jet0(good_jets.at(0).SoftDroppedP4[1]);
           TLorentzVector p4_sj0_ak8jet1(good_jets.at(1).SoftDroppedP4[1]);
          TLorentzVector p4_sj1_ak8jet0(good_jets.at(0).SoftDroppedP4[2]);
           TLorentzVector p4_sj1_ak8jet1(good_jets.at(1).SoftDroppedP4[2]);
		
	sj00BTagged =  int(isBTagged(p4_sj0_ak8jet0.Pt(), p4_sj0_ak8jet0.Eta(), pu, good_jets.at(0).Flavor ));
       sj10BTagged =  int(isBTagged(p4_sj1_ak8jet0.Pt(), p4_sj1_ak8jet0.Eta(), pu, good_jets.at(0).Flavor ));
          sj01BTagged =  int(isBTagged(p4_sj0_ak8jet1.Pt(), p4_sj0_ak8jet1.Eta(), pu, good_jets.at(1).Flavor ));
         sj11BTagged =  int(isBTagged(p4_sj1_ak8jet1.Pt(), p4_sj1_ak8jet1.Eta(), pu, good_jets.at(1).Flavor ));

		
		top1_pt = good_jets.at(0).PT;
		top1_eta = good_jets.at(0).Eta;
		top1_phi = good_jets.at(0).Phi;
		top1_sdmass = good_jets.at(0).SoftDroppedJet.M();
		top1_tau32 = good_jets.at(0).Tau[2]/good_jets.at(0).Tau[1];
	//	top1_btag = btags.at(0);
		 if ( sj00BTagged + sj10BTagged >=1) { top1_btag = 1;}
		top2_pt = good_jets.at(1).PT;
		top2_eta = good_jets.at(1).Eta;
		top2_phi = good_jets.at(1).Phi;
		top2_sdmass = good_jets.at(1).SoftDroppedJet.M();
		top2_tau32 = good_jets.at(1).Tau[2]/good_jets.at(1).Tau[1];
	//	top2_btag = btags.at(1);
		if ( sj01BTagged + sj11BTagged >=1) { top2_btag = 1;}
		TLorentzVector zprime(good_jets.at(0).P4()+good_jets.at(1).P4());
		TLorentzVector zprime2(good_jets.at(0).SoftDroppedJet+good_jets.at(1).SoftDroppedJet);
		TLorentzVector top1_mix;
		TLorentzVector top2_mix;
		top1_mix.SetPtEtaPhiM(good_jets.at(0).PT, good_jets.at(0).Eta, good_jets.at(0).Phi, good_jets.at(0).SoftDroppedJet.M() ) ;
		top2_mix.SetPtEtaPhiM(good_jets.at(1).PT, good_jets.at(1).Eta, good_jets.at(1).Phi, good_jets.at(1).SoftDroppedJet.M() ) ;
		TLorentzVector zprime3(top1_mix+top2_mix);

		zp_m = zprime.M();
		zp_m2 = zprime2.M();
		zp_m3 = zprime3.M();
		zp_dy = fabs(good_jets.at(0).P4().Rapidity()-good_jets.at(1).P4().Rapidity());
		zp_eta = zprime.Eta();
		zp_phi = zprime.Phi();
		zp_pt = zprime.Pt();
		zp_btag = top1_btag+top2_btag;
		// for (auto jet: jets)
		// {



		// }

		for (unsigned int i=0;i<genpart.size();i++)
		{
			if (genpart.at(i)->PID==5100021)
			{
				zp_m_gen= genpart.at(i)->Mass;
				break;
			}
 		}






		myskim->Fill();


		/*==SKIM==
		 * Access the branches of the skim
		 */
		//std::vector<Electron> * skimelecs=electrons.content();
		//for(size_t i=0;i<skimelecs->size();i++){
		//	histo->Fill(skimelecs->at(i).PT);
		//}
	}


	/*
	 * Must be called in the end, takes care of thread-safe writeout and
	 * call-back to the parent process
	 */
	processEndFunction();
}



void skim::postProcess(){
	/*
	 * This function can be used to analyse the output histograms, e.g. extract a signal contribution etc.
	 * The function can also be called directly on an output file with the histograms, if
	 * RunOnOutputOnly = true
	 * is set in the analyser's config file
	 *
	 * This function also represents an example of how the output of the analyser can be
	 * read-back in an external program.
	 * Just include the sampleCollection.h header and follow the procedure below
	 *
	 */

	/*
	 * Here, the input file to the extraction of parameters from the histograms is the output file
	 * of the parallelised analysis.
	 * The sampleCollection class can also be used externally for accessing the output consistently
	 */
	// d_ana::sampleCollection samplecoll;
	// samplecoll.readFromFile(getOutPath());

	// std::vector<TString> alllegends = samplecoll.listAllLegends();

	/*
	 * Example how to process the output.
	 * Usually, one would define the legendname of the histogram to be used here
	 * by hand, e.g. "signal" or "background".
	 * To make this example run in any case, I am using alllegends.at(0), which
	 * could e.g. be the signal legend.
	 *
	 * So in practise, the following would more look like
	 * samplecoll.getHistos("signal");
	 */
	// if(alllegends.size()>0){
	// 	d_ana::histoCollection histos=samplecoll.getHistos(alllegends.at(0));

	// 	/*
	// 	 * here, the histogram created in the analyze() function is selected and evaluated
	// 	 * The histoCollection maintains ownership (you don't need to delete the histogram)
	// 	 */
	// 	const TH1* myplot=histos.getHisto("histoname1");

	// 	std::cout << "(example output): the integral is " << myplot->Integral() <<std::endl;

	// 	/*
	// 	 * If the histogram is subject to changes, please clone it and take ownership
	// 	 */

	// 	TH1* myplot2=histos.cloneHisto("histoname1");

	// 	/*
	// 	 * do something with the histogram
	// 	 */

	// 	delete myplot2;
	// }

	/*
	 * do the extraction here.
	 */



}



