# NREL_CSM

The NREL Cost and Scaling Model (NREL_CSM) is a set of models for assessing overall wind plant cost of energy (coe).  The models use wind turbine and plant cost and energy production information as well as several financial parameters in simple equations to estimate coe.

This code is based on the NREL Wind Turbine Cost and Scaling Model which was published in a report in 2006.  The contents of the model have been incorporated into the WISDEM OpenMDAO software but the raw python version of the model is provided here.  This raw python version of the model (NREL_CSM) will not be maintained going forward and users are encouraged to use the version in [Turbine_CostsSE](http://github.com/Turbine_CostsSE) for cost analysis work.

Author: [NREL WISDEM Team](mailto:systems.engineering@nrel.gov) 

## Documentation

See local documentation in the `docs`-directory or access the online version at <http://wisdem.github.io/NREL_CSM/>

## Installation

For detailed installation instructions of WISDEM modules see <https://github.com/WISDEM/WISDEM> or to install NREL_CSM by itself do:

    $ python setup.py install

## Check Installation

To check if installation was successful try to import the module

	$ python
	> import NREL_CSM.csm

For software issues please use <https://github.com/WISDEM/NREL_CSM/issues>.  For functionality and theory related questions and comments please use the NWTC forum for [Systems Engineering Software Questions](https://wind.nrel.gov/forum/wind/viewtopic.php?f=34&t=1002).
