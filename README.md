NREL_CSM is a set of models for assessing overall wind plant cost of energy (coe).  The models use wind turbine and plant cost and energy production information as well as several financial parameters in simple equations to estimate coe.

This code is based on the NREL Wind Turbine Cost and Scaling Model which was published in a report in 2006.  The contents of the model have been incorporated into the WISDEM OpenMDAO software but the raw python version of the model is provided here.  This raw python version of the model (NREL_CSM) will not be maintained going forward and users are encouraged to use the version in [WISDEM](http://github.com/WISDEM) for cost analysis work.

Author:
[K. Dykes](mailto:katherine.dykes@nrel.gov) and
[G. Scott](mailto:george.scott@nrel.gov)

## Detailed Documentation

Online documentation is available at <http://wisdem.github.io/NREL_CSM/>

## Prerequisites

NumPy, SciPy

## Installation

Install NREL_CSM using standard python commands:

	$ python setup.py install

## Check Installation

To check if installation was successful try to import the module

	$ python
	> import NREL_CSM.csm

For software issues please use <https://github.com/WISDEM/NREL_CSM/issues>.  For functionality and theory related questions and comments please use the NWTC forum for [Systems Engineering Software Questions](https://wind.nrel.gov/forum/wind/viewtopic.php?f=34&t=1002).