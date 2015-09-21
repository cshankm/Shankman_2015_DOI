This document provides a description of the SurveySimulator package.
The SurveySimulator software package simulates the detection of a model distribution of Trans-Neptunian Objects (TNOs) subject to the detection characteristics of a given survey. 
This package proivides the SureveySimulator software as well as the characterization files for the three TNO surveys: [CFEPS](http://adsabs.harvard.edu/abs/2011AJ....142..131P), [Alexandersen et al. 2015](http://arxiv.org/abs/1411.7953) and [OSSOS](http://www.ossos-survey.org/). 
This version of the package is offered as a companion to Shankman et al. 2015 (an analysis the H-magnitude distribution of the Scattering TNOs)

TNO surveys have a number of strong observational biases. 
To draw meaningful conclusions regarding the intrinsic distribution of TNOs, these biases must be taken into consideration. 
Each of the above mentioned surveys has been carefully designed to minimize tracking biases and have had their detection biases carefully characterised. 
The characterisics of the observational biases are recorded in the \*.eff files stored in the directory "ALL". 

The Survey Simulator takes a straightforward approach to handling the observational biases. 
As one cannot know what was not seen in a particular survey, discovering the intrinsic TNO distribution by de-biasing the observed sample is not possible. 
Instead, the Survey Simulator takes a model for the intrinsic distribution of TNOs and applies the survey's measured detection biases. 
A model is forward biased through the Survey Simulator to produce a set of "Simulated Detections" that can then be compared to the actual detected sample. 
The SurveySimulator executes a loop, continuously drawing objects from a model until a specified number of sources have been "detected".
The following papers provide some details on the design of the Survey Simulator:

Jones et al. 2006: [http://adsabs.harvard.edu/abs/2006Icar..185..508J](http://adsabs.harvard.edu/abs/2006Icar..185..508J)

Petit et al. 2011: [http://adsabs.harvard.edu/abs/2011AJ....142..131P](http://adsabs.harvard.edu/abs/2011AJ....142..131P)

Here we provide the implementation of the Survey Simulator we used to examine the absolute magnitude distribution (H) of the Scattering TNOs. 
The SurveySimulator is written in Fortran (included here as SurveySubs.f) with a python wrapper (Driver.py). 
SurveySubs.f must be compiled on your machine, and then the Driver.py module is called as a python script, e.g. "python problem.py".
Using the SurveySimulator we forward biased the [Kaib et al. 2011](http://adsabs.harvard.edu/abs/2011Icar..215..491K) orbital model of scattering objects (q200_scattering_hot_alt1k_aei.dat) joined with a given H-distribution. 
For a description of the paramaterisation of H-magnitudes and details on our statisical techniques, see Shankman et al. 2015


To compile SurveySubs.f with f2py, use a command like:

f2py -c --f77exec=/usr/bin/gfortran --f77flags=-fPIC -m SurveySubs SurveySubs.f

You may need to change the path to your gfortan compiler.

There are two files you may immediately want to edit:

* num_to_track.txt - this specifies the number of objects the Survey Simulator needs to track
* H_dist_vars.txt  - this specifies the parameters of the H-distribution to be tested


# Workflow:

* Driver.py (run this file)
  * calls GiMiObj, which, at each call, returns one object with orbital parameters, colour conversion list (e.g. g-r), H-magnitude, and phase curve information
    * this uses ssimTools.py tools to generate an H magnitude and for writing output
  * calls the *detect*  method within SurveySimulator.f with the given object to check for detection, returning the detected characteristics if the object is declared as detected. 
  * writes outputs


## Driver.py
### Inputs
* input.file	       - a file containing the number of lines in a file and the file name. This is generated from the output of the shell command `wc -l filename`
* seeds.txt    	       - a file containing the random number generator seed for the simulation
* number_to_track.txt  - a file containing the desired number of tracked objects from the survey simulator
* surveydir.txt        - a file containing the name of the folder which contains the survey characterisations 
* H_dist_vars.txt      - a file containing the parameters of the H-distribution. See Shankman et al. 2013, Shankman et al. 2015, or SSimTools.py for a description of the parameters

### Outputs
* detections.dat       - a file containing all of the simulator-detected objects
* tracked.dat	       - a file containing all of the detected objects which were tracked
* drawn.dat 	       - a file containing the first 5000 model-drawn objects


# Survey Characterisations

The folder "ALL" contains the characterisations and pointings for the Canada-France Ecliptic Plane Survey (+ its 2 extensions), 
Alexandersen et al. 2015, and the first quarter dataset of the Outer Solar System Origins Survey (OSSOS).
There are two types of files within this folder:

* \*.eff   	       - characterization files for the given block of a survey. For more documentation, see the readme files in ALL
* pointings.list       - the patches of the sky for each characterised survey block 

The efficiency files and template.eff describe the formats of these files