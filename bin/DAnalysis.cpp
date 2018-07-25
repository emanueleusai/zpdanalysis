/*
 * DAnalysis_EXEC.cpp
 *
 *  Created on: 24 Aug 2016
 *      Author: jkiesele
 */


#include <iostream>
#include "interface/DAnalysis.h"

int main(int argc, char* argv[]){

	if(argc!=2){
		std::cout << "DAnalysis: need exactly one input file" <<std::endl;
		exit (-1);
	}


	std::string inputfile=argv[1];

	DAnalysis analyser;


	analyser.readConfigFile(inputfile);

	analyser.start();

	return 1;
}
