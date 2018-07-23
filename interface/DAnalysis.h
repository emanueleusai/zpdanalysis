/*
 * DAnalysis.h
 *
 *  Created on: 24 Aug 2016
 *      Author: jkiesele
 */

#ifndef DAnalysis_H_
#define DAnalysis_H_

#include "interface/basicAnalyzer.h"
#include "interface/sampleCollection.h"
#include "classes/DelphesClasses.h"


class DAnalysis: public d_ana::basicAnalyzer{
public:
	DAnalysis():d_ana::basicAnalyzer(){}
	~DAnalysis(){}


private:
	void analyze(size_t id);

	void postProcess();
};





#endif /* DAnalysis_H_ */
