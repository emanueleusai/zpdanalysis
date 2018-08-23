// -*- C++ -*-
//
// Package:    PhaseTwoAnalysis/MetStudies
// Class:      MetStudies
// 
/**\class MetStudies MetStudies.cc PhaseTwoAnalysis/MetStudies/plugins/MetStudies.cc

 Description: [one line class summary]

 Implementation:
     [Notes on implementation]
*/
//
// Original Author:  Emanuele Usai
//         Created:  Wed, 01 Aug 2018 20:28:27 GMT
//
//


// system include files
#include <memory>

// user include files
#include "FWCore/Framework/interface/Frameworkfwd.h"
#include "FWCore/Framework/interface/one/EDAnalyzer.h"

#include "FWCore/Framework/interface/Event.h"
#include "FWCore/Framework/interface/MakerMacros.h"

#include "FWCore/ParameterSet/interface/ParameterSet.h"
#include "DataFormats/PatCandidates/interface/MET.h"
#include "DataFormats/PatCandidates/interface/Jet.h"
#include "DataFormats/JetReco/interface/GenJet.h"
#include "DataFormats/PatCandidates/interface/Electron.h"
#include "DataFormats/PatCandidates/interface/Muon.h"
#include "DataFormats/ParticleFlowCandidate/interface/PFCandidateFwd.h"
#include "DataFormats/PatCandidates/interface/PackedGenParticle.h"
#include "SimDataFormats/GeneratorProducts/interface/GenEventInfoProduct.h"
#include "TTree.h"
#include "TLorentzVector.h"
using namespace std;
//
// class declaration
//

// If the analyzer does not use TFileService, please remove
// the template argument to the base class so the class inherits
// from  edm::one::EDAnalyzer<> and also remove the line from
// constructor "usesResource("TFileService");"
// This will improve performance in multithreaded jobs.

class MetStudies : public edm::one::EDAnalyzer<edm::one::SharedResources>  {
   public:
      explicit MetStudies(const edm::ParameterSet&);
      ~MetStudies();

      static void fillDescriptions(edm::ConfigurationDescriptions& descriptions);


   private:
      virtual void beginJob() override;
      virtual void analyze(const edm::Event&, const edm::EventSetup&) override;
      virtual void endJob() override;

      TFile *tf1;
      TTree* s;

      TLorentzVector met;
      Double_t met_t;
      Double_t met_p;
      TLorentzVector puppi_met;
      Double_t puppi_met_t;
      Double_t puppi_met_p;
      TLorentzVector gen_met;
      Double_t gen_met_t;
      Double_t gen_met_p;
      TLorentzVector genpileup_met;
      Double_t genpileup_met_t;
      Double_t genpileup_met_p;

      TLorentzVector l1;
      TLorentzVector l2;
      TLorentzVector median;
      TLorentzVector z;

      Double_t npv;
      Double_t njet;
      Double_t npuppijet;
      Double_t ngenjet;
      Double_t ht;
      Double_t puppi_ht;
      Double_t gen_ht;
      Double_t rho;

      TLorentzVector jetsum;
      Double_t jetsum_t;
      Double_t jetsum_p;
      TLorentzVector puppi_jetsum;
      Double_t puppi_jetsum_t;
      Double_t puppi_jetsum_p;
      TLorentzVector gen_jetsum;
      Double_t gen_jetsum_t;
      Double_t gen_jetsum_p;
      TLorentzVector pfsum;
      Double_t pfsum_t;
      Double_t pfsum_p;

      Double_t weight;


      edm::EDGetTokenT<vector<pat::Jet> > tokenslimmedJets_;
      edm::EDGetTokenT<vector<pat::Jet> > tokenslimmedJetsPuppi_;
      edm::EDGetTokenT<vector<reco::GenJet> > tokenslimmedGenJets_;

      edm::EDGetTokenT<vector<pat::MET> > tokenslimmedMETs_;
      edm::EDGetTokenT<vector<pat::MET> > tokenslimmedMETsNoHF_;
      edm::EDGetTokenT<vector<pat::MET> > tokenslimmedMETsPuppi_;
      edm::EDGetTokenT<vector<reco::GenMET> > tokengenMetTrue_;

      edm::EDGetTokenT<double> tokenfixedGridRhoAll_;

      edm::EDGetTokenT<vector<pat::Electron> > tokenslimmedElectrons_;
      edm::EDGetTokenT<vector<pat::Muon> > tokenslimmedMuons_;

      edm::EDGetTokenT<vector<pat::PackedGenParticle> > tokenpackedGenParticles_;
      edm::EDGetTokenT<vector<reco::GenParticle> > tokenprunedGenParticles_;
      edm::EDGetTokenT<vector<pat::PackedCandidate> > tokenpackedPFCandidates_;

