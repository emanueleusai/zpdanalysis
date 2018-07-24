/*
 * metskim.cpp
 *
 *  Created on: 24 Aug 2016
 *      Author: jkiesele
 */

#include "interface/metskim.h"



void metskim::analyze(size_t childid /* this info can be used for printouts */){

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
	// d_ana::dBranchHandler<Electron> elecs(tree(),"Electron");
	/*
	 * Other branches might be the following
	 * (for a full list, please inspect the Delphes sample root file with root)
	 * For the Delphes class description, see $DELPHES_PATH/classes/DelphesClasses.h
	 */
	//
	// d_ana::dBranchHandler<HepMCEvent>  event(tree(),"Event");
	// d_ana::dBranchHandler<GenParticle> genpart(tree(),"Particle");
	// d_ana::dBranchHandler<Jet>         genjet(tree(),"GenJet");
	// d_ana::dBranchHandler<Jet>         jet(tree(),"Jet");
	// d_ana::dBranchHandler<Muon>        muontight(tree(),"MuonTight");
	// d_ana::dBranchHandler<Muon>        muonloose(tree(),"MuonLoose");
	// d_ana::dBranchHandler<Photon>      photon(tree(),"Photon");
	d_ana::dBranchHandler<MissingET>   mets(tree(),"MissingET");
	d_ana::dBranchHandler<MissingET>   puppi_mets(tree(),"PuppiMissingET");
	d_ana::dBranchHandler<MissingET>   gen_mets(tree(),"GenMissingET");
	d_ana::dBranchHandler<MissingET>   genpileup_mets(tree(),"GenPileUpMissingET");

	d_ana::dBranchHandler<ScalarHT>    hts(tree(),"ScalarHT");
	d_ana::dBranchHandler<Vertex>      vertices(tree(),"Vertex");

	d_ana::dBranchHandler<Jet>      jets(tree(),"Jet");
	d_ana::dBranchHandler<Jet>      puppi_jets(tree(),"JetPUPPI");
	d_ana::dBranchHandler<Jet>      gen_jets(tree(),"GenJet");

	d_ana::dBranchHandler<Weight>      weights(tree(),"Weight");


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
	// TH1* histo=addPlot(new TH1D("histoname1","histotitle1",100,0,100),"p_{T} [GeV]","N_{e}");


	/*
	 * If (optionally) a skim or a flat ntuple is to be created, please use the following function to initialize
	 * the tree.
	 * The output files will be written automatically, and a config file will be created.
	 */
	TTree* myskim=addTree();

	TLorentzVector met;
	Double_t met_t = 0;
	Double_t met_p = 0;
	TLorentzVector puppi_met;
	Double_t puppi_met_t = 0;
	Double_t puppi_met_p = 0;
	TLorentzVector gen_met;
	Double_t gen_met_t = 0;
	Double_t gen_met_p = 0;
	TLorentzVector genpileup_met;
	Double_t genpileup_met_t = 0;
	Double_t genpileup_met_p = 0;

	TLorentzVector l1;
	TLorentzVector l2;
	TLorentzVector median;
	TLorentzVector weighted_median;
	TLorentzVector z;

	Double_t npv = 0;
	Double_t njet = 0;
	Double_t npuppijet = 0;
	Double_t ngenjet = 0;
	Double_t ht = 0;
	Double_t rho = 0;

	TLorentzVector jetsum;
	Double_t jetsum_t = 0;
	Double_t jetsum_p = 0;
	TLorentzVector puppi_jetsum;
	Double_t puppi_jetsum_t = 0;
	Double_t puppi_jetsum_p = 0;
	TLorentzVector gen_jetsum;
	Double_t gen_jetsum_t = 0;
	Double_t gen_jetsum_p = 0;

	Double_t weight = 1;


	myskim->Branch("weight",&weight);

	myskim->Branch("met",&met);
	myskim->Branch("met_t",&met_t);
	myskim->Branch("met_p",&met_p);
	myskim->Branch("puppi_met",&puppi_met);
	myskim->Branch("puppi_met_t",&puppi_met_t);
	myskim->Branch("puppi_met_p",&puppi_met_p);
	myskim->Branch("gen_met",&gen_met);
	myskim->Branch("gen_met_t",&gen_met_t);
	myskim->Branch("gen_met_p",&gen_met_p);
	myskim->Branch("genpileup_met",&genpileup_met);
	myskim->Branch("genpileup_met_t",&genpileup_met_t);
	myskim->Branch("genpileup_met_p",&genpileup_met_p);

	myskim->Branch("l1",&l1);
	myskim->Branch("l2",&l2);
	myskim->Branch("median",&median);
	myskim->Branch("weighted_median",&weighted_median);
	myskim->Branch("z",&z);

	myskim->Branch("npv",&npv);
	myskim->Branch("njet",&njet);
	myskim->Branch("npuppijet",&npuppijet);
	myskim->Branch("ngenjet",&ngenjet);
	myskim->Branch("ht",&ht);
	myskim->Branch("rho",&rho);

	myskim->Branch("jetsum",&jetsum);
	myskim->Branch("jetsum_t",&jetsum_t);
	myskim->Branch("jetsum_p",&jetsum_p);
	myskim->Branch("puppi_jetsum",&puppi_jetsum);
	myskim->Branch("puppi_jetsum_t",&puppi_jetsum_t);
	myskim->Branch("puppi_jetsum_p",&puppi_jetsum_p);
	myskim->Branch("gen_jetsum",&gen_jetsum);
	myskim->Branch("gen_jetsum_t",&gen_jetsum_t);
	myskim->Branch("gen_jetsum_p",&gen_jetsum_p);


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

		met.SetXYZT(0,0,0,0);
		met_t = 0;
		met_p = 0;
		puppi_met.SetXYZT(0,0,0,0);
		puppi_met_t = 0;
		puppi_met_p = 0;
		gen_met.SetXYZT(0,0,0,0);
		gen_met_t = 0;
		gen_met_p = 0;
		genpileup_met.SetXYZT(0,0,0,0);
		genpileup_met_t = 0;
		genpileup_met_p = 0;
		l1.SetXYZT(0,0,0,0);
		l2.SetXYZT(0,0,0,0);
		median.SetXYZT(0,0,0,0);
		weighted_median.SetXYZT(0,0,0,0);
		z.SetXYZT(0,0,0,0);
		npv = 0;
		njet = 0;
		npuppijet = 0;
		ngenjet = 0;
		ht = 0;
		rho = 0;
		jetsum.SetXYZT(0,0,0,0);
		jetsum_t = 0;
		jetsum_p = 0;
		puppi_jetsum.SetXYZT(0,0,0,0);
		puppi_jetsum_t = 0;
		puppi_jetsum_p = 0;
		gen_jetsum.SetXYZT(0,0,0,0);
		gen_jetsum_t = 0;
		gen_jetsum_p = 0;

		/*
		 * Begin the event-by-event analysis
		 */
		// for(size_t i=0;i<elecs.size();i++){
		// 	histo->Fill(elecs.at(i)->PT);
		// }

		/*
		 * Or to fill the skim
		 */
		// skimmedelecs.clear();
		// for(size_t i=0;i<elecs.size();i++){
		// 	//flat info
		// 	elecPt=elecs.at(i)->PT;
		// 	if(elecs.at(i)->PT < 20) continue;
		// 	//or objects
		// 	skimmedelecs.push_back(*elecs.at(i));
		// }

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



void metskim::postProcess(){
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
		// d_ana::histoCollection histos=samplecoll.getHistos(alllegends.at(0));

		/*
		 * here, the histogram created in the analyze() function is selected and evaluated
		 * The histoCollection maintains ownership (you don't need to delete the histogram)
		 */
		// const TH1* myplot=histos.getHisto("histoname1");

		// std::cout << "(example output): the integral is " << myplot->Integral() <<std::endl;

		/*
		 * If the histogram is subject to changes, please clone it and take ownership
		 */

		// TH1* myplot2=histos.cloneHisto("histoname1");

		/*
		 * do something with the histogram
		 */

		// delete myplot2;
	

	/*
	 * do the extraction here.
	 */



}



