/*
 * DAnalysis.cpp
 *
 *  Created on: 24 Aug 2016
 *      Author: jkiesele
 */

#include "interface/DAnalysis.h"

const double MTOP  = 172.5;
const double MW    = 80.4; 

void DAnalysis::analyze(size_t childid /* this info can be used for printouts */){

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
	d_ana::dBranchHandler<Electron> elecs(tree(),"Electron"); //Medium electron
	/*
	 * Other branches might be the following
	 * (for a full list, please inspect the Delphes sample root file with root)
	 * For the Delphes class description, see $DELPHES_PATH/classes/DelphesClasses.h
	 */
	//
	d_ana::dBranchHandler<HepMCEvent>  event(tree(),"Event");
	d_ana::dBranchHandler<GenParticle> genpart(tree(),"Particle");
	d_ana::dBranchHandler<Jet>         genjet(tree(),"GenJet");
	d_ana::dBranchHandler<Jet>         jet(tree(),"Jet");
	d_ana::dBranchHandler<Muon>        muontight(tree(),"MuonTight");
	//d_ana::dBranchHandler<Photon>      photon(tree(),"Photon");
	d_ana::dBranchHandler<MissingET>   met(tree(),"MissingET");
	d_ana::dBranchHandler<Vertex>      vrtx(tree(),"Vertex");

	TString jetCollection = "";
	if(getSampleFile().Contains("_0PU")) {jetCollection = "JetAK8";}
	else {jetCollection = "JetPUPPIAK8";}
	d_ana::dBranchHandler<Jet> jetAK8(tree(),jetCollection);
	d_ana::dBranchHandler<Jet> genjetAK8(tree(),"GenJetAK8");
	//std::cout<<"jetCollection="<<jetCollection<<", FName="<<getSampleFile()<<std::endl;

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
	TH1* histo=addPlot(new TH1D("histoname1","histotitle1",100,0,100),"p_{T} [GeV]","N_{e}");


	/*
	 * If (optionally) a skim or a flat ntuple is to be created, please use the following function to initialize
	 * the tree.
	 * The output files will be written automatically, and a config file will be created.
	 */
	TTree* myskim=addTree();
	/*
	 * Add a simple branch to the skim
	 */
	Int_t Nvrtx=0;
	Bool_t isSingEl=false;
	Bool_t isSingMu=false;
	Bool_t isAllHad=false;
	
	Double_t metPt =-999;
	Double_t metEta=-999;
	Double_t metPhi=-999;

	std::vector<Double_t> elPt;
	std::vector<Double_t> elEta;
	std::vector<Double_t> elPhi;
	
	std::vector<Double_t> muPt;
	std::vector<Double_t> muEta;
	std::vector<Double_t> muPhi;

	Int_t Njets=0;
	std::vector<Double_t> jetPt;
	std::vector<Double_t> jetEta;
	std::vector<Double_t> jetPhi;
	std::vector<Double_t> jetMass;
	std::vector<Double_t> jetBTag;
	std::vector<Double_t> jetTau1;
	std::vector<Double_t> jetTau2;
	std::vector<Double_t> jetTau3;
	std::vector<Double_t> jetSDMass;
	
	Int_t NAK8jets=0;
	std::vector<Double_t> jetAK8Pt;
	std::vector<Double_t> jetAK8Eta;
	std::vector<Double_t> jetAK8Phi;
	std::vector<Double_t> jetAK8Mass;
	std::vector<Double_t> jetAK8Tau1;
	std::vector<Double_t> jetAK8Tau2;
	std::vector<Double_t> jetAK8Tau3;
	std::vector<Double_t> jetAK8SDMass;

	std::vector<Double_t> genjetPt;
	std::vector<Double_t> genjetEta;
	std::vector<Double_t> genjetPhi;
	std::vector<Double_t> genjetMass;
	std::vector<Double_t> genjetAK8Pt;
	std::vector<Double_t> genjetAK8Eta;
	std::vector<Double_t> genjetAK8Phi;
	std::vector<Double_t> genjetAK8Mass;
	
	Double_t zpPt=-999;
	Double_t zpMass=-999;
	Double_t zpDeltaY=-999;
	Double_t zpDeltaPhi=-999;
	Double_t zpDeltaR=-999;
	TLorentzVector lepton_lv,j0_lv,j1_lv,zp_lv,W_lv,W_lv_r1,W_lv_r2,nu_lv1,nu_lv2,b_lv;
	
	myskim->Branch("Nvrtx", &Nvrtx);
	myskim->Branch("isSingEl", &isSingEl);
	myskim->Branch("isSingMu", &isSingMu);
	myskim->Branch("isAllHad", &isAllHad);
	myskim->Branch("elPt", &elPt);
	myskim->Branch("elEta", &elEta);
	myskim->Branch("elPhi", &elPhi);
	myskim->Branch("muPt", &muPt);
	myskim->Branch("muEta", &muEta);
	myskim->Branch("muPhi", &muPhi);
	myskim->Branch("metPt", &metPt);
	myskim->Branch("metEta", &metEta);
	myskim->Branch("metPhi", &metPhi);
	myskim->Branch("Njets", &Njets);
	myskim->Branch("jetPt", &jetPt);
	myskim->Branch("jetEta", &jetEta);
	myskim->Branch("jetPhi", &jetPhi);
	myskim->Branch("jetMass", &jetMass);
	myskim->Branch("jetBTag", &jetBTag);
	myskim->Branch("jetTau1", &jetTau1);
	myskim->Branch("jetTau2", &jetTau2);
	myskim->Branch("jetTau3", &jetTau3);
	myskim->Branch("jetSDMass", &jetSDMass);
	myskim->Branch("NAK8jets", &NAK8jets);
	myskim->Branch("jetAK8Pt", &jetAK8Pt);
	myskim->Branch("jetAK8Eta", &jetAK8Eta);
	myskim->Branch("jetAK8Phi", &jetAK8Phi);
	myskim->Branch("jetAK8Mass", &jetAK8Mass);
	myskim->Branch("jetAK8Tau1", &jetAK8Tau1);
	myskim->Branch("jetAK8Tau2", &jetAK8Tau2);
	myskim->Branch("jetAK8Tau3", &jetAK8Tau3);
	myskim->Branch("jetAK8SDMass", &jetAK8SDMass);
	myskim->Branch("zpPt", &zpPt);
	myskim->Branch("zpMass", &zpMass);
	myskim->Branch("zpDeltaY", &zpDeltaY);
	myskim->Branch("zpDeltaPhi", &zpDeltaPhi);
	myskim->Branch("zpDeltaR", &zpDeltaR);
	myskim->Branch("genjetPt", &genjetPt);
	myskim->Branch("genjetEta", &genjetEta);
	myskim->Branch("genjetPhi", &genjetPhi);
	myskim->Branch("genjetMass", &genjetMass);
	myskim->Branch("genjetAK8Pt", &genjetAK8Pt);
	myskim->Branch("genjetAK8Eta", &genjetAK8Eta);
	myskim->Branch("genjetAK8Phi", &genjetAK8Phi);
	myskim->Branch("genjetAK8Mass", &genjetAK8Mass);
	/*
	 * Or store a vector of objects (also possible to store only one object)
	 */
	//std::vector<Electron> skimmedelecs;
	//myskim->Branch("Electrons",&skimmedelecs);



	//std::cout<<"FName="<<getSampleFile()<<" contains _0PU? "<<getSampleFile().Contains("_0PU")<<std::endl;
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



		/*
		 * Begin the event-by-event analysis
		 */
		 
		Nvrtx = vrtx.size();
		 
		for(size_t i=0;i<elecs.size();i++){
			histo->Fill(elecs.at(i)->PT);
		}

		/*
		 * Or to fill the skim
		 */
		//skimmedelecs.clear();
		elPt.clear();
		elEta.clear();
		elPhi.clear();
		Int_t Nels = 0;
		for(size_t iel=0;iel<elecs.size();iel++){
			//flat info
			if(elecs.at(iel)->PT < 20) continue;
			if(fabs(elecs.at(iel)->Eta) > 2.4) continue;
			elPt.push_back(elecs.at(iel)->PT);
			elEta.push_back(elecs.at(iel)->Eta);
			elPhi.push_back(elecs.at(iel)->Phi);
			Nels++;
			//or objects
			//skimmedelecs.push_back(*elecs.at(i));
			}

		muPt.clear();
		muEta.clear();
		muPhi.clear();
		Int_t Nmus = 0;
		for(size_t imu=0;imu<muontight.size();imu++){
			//flat info
			if(muontight.at(imu)->PT < 20) continue;
			if(fabs(muontight.at(imu)->Eta) > 2.4) continue;
			muPt.push_back(muontight.at(imu)->PT);
			muEta.push_back(muontight.at(imu)->Eta);
			muPhi.push_back(muontight.at(imu)->Phi);
			Nmus++;
			}

		isSingEl=false;
		isSingMu=false;
		isAllHad=false;
		if(Nels==0 && Nmus==0){isAllHad=true;} 
		else if(Nels==1 && Nmus==0){isSingEl=true;}
		else if(Nels==0 && Nmus==1){isSingMu=true;}
		
		metPt  = met.at(0)->MET;
		metEta = met.at(0)->Eta;
		metPhi = met.at(0)->Phi;

		Njets = 0;
		jetPt.clear();
		jetEta.clear();
		jetPhi.clear();
		jetMass.clear();
		jetBTag.clear();
		jetTau1.clear();
		jetTau2.clear();
		jetTau3.clear();
		jetSDMass.clear();
		for(size_t ijet=0;ijet<jet.size();ijet++){
			if(jet.at(ijet)->PT < 30) continue;
			if(fabs(jet.at(ijet)->Eta) > 4) continue;
			jetPt.push_back(jet.at(ijet)->PT);
			jetEta.push_back(jet.at(ijet)->Eta);
			jetPhi.push_back(jet.at(ijet)->Phi);
			jetMass.push_back(jet.at(ijet)->Mass);
			jetBTag.push_back(jet.at(ijet)->BTag);
			jetTau1.push_back(jet.at(ijet)->Tau[0]);
			jetTau2.push_back(jet.at(ijet)->Tau[1]);
			jetTau3.push_back(jet.at(ijet)->Tau[2]);
			jetSDMass.push_back(jet.at(ijet)->SoftDroppedJet.M());
			Njets++;
			}
		
		NAK8jets = 0;
		jetAK8Pt.clear();
		jetAK8Eta.clear();
		jetAK8Phi.clear();
		jetAK8Mass.clear();
		jetAK8Tau1.clear();
		jetAK8Tau2.clear();
		jetAK8Tau3.clear();
		jetAK8SDMass.clear();
		for(size_t ijet=0;ijet<jetAK8.size();ijet++){
			if(jetAK8.at(ijet)->PT < 400) continue;
			if(fabs(jetAK8.at(ijet)->Eta) > 4) continue;
			if(jetAK8.at(ijet)->SoftDroppedJet.M() < 50) continue;
			jetAK8Pt.push_back(jetAK8.at(ijet)->PT);
			jetAK8Eta.push_back(jetAK8.at(ijet)->Eta);
			jetAK8Phi.push_back(jetAK8.at(ijet)->Phi);
			jetAK8Mass.push_back(jetAK8.at(ijet)->Mass);
			jetAK8Tau1.push_back(jetAK8.at(ijet)->Tau[0]);
			jetAK8Tau2.push_back(jetAK8.at(ijet)->Tau[1]);
			jetAK8Tau3.push_back(jetAK8.at(ijet)->Tau[2]);
			jetAK8SDMass.push_back(jetAK8.at(ijet)->SoftDroppedJet.M());
			NAK8jets++;
			}

		genjetPt.clear();
		genjetEta.clear();
		genjetPhi.clear();
		genjetMass.clear();
		for(size_t ijet=0;ijet<genjet.size();ijet++){
			genjetPt.push_back(genjet.at(ijet)->PT);
			genjetEta.push_back(genjet.at(ijet)->Eta);
			genjetPhi.push_back(genjet.at(ijet)->Phi);
			genjetMass.push_back(genjet.at(ijet)->Mass);
			}
		genjetAK8Pt.clear();
		genjetAK8Eta.clear();
		genjetAK8Phi.clear();
		genjetAK8Mass.clear();
		for(size_t ijet=0;ijet<genjetAK8.size();ijet++){
			genjetAK8Pt.push_back(genjetAK8.at(ijet)->PT);
			genjetAK8Eta.push_back(genjetAK8.at(ijet)->Eta);
			genjetAK8Phi.push_back(genjetAK8.at(ijet)->Phi);
			genjetAK8Mass.push_back(genjetAK8.at(ijet)->Mass);
			}
		
		if(isAllHad && NAK8jets>1){ //All-had reconstruction
	      j0_lv.SetPtEtaPhiM(jetAK8Pt.at(0),jetAK8Eta.at(0),jetAK8Phi.at(0),jetAK8Mass.at(0));
		  j1_lv.SetPtEtaPhiM(jetAK8Pt.at(1),jetAK8Eta.at(1),jetAK8Phi.at(1),jetAK8Mass.at(1));
		  zp_lv = j0_lv+j1_lv;
      	  Double_t j0_rap = 0.5*log((j0_lv.E()+j0_lv.P())/(j0_lv.E()-j0_lv.P()));
      	  Double_t j1_rap = 0.5*log((j1_lv.E()+j1_lv.P())/(j1_lv.E()-j1_lv.P()));
      	  zpPt = zp_lv.Pt();
      	  zpMass = zp_lv.M();
      	  zpDeltaY = fabs(j0_rap-j1_rap);
      	  zpDeltaPhi = j0_lv.DeltaPhi(j1_lv);
      	  zpDeltaR = j0_lv.DeltaR(j1_lv);
		  }

		if((isSingEl || isSingMu) && Njets>0 && NAK8jets>0){ //Single-lepton reconstruction
	      j0_lv.SetPtEtaPhiM(jetAK8Pt.at(0),jetAK8Eta.at(0),jetAK8Phi.at(0),jetAK8Mass.at(0));
	      
          // ----------------------------------------------------------------------------
          // W --> l nu with mass constraint
          // ----------------------------------------------------------------------------
          
          Double_t lepM;
          if(isSingMu){
            lepM = 0.105658367;
            lepton_lv.SetPtEtaPhiM(muPt.at(0),muEta.at(0),muPhi.at(0),lepM);
          }else{
          	lepM = 0.00051099891;
            lepton_lv.SetPtEtaPhiM(elPt.at(0),elEta.at(0),elPhi.at(0),lepM);
         	}
	         
          Double_t metPx = metPt*cos(metPhi);
          Double_t metPy = metPt*sin(metPhi);
          
          Double_t Dtmp = MW*MW-lepM*lepM+2.0*(lepton_lv.Px()*metPx+lepton_lv.Py()*metPy);
          Double_t Atmp = 4.0*(lepton_lv.Energy()*lepton_lv.Energy()-lepton_lv.Pz()*lepton_lv.Pz());
          Double_t Btmp =-4.0*Dtmp*lepton_lv.Pz();
          Double_t Ctmp = 4.0*lepton_lv.Energy()*lepton_lv.Energy()*metPt*metPt-Dtmp*Dtmp;
          
          Double_t nuPz_1;
          Double_t nuPz_2;
          
          Double_t DETtmp = Btmp*Btmp-4.0*Atmp*Ctmp;
          
          if(DETtmp >= 0){ // real roots
            nuPz_1 = (-Btmp+TMath::Sqrt(DETtmp))/(2.0*Atmp);
            nuPz_2 = (-Btmp-TMath::Sqrt(DETtmp))/(2.0*Atmp);
            nu_lv1.SetPxPyPzE(metPx,metPy,nuPz_1,TMath::Sqrt(metPt*metPt+nuPz_1*nuPz_1));
            nu_lv2.SetPxPyPzE(metPx,metPy,nuPz_2,TMath::Sqrt(metPt*metPt+nuPz_2*nuPz_2));
            W_lv_r1 = nu_lv1+lepton_lv;
            W_lv_r2 = nu_lv2+lepton_lv;
          }else{ // complex roots
            nuPz_1 = (-Btmp)/(2.0*Atmp);
            nuPz_2 = (-Btmp)/(2.0*Atmp);
            Double_t alpha = (lepton_lv.Px()*metPx+lepton_lv.Py()*metPy)/metPt;
            Double_t Delta = MW*MW-lepM*lepM;
            Atmp = 4.0*(lepton_lv.Pz()*lepton_lv.Pz()-lepton_lv.Energy()*lepton_lv.Energy()+alpha*alpha);
            Btmp = 4.0*alpha*Delta;
            Ctmp = Delta*Delta;
            DETtmp = Btmp*Btmp-4.0*Atmp*Ctmp;
            Double_t pTnu_1 = (-Btmp+TMath::Sqrt(DETtmp))/(2.0*Atmp);
            Double_t pTnu_2 = (-Btmp-TMath::Sqrt(DETtmp))/(2.0*Atmp);
            nu_lv1.SetPxPyPzE(metPx*(pTnu_1)/(metPt),metPy*(pTnu_1)/(metPt),nuPz_1,TMath::Sqrt((pTnu_1)*(pTnu_1)+(nuPz_1)*(nuPz_1)));
            nu_lv2.SetPxPyPzE(metPx*(pTnu_2)/(metPt),metPy*(pTnu_2)/(metPt),nuPz_2,TMath::Sqrt((pTnu_2)*(pTnu_2)+(nuPz_2)*(nuPz_2)));
            W_lv_r1 = nu_lv1+lepton_lv;
            W_lv_r2 = nu_lv2+lepton_lv;
            if (fabs(W_lv_r1.M()-MW) < fabs(W_lv_r2.M()-MW)) W_lv_r2 = W_lv_r1;
            else W_lv_r1 = W_lv_r2;
            }
            
          // ----------------------------------------------------------------------------
      	  // top --> W b --> l nu b using W from above
          // ----------------------------------------------------------------------------
          
          Double_t dMTOP = 1e8;
          Int_t bIndex = -1;
          Bool_t firstW = true;
          Double_t MTop_1, MTop_2;
          for(unsigned int ijet=0; ijet < jetPt.size(); ijet++){
	         b_lv.SetPtEtaPhiM(jetPt.at(ijet),jetEta.at(ijet),jetPhi.at(ijet),jetMass.at(ijet));
	         if(j0_lv.DeltaR(b_lv)<1.2) continue; //Require AK4 and AK8 jets to be well separated (value from B2G-17-017)
	         MTop_1 = (b_lv + W_lv_r1).M();
	         MTop_2 = (b_lv + W_lv_r2).M();
	         if(fabs(MTop_1 - MTOP) < dMTOP){
	           if(fabs(MTop_1 - MTOP) < fabs(MTop_2 - MTOP)){
	             firstW = true;
	             bIndex = ijet;
	             dMTOP = fabs(MTop_1 - MTOP);
	           }else{
	             firstW = false;
	             bIndex = ijet;
	             dMTOP = fabs(MTop_2 - MTOP);
	             }
	         }else if(fabs(MTop_2 - MTOP) < dMTOP){
	           firstW = false;
	           bIndex = ijet;
	           dMTOP = fabs(MTop_2 - MTOP);
	           }
	         }

          if(firstW) {W_lv = W_lv_r1;}
          else{W_lv = W_lv_r2;}
          
          if(bIndex<0){
          	std::cout<<"No b-jet was found near leptonic W! Continuing ..."<<std::endl;
          }else{
            b_lv.SetPtEtaPhiM(jetPt.at(bIndex),jetEta.at(bIndex),jetPhi.at(bIndex),jetMass.at(bIndex));
            j1_lv = W_lv+b_lv; //Leptonic top LV
		    zp_lv = j0_lv+j1_lv;
      	    Double_t j0_rap = 0.5*log((j0_lv.E()+j0_lv.P())/(j0_lv.E()-j0_lv.P()));
      	    Double_t j1_rap = 0.5*log((j1_lv.E()+j1_lv.P())/(j1_lv.E()-j1_lv.P()));
      	    zpPt = zp_lv.Pt();
      	    zpMass = zp_lv.M();
      	    zpDeltaY = fabs(j0_rap-j1_rap);
      	    zpDeltaPhi = j0_lv.DeltaPhi(j1_lv);
      	    zpDeltaR = j0_lv.DeltaR(j1_lv);
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



void DAnalysis::postProcess(){
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
	d_ana::sampleCollection samplecoll;
	samplecoll.readFromFile(getOutPath());

	std::vector<TString> alllegends = samplecoll.listAllLegends();

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
	if(alllegends.size()>0){
		d_ana::histoCollection histos=samplecoll.getHistos(alllegends.at(0));

		/*
		 * here, the histogram created in the analyze() function is selected and evaluated
		 * The histoCollection maintains ownership (you don't need to delete the histogram)
		 */
		const TH1* myplot=histos.getHisto("histoname1");

		std::cout << "(example output): the integral is " << myplot->Integral() <<std::endl;

		/*
		 * If the histogram is subject to changes, please clone it and take ownership
		 */

		TH1* myplot2=histos.cloneHisto("histoname1");

		/*
		 * do something with the histogram
		 */

		delete myplot2;
	}

	/*
	 * do the extraction here.
	 */



}



