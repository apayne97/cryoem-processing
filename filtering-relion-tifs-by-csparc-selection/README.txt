Written by Alex Payne, 20220505

In this directory contains the python command required to use a csparc particle file to filter out unused micrographs from a relion movies.star file.

This python script expects that you have already converted a particles.cs file into a particles.star file using csparc2star.py.

in order to run this python script, you should first run this:
source ~/.bashrc
conda activate clean

You can use the -h flag to learn more about the options:
python select-csparc-particles.py -h

And then here is an example of running the script:

(clean) hiter@HiteGPU1:~/testing-csparc-selection$ python select-csparc-particles.py /mnt/raid1/MCM-DDK/20220328/P23/J169/cryosparc_P23_J169_007_particles.star -r /mnt/raid1/MCM-DDK/20220328/Import/job002/movies.star
Loading /mnt/raid1/MCM-DDK/20220328/P23/J169/cryosparc_P23_J169_007_particles.star...
Removing these lines as header:
	 data_optics
	 loop_
	 _rlnVoltage #1
	 _rlnImagePixelSize #2
	 _rlnSphericalAberration #3
	 _rlnAmplitudeContrast #4
	 _rlnOpticsGroup #5
	 _rlnImageSize #6
	 _rlnImageDimensionality #7
	 300.000000 0.826000 2.700000 0.100000 2 384 2
	 data_particles
	 loop_
	 _rlnImageName #1
	 _rlnMicrographName #2
	 _rlnCoordinateX #3
	 _rlnCoordinateY #4
	 _rlnAngleRot #5
	 _rlnAngleTilt #6
	 _rlnAnglePsi #7
	 _rlnOriginXAngst #8
	 _rlnOriginYAngst #9
	 _rlnDefocusU #10
	 _rlnDefocusV #11
	 _rlnDefocusAngle #12
	 _rlnPhaseShift #13
	 _rlnCtfBfactor #14
	 _rlnOpticsGroup #15
	 _rlnRandomSubset #16
	 _rlnClassNumber #17
702491 particles found
2454 unique micrographs found
Printing first line after being processed...
['20220328-Elg1-RFC-PCNA-dS', '366', '0013', 'patch', 'aligned', 'doseweighted.mrc']
Found these datasets:
20220328-Elg1-RFC-PCNA-dS
Successfully found paths to relion movies for these datasets:
20220328-Elg1-RFC-PCNA-dS:	/mnt/raid1/MCM-DDK/20220328/Import/job002/movies.star
Selecting micrographs from 20220328-Elg1-RFC-PCNA-dS
Loading data from "/mnt/raid1/MCM-DDK/20220328/Import/job002/movies.star" to be filtered into "20220328-Elg1-RFC-PCNA-dS_movies_subset.star"...
Copying these lines as header:
	 # version 30001
	 data_optics
	 loop_
	 _rlnOpticsGroupName #1
	 _rlnOpticsGroup #2
	 _rlnMicrographOriginalPixelSize #3
	 _rlnVoltage #4
	 _rlnSphericalAberration #5
	 _rlnAmplitudeContrast #6
	 opticsGroup1            1     0.413000   300.000000     2.700000     0.100000
	 # version 30001
	 data_movies
	 loop_
	 _rlnMicrographMovieName #1
	 _rlnOpticsGroup #2
20220328-Elg1-RFC-PCNA-dS: 4301 --> 2454 micrographs, 1847 removed

Congratulations! You have removed a total of 1847 micrographs from your dataset.

IMPORTANT: Make sure to check that the numbers line up, and make sure that the headers are correctly parsed.
You may have to adjust the header cutoffs.
Run this function with only the flag '-h' to see how.
 