      edm::EDGetTokenT<vector<reco::Vertex> > tokenofflineSlimmedPrimaryVertices_;
 
      edm::EDGetTokenT<GenEventInfoProduct > tokengenerator_;


      // ----------member data ---------------------------
};

//
// constants, enums and typedefs
//

//
// static data member definitions
//

//
// constructors and destructor
//
MetStudies::MetStudies(const edm::ParameterSet& iConfig)

{
   //now do what ever initialization is needed
   usesResource("TFileService");

   tf1 = new TFile("metstudies_output.root", "RECREATE");  
   s = new TTree("s","s");

   s->Branch("weight",&weight);

   s->Branch("met",&met);
   s->Branch("met_t",&met_t);
   s->Branch("met_p",&met_p);
   s->Branch("puppi_met",&puppi_met);
   s->Branch("puppi_met_t",&puppi_met_t);
   s->Branch("puppi_met_p",&puppi_met_p);
   s->Branch("gen_met",&gen_met);
   s->Branch("gen_met_t",&gen_met_t);
   s->Branch("gen_met_p",&gen_met_p);
   s->Branch("genpileup_met",&genpileup_met);
   s->Branch("genpileup_met_t",&genpileup_met_t);
   s->Branch("genpileup_met_p",&genpileup_met_p);

   s->Branch("l1",&l1);
   s->Branch("l2",&l2);
   s->Branch("median",&median);
   s->Branch("z",&z);

   s->Branch("npv",&npv);
   s->Branch("njet",&njet);
   s->Branch("npuppijet",&npuppijet);
   s->Branch("ngenjet",&ngenjet);
   s->Branch("ht",&ht);
   s->Branch("rho",&rho);

   s->Branch("jetsum",&jetsum);
   s->Branch("jetsum_t",&jetsum_t);
   s->Branch("jetsum_p",&jetsum_p);
   s->Branch("puppi_jetsum",&puppi_jetsum);
   s->Branch("puppi_jetsum_t",&puppi_jetsum_t);
   s->Branch("puppi_jetsum_p",&puppi_jetsum_p);
   s->Branch("gen_jetsum",&gen_jetsum);
   s->Branch("gen_jetsum_t",&gen_jetsum_t);
   s->Branch("gen_jetsum_p",&gen_jetsum_p);

   s->Branch("puppi_ht",&puppi_ht);
   s->Branch("gen_ht",&gen_ht);
   s->Branch("pfsum",&pfsum);
   s->Branch("pfsum_t",&pfsum_t);
   s->Branch("pfsum_p",&pfsum_p);

   tokenslimmedJets_ = consumes<vector<pat::Jet> >(edm::InputTag("slimmedJets"));
   tokenslimmedJetsPuppi_ = consumes<vector<pat::Jet> >(edm::InputTag("slimmedJetsPuppi"));
   tokenslimmedGenJets_ = consumes<vector<reco::GenJet> >(edm::InputTag("slimmedGenJets"));

   tokenslimmedMETs_ = consumes<vector<pat::MET> >(edm::InputTag("slimmedMETs"));
   tokenslimmedMETsNoHF_ = consumes<vector<pat::MET> >(edm::InputTag("slimmedMETsNoHF"));
   tokenslimmedMETsPuppi_ = consumes<vector<pat::MET> >(edm::InputTag("slimmedMETsPuppi"));
   tokengenMetTrue_ = consumes<vector<reco::GenMET> >(edm::InputTag("genMetTrue"));

   tokenfixedGridRhoAll_ = consumes<double>(edm::InputTag("fixedGridRhoAll"));

   tokenslimmedElectrons_ = consumes<vector<pat::Electron> >(edm::InputTag("slimmedElectrons"));
   tokenslimmedMuons_ = consumes<vector<pat::Muon> >(edm::InputTag("slimmedMuons"));

   tokenpackedGenParticles_ = consumes<vector<pat::PackedGenParticle> >(edm::InputTag("packedGenParticles"));
   tokenprunedGenParticles_ = consumes<vector<reco::GenParticle> >(edm::InputTag("prunedGenParticles"));
   tokenpackedPFCandidates_ = consumes<vector<pat::PackedCandidate> >(edm::InputTag("packedPFCandidates"));

   tokenofflineSlimmedPrimaryVertices_ = consumes<vector<reco::Vertex> >(edm::InputTag("offlineSlimmedPrimaryVertices"));

   tokengenerator_ = consumes<GenEventInfoProduct>(edm::InputTag("generator"));
}


MetStudies::~MetStudies()
{
 
   // do anything here that needs to be done at desctruction time
   // (e.g. close files, deallocate resources etc.)
    tf1->cd();
  s->Write();
  tf1->Write();
  tf1->Close(); 

}


//
// member functions
//

