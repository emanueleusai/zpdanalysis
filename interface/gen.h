/*
 * gen.h
 *
 *  Created on: 24 Aug 2016
 *      Author: jkiesele
 */

#ifndef gen_H_
#define gen_H_

#include "interface/basicAnalyzer.h"
#include "interface/sampleCollection.h"
#include "classes/DelphesClasses.h"


class gen: public d_ana::basicAnalyzer{
public:
	gen():d_ana::basicAnalyzer(){}
	~gen(){}


private:
	void analyze(size_t id);

	void postProcess();
};





#endif /* gen_H_ */
