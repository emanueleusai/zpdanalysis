/*
 * skim.h
 *
 *  Created on: 24 Aug 2016
 *      Author: jkiesele
 */

#ifndef skim_H_
#define skim_H_

#include "interface/basicAnalyzer.h"
#include "interface/sampleCollection.h"
#include "classes/DelphesClasses.h"


class skim: public d_ana::basicAnalyzer{
public:
	skim():d_ana::basicAnalyzer(){}
	~skim(){}


private:
	void analyze(size_t id);

	void postProcess();
};





#endif /* skim_H_ */
