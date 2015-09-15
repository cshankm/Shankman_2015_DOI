This DOI provides a Survey Simulator as a tool to analyze the observations of Trans-Neptunian Objects (TNOs) from [CFEPS](http://adsabs.harvard.edu/abs/2011AJ....142..131P), [Alexandersen et al. 2015](http://arxiv.org/abs/1411.7953) and [OSSOS](http://www.ossos-survey.org/). This DOI is offered as a companion to Shankman et al. 2015, which analyses the Scattering TNOs from these surveys.

TNO surveys have a number of strong observational biases. In order to meaningfully interpret the observations, these biases must be taken into consideration so that conclusions can be drawn about the intrinsic TNO populations being observed. Each of the above surveys has been carefully characterised and has measured their intrinsic biases. These biases are recorded in the \*.eff files stored in the directory "ALL". The Survey Simulator takes a straightforward approach to handling the observational biases. It is not possible to take the observed population and de-bias them to know what the intrinsic populations is. One simply can't know what they didn't see. Instead, the Survey Simulator takes a model for the intrinsic distribution of objects in the Solar System and applies the survey's known biases. A model is forward biased through the Survey Simulator to produce a set of "Simulated Detections" that can then be compared to the real detected sample. For details on the inner workings of the Survey Simulator, see the following paper:

Jones et al. 2006: [http://adsabs.harvard.edu/abs/2006Icar..185..508J](http://adsabs.harvard.edu/abs/2006Icar..185..508J)

Petit et al. 2011: [http://adsabs.harvard.edu/abs/2011AJ....142..131P](http://adsabs.harvard.edu/abs/2011AJ....142..131P)

Here we provide an implementation of the Survey Simulator to examine the absolute magnitude distribution (H) of the Scattering TNOs. For a detailed description of our methods and statistical techniques, see Shankman et al. 2015. Here we are set-up to forward bias the Kaib et al. 2011 orbital model of scattering objects (q200_scattering_hot_alt1k_aei.dat), with a given H-distribution.

The Survey Simulator was written in Fortran (included here as SurveySubs.f) and has a python wrapper (Driver.py). SurveySubs.f must be compiled on your machine, and then Driver.py can simply be executed with the command "python problem.py". The simulator runs until it has "detected" a specified number of objects, continually drawing test objects from the model until this criteria is satisfied.

There are two files you may immediately want to edit:

num_to_track.txt - this specifies the number of objects the Survey Simulator needs to track
H_dist_vars.txt  - this specifies the parameters of the H-distribution to be tested


#Workflow:

- Driver.py (run this file)
   -> calls GiMiObj to draw model object
      ->  Use ssimTools.py tools
   -> calls the compiled version of SurveySubs.f with an object to check for detection, returns if it was and what it's detected characteristics are
   -> writes outputs


##Driver.py
###Inputs
*input.file	       - a file containing the name of the input orbital model file (essentially the ouptu of "wc -l filename > input.file")
*seeds.txt    	       - a file containing the seed for the simulation
*number_to_track.txt   - a file containing the desired number of tracked objects from the survey simulator
*surveydir.txt 	       - a file contianing the name of the folder containing the survey characterisations 
*H_dist_vars.txt       - a file contianing the parameters of the H-distribution. See Shankman et al. 2015, or SSimTools.py for a description of the parameters

###Outputs
*detections.dat        - a file containing all of the simulator-detected objects
*tracked.dat	       - a file containing all of the detected objects which were tracked
*drawn.dat 	       - a file containing the first 5000 model-drawn objects





#Survey Characterisations

The folder "ALL" contains the characterisations and pointings for CFEPS (+ its 2 extensions), Alexandersen et al. 2015, and the first quarter of OSSOS.
There are two kinds of files:

*\*.eff   	  - the efficiency files for each block of each survey. For more documentation, see the readme files in ALL
*pointings.list   - a list of the patch of the sky for each characterised survey block 

The efficiency files and template.eff describe the format of these files