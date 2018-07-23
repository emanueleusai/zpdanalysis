/*
 * metskim.h
 *
 *  Created on: 24 Aug 2016
 *      Author: jkiesele
 */

#ifndef metskim_H_
#define metskim_H_

#include "interface/basicAnalyzer.h"
#include "interface/sampleCollection.h"
#include "classes/DelphesClasses.h"


class metskim: public d_ana::basicAnalyzer{
public:
	metskim():d_ana::basicAnalyzer(){}
	~metskim(){}


private:
	void analyze(size_t id);

	void postProcess();
};





#endif /* metskim_H_ */
