# csmpy
# 2012 01 16

""" 
csmAEP.py
    
Created by George Scott 2012
Modified  by Katherine Dykes 2012
Copyright (c)  NREL. All rights reserved.

"""
    
from math import *
import numpy as np

class csmAEP:

    def __init__(self):

        pass

    #--------------------
            
    def compute(self,powercurve, ratedPower=5000.0, hubHt=90.0, shearExp=0.143,ws50m=8.25,weibullK=2.4, \
                soilingLosses = 0.0, arrayLosses = 0.10, availability = 0.95):
        ''' 
        Computes annual energy production from a wind plant
        
        Parameters
        ----------
        powercurve : array_like of float
          power curve for a turbine (power output [kW] by wind speed [m/s])
        ratedPower : float
          wind turbine rated power [kW]
        hubHt : float
          wind turbine hub height [m]
        shearExp : float
          wind plant site shear exponent
        ws50m : float
          annual average 50 m wind speed [m/s]
        weibullK : float
          wind plant weibull shape factor
        soilingLosses : float
          percent losses due to blade soiling
        arrayLosses : float
          percent losses due to turbine interactions
        availability : float
          annual availability for overall wind plant

        ''' 
           
        
        # compute other model inputs
        hubHeightWindSpeed = ((hubHt/50)**shearExp)*ws50m
        K = weibullK
        L = hubHeightWindSpeed / exp(log(gamma(1.+1./weibullK)))
        turbine_energy = 0.0
        for i in xrange(0,powercurve.shape[1]):
           X = powercurve[0,i]
           result = powercurve[1,i] * weibull(X, weibullK, L)
           #print [X, self.weibullK, L, self.powerCurve[1,i],result] # remove when not testing
           turbine_energy += result
        
        # determine aep after losses from soiling, availability and turbine wake
        aep_turbine_energy = turbine_energy
        aep_turbine_energy *= (1.0-soilingLosses)
        aep_turbine_energy *= (1.0-arrayLosses)
        aep_turbine_energy *= (availability * 8760.0)  # 8760hrs/yr
        ws_inc = powercurve[0,1] - powercurve[0,0]
        aep_turbine_energy *= ws_inc # adjust for bin size not equal to 1.0
        self.aep = aep_turbine_energy
        
        # determine capacity factor
        self.capFact = aep_turbine_energy / (ratedPower * 8760)   # return power in kWh

        pass

    #--------------------

    def getAEP(self):
        """ 
        Returns annual energy production for the project.

        Returns
        -------
        aep : float
            Annual energy production [kWh]
        """        
        return self.aep
        
    #--------------------
            
    def getCapacityFactor(self):
        """ 
        Returns project capacity factor.

        Returns
        -------
        capFact : float
            Project capacity factor (unitless)
        """      
        return self.capFact

#-----------------------------------------------------------------

def weibull(X,K,L):
    ''' 
    Return Weibull probability at speed X for distribution with k=K, c=L 
    
    Parameters
    ----------
    X : float
       wind speed of interest [m/s]
    K : float
       Weibull shape factor for site
    L : float
       Weibull scale factor for site [m/s]
       
    Returns
    -------
    w : float
      Weibull pdf value
    '''
    w = (K/L) * ((X/L)**(K-1)) * exp(-((X/L)**K))
    return w

#------------------------------------------------------------------

def example():

    # simple test of module
    
    aep = csmAEP()
    from csmPowerCurve import csmPowerCurve
    from csmDriveEfficiency import DrivetrainEfficiencyModel, csmDriveEfficiency
    drivetrain = csmDriveEfficiency(1)
    pcurve = csmPowerCurve()
    pcurve.compute(drivetrain)
    powercurve = np.array(pcurve.powerCurve)

    # initialize input parameters
    powercurve = np.array([[0.0, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, \
                           11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 17.0, 18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 24.0, 25.0, 26.0], \
                          [0.0, 0.0, 0.0, 0.0, 187.0, 350.0, 658.30, 1087.4, 1658.3, 2391.5, 3307.0, \
                          4415.70, 5000.0, 5000.0, 5000.0, 5000.0, 5000.0, 5000.0, 5000.0, 5000.0, 5000.0, 5000.0, \
                          5000.0, 5000.0, 5000.0, 5000.0, 0.0]])
    ratedPower=5000.0
    hubHt    = 90.0
    shearExp = 0.1
    ws50m    = 8.02
    weibullK = 2.15
    altitude = 0.0        
    soilingLosses = 0.0
    arrayLosses   = 0.10
    availability  = 0.941    

    aep.compute(powercurve, ratedPower, hubHt, shearExp, ws50m, weibullK, \
                soilingLosses, arrayLosses, availability)

    print 'AEP per turbine: %9.3f MWh (for Rated Power: %6.1f)'   % (aep.getAEP(), ratedPower)
    print 'CapFactor:  %9.3f %% '          % (aep.getCapacityFactor()*100.0)
    print 'Power Curve:'
    print powercurve

if __name__ == "__main__":

    example()