// ------------ method called for each event  ------------
void
MetStudies::analyze(const edm::Event& iEvent, const edm::EventSetup& iSetup)
{
   using namespace edm;



#ifdef THIS_IS_AN_EVENT_EXAMPLE
   Handle<ExampleData> pIn;
   iEvent.getByLabel("example",pIn);
#endif
   
#ifdef THIS_IS_AN_EVENTSETUP_EXAMPLE
   ESHandle<SetupData> pSetup;
   iSetup.get<SetupRecord>().get(pSetup);
#endif


   // Handle<reco::PFCandidateCollection> pfCandidates;
   // iEvent.getByToken(tokenPFCandidates_, pfCandidates);

   Handle<vector<pat::Jet> > slimmedJets;
   Handle<vector<pat::Jet> > slimmedJetsPuppi;
   Handle<vector<reco::GenJet> > slimmedGenJets;

   Handle<vector<pat::MET> > slimmedMETs;
   Handle<vector<pat::MET> > slimmedMETsNoHF;
   Handle<vector<pat::MET> > slimmedMETsPuppi;
   Handle<vector<reco::GenMET> > genMetTrue;

   Handle<double> fixedGridRhoAll;

   Handle<vector<pat::Electron> > slimmedElectrons;
   Handle<vector<pat::Muon> > slimmedMuons;

   Handle<vector<pat::PackedGenParticle> > packedGenParticles;
   Handle<vector<reco::GenParticle> > prunedGenParticles;
   Handle<vector<pat::PackedCandidate> > packedPFCandidates;

   Handle<vector<reco::Vertex> > offlineSlimmedPrimaryVertices;
   Handle<GenEventInfoProduct> generator;

   iEvent.getByToken(tokenslimmedJets_, slimmedJets);
   iEvent.getByToken(tokenslimmedJetsPuppi_, slimmedJetsPuppi);
   iEvent.getByToken(tokenslimmedGenJets_, slimmedGenJets);

   iEvent.getByToken(tokenslimmedMETs_, slimmedMETs);
   iEvent.getByToken(tokenslimmedMETsNoHF_, slimmedMETsNoHF);
   iEvent.getByToken(tokenslimmedMETsPuppi_, slimmedMETsPuppi);
   iEvent.getByToken(tokengenMetTrue_, genMetTrue);

   iEvent.getByToken(tokenfixedGridRhoAll_, fixedGridRhoAll);

   iEvent.getByToken(tokenslimmedElectrons_, slimmedElectrons);
   iEvent.getByToken(tokenslimmedMuons_, slimmedMuons);

   iEvent.getByToken(tokenpackedGenParticles_, packedGenParticles);
   iEvent.getByToken(tokenprunedGenParticles_, prunedGenParticles);
   iEvent.getByToken(tokenpackedPFCandidates_, packedPFCandidates);

   iEvent.getByToken(tokenofflineSlimmedPrimaryVertices_, offlineSlimmedPrimaryVertices);
   iEvent.getByToken(tokengenerator_, generator);


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
   weight = 1;

   puppi_ht = 0;
   gen_ht = 0;
   pfsum.SetXYZT(0,0,0,0);
   pfsum_t = 0;
   pfsum_p = 0;


    if (slimmedElectrons->size()<2 && slimmedMuons->size()<2) return;
    if (slimmedElectrons->size()>1 && slimmedMuons->size()<2)
    {
      l1.SetPxPyPzE(slimmedElectrons->at(0).px(),slimmedElectrons->at(0).py(),slimmedElectrons->at(0).pz(),slimmedElectrons->at(0).energy());
      l2.SetPxPyPzE(slimmedElectrons->at(1).px(),slimmedElectrons->at(1).py(),slimmedElectrons->at(1).pz(),slimmedElectrons->at(1).energy());
    } 
    if (slimmedMuons->size()>1 && slimmedElectrons->size()<2)
    {
      l1.SetPxPyPzE(slimmedMuons->at(0).px(),slimmedMuons->at(0).py(),slimmedMuons->at(0).pz(),slimmedMuons->at(0).energy());
      l2.SetPxPyPzE(slimmedMuons->at(1).px(),slimmedMuons->at(1).py(),slimmedMuons->at(1).pz(),slimmedMuons->at(1).energy());
    } 
    if (slimmedElectrons->size()>1 && slimmedMuons->size()>1)
    {
      float epair= (slimmedElectrons->at(0).p4()+slimmedElectrons->at(1).p4()).M();
      float mupair= (slimmedMuons->at(0).p4()+slimmedMuons->at(1).p4()).M();
      if (fabs(91.2-mupair)<fabs(91.2-epair))
      {
        l1.SetPxPyPzE(slimmedMuons->at(0).px(),slimmedMuons->at(0).py(),slimmedMuons->at(0).pz(),slimmedMuons->at(0).energy());
        l2.SetPxPyPzE(slimmedMuons->at(1).px(),slimmedMuons->at(1).py(),slimmedMuons->at(1).pz(),slimmedMuons->at(1).energy());
      }
      else
      {
        l1.SetPxPyPzE(slimmedElectrons->at(0).px(),slimmedElectrons->at(0).py(),slimmedElectrons->at(0).pz(),slimmedElectrons->at(0).energy());
        l2.SetPxPyPzE(slimmedElectrons->at(1).px(),slimmedElectrons->at(1).py(),slimmedElectrons->at(1).pz(),slimmedElectrons->at(1).energy());
      }
    } 
    //weight = weights->at(0)->Weight;
    met.SetPxPyPzE(slimmedMETs->at(0).px(),slimmedMETs->at(0).py(),slimmedMETs->at(0).pz(),slimmedMETs->at(0).energy());
    puppi_met.SetPxPyPzE(slimmedMETsPuppi->at(0).px(),slimmedMETsPuppi->at(0).py(),slimmedMETsPuppi->at(0).pz(),slimmedMETsPuppi->at(0).energy());
    gen_met.SetPxPyPzE(genMetTrue->at(0).px(),genMetTrue->at(0).py(),genMetTrue->at(0).pz(),genMetTrue->at(0).energy());
    genpileup_met.SetPxPyPzE(slimmedMETsNoHF->at(0).px(),slimmedMETsNoHF->at(0).py(),slimmedMETsNoHF->at(0).pz(),slimmedMETsNoHF->at(0).energy());
    for (const auto& j : *slimmedJets)
      ht+=j.pt();
    for (const auto& j : *slimmedJetsPuppi)
      puppi_ht+=j.pt();
    for (const auto& j : *slimmedGenJets)
      gen_ht+=j.pt();
    rho=*fixedGridRhoAll;
    npv = offlineSlimmedPrimaryVertices->size();
    njet = slimmedJets->size();
    npuppijet = slimmedJetsPuppi->size();
    ngenjet = slimmedGenJets->size();

    for (const auto& j : *slimmedJets)
      jetsum+=TLorentzVector(j.px(),j.py(),j.pz(),j.energy());

    for (const auto& j : *slimmedJetsPuppi)
      puppi_jetsum+=TLorentzVector(j.px(),j.py(),j.pz(),j.energy());

    for (const auto& j : *slimmedGenJets)
      gen_jetsum+=TLorentzVector(j.px(),j.py(),j.pz(),j.energy());

    for (const auto& j : *packedPFCandidates)
      pfsum+=TLorentzVector(j.px(),j.py(),j.pz(),j.energy());

    for (const auto& j : *packedGenParticles)
    {
      if (j.pdgId()==23)
      {
        z.SetPxPyPzE(j.px(),j.py(),j.pz(),j.energy());
        break;
      }
    }
    median=l1+l2;
    TVector3 parallel=median.Vect().Unit();
    TVector3 transverse=median.Vect().Orthogonal();

    met_t = transverse.Dot(met.Vect());
    met_p = parallel.Dot(met.Vect());

    puppi_met_t = transverse.Dot(puppi_met.Vect());
    puppi_met_p = parallel.Dot(puppi_met.Vect());

    gen_met_t = transverse.Dot(gen_met.Vect());
    gen_met_p = parallel.Dot(gen_met.Vect());

    genpileup_met_t = transverse.Dot(genpileup_met.Vect());
    genpileup_met_p = parallel.Dot(genpileup_met.Vect());

    jetsum_t = transverse.Dot(jetsum.Vect());
    jetsum_p = parallel.Dot(jetsum.Vect());

    puppi_jetsum_t = transverse.Dot(puppi_jetsum.Vect());
    puppi_jetsum_p = parallel.Dot(puppi_jetsum.Vect());

    gen_jetsum_t = transverse.Dot(gen_jetsum.Vect());
    gen_jetsum_p = parallel.Dot(gen_jetsum.Vect());

    pfsum_t = transverse.Dot(pfsum.Vect());
    pfsum_p = parallel.Dot(pfsum.Vect());

    weight = generator->weight();

   s->Fill();

}


// ------------ method called once each job just before starting event loop  ------------
void 
MetStudies::beginJob()
{
}

// ------------ method called once each job just after ending the event loop  ------------
void 
MetStudies::endJob() 
{
}

// ------------ method fills 'descriptions' with the allowed parameters for the module  ------------
void
MetStudies::fillDescriptions(edm::ConfigurationDescriptions& descriptions) {
  //The following says we do not know what parameters are allowed so do no validation
  // Please change this to state exactly what you do use, even if it is no parameters
  edm::ParameterSetDescription desc;
  desc.setUnknown();
  descriptions.addDefault(desc);
}

//define this as a plug-in
DEFINE_FWK_MODULE(MetStudies);
