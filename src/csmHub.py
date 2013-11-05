"""
csmHub.py

Created by George Scott on 2012-08-01.
Modified by Katherine Dykes 2012.
Copyright (c) NREL. All rights reserved.
"""

from config import *

#-------------------------------------------------------------------------------

class csmHub(object):
    """ 
    csmHub class 
        
    This class determines the mass and cost for a wind turbine hub based on the NREL cost and scaling model
    
    """
    
    def __init__(self):
      
        """
        Initialize the parameters for csm Hub
        
        Parameters
        ----------
        mass : float
          Individual wind turbine hub system mass [kg]
        cost : float
          individual wind turbine hub system cost [USD]
        hubMass : float
          mass of hub [kg]
        spinnerMass : float
          mass of spinner / nose cone [kg]
        pitchSysMass : float
          mass of pitch system including bearings [kg]
        hubCost : float
          cost of hub [USD]
        spinnerCost : float
          cost of spinner / nose cone [USD]
        pitchSysCost : float
          cost of pitch system including bearings [USD]
        """
        
    def compute(self, blademass, diam=126.0,nblades=3,curr_yr=2009,curr_mon=9,verbose=0):
        """
        Compute mass and cost for the hub system by calling computeMass and computeCost
        
        Parameters
        ----------
        blademass : float
          mass [kg] of a single blade for the wind turbine
        diam : float
          rotor diameter [m] of the turbine
        nblades : int
          number of wind turbine blades
        curr_yr : int
          year of project start
        curr_mon : int
          month of project start
        """
        self.computeMass(blademass, diam, nblades)
        
        self.computeCost(diam, curr_yr, curr_mon, self.hubMass, self.spinnerMass)

        if (verbose > 0):
            print "Hub System Components"
            print '  hub           %6.3f K$  %8.3f kg' % (self.hubCost      , self.hubMass          )
            print '  pitch mech    %6.3f K$  %8.3f kg' % (self.pitchMechCost, self.pitchSysMass     )
            print '  nose cone     %6.3f K$  %8.3f kg' % (self.spinnerCost  , self.spinnerMass     )
            print '  hub total     %6.3f K$  %8.3f kg' % (self.cost         , self.mass     )           
           
    def computeMass(self, blademass, diam=126.0, nblades=3):
        """
        Compute mass for the hub system based on NREL Cost and Scaling Model
        
        Parameters
        ----------
        blademass : float
          mass [kg] of a single blade for the wind turbine
        diam : float
          rotor diameter [m] of the turbine
        nblades : int
          number of wind turbine blades
        """

        #*** Pitch bearing and mechanism
        pitchBearingMass = 0.1295 * blademass*nblades + 491.31  # slope*BldMass3 + int
        bearingHousingPct = 32.80 / 100.0
        massSysOffset = 555.0
        self.pitchSysMass = pitchBearingMass * (1+bearingHousingPct) + massSysOffset
    
        #*** Hub
        self.hubMass = 0.95402537 * blademass + 5680.272238
    
        #*** NoseCone/Spinner
        self.spinnerMass = 18.5*diam+(-520.5)   # GNS

        self.mass = self.hubMass + self.pitchSysMass + self.spinnerMass
    
    def computeCost(self,diam=126.0,curr_yr=2009,curr_mon=9,hubMass=0.0, spinnerMass=0.0):
        """
        Compute cost for the hub system by the NREL Cost and Scaling Model
        
        Parameters
        ----------
        diam : float
          rotor diameter [m] of the turbine
        curr_yr : int
          year of project start
        curr_mon : int
          month of project start
        hubMass : float
          mass [kg] of the wind turbine hub component
        spinnerMass : float
          mass [kg] of the wind turbine spinner / nose cone component
        """        
        ppi.curr_yr = curr_yr
        ppi.curr_mon = curr_mon

        #*** Pitch bearing and mechanism    
        bearingCost = (0.2106*diam**2.6576)
        bearingCostEscalator = ppi.compute('IPPI_PMB')
        self.pitchMechCost = bearingCostEscalator * ( bearingCost + bearingCost * 1.28 )
    
        #*** Hub
        if hubMass == 0.0:
          hubCost2002 = hubMass * 4.25 # $/kg
        else:
          hubCost2002 = hubMass * 4.25 # $/kg         
        hubCostEscalator = ppi.compute('IPPI_HUB')
        self.hubCost = hubCost2002 * hubCostEscalator
    
        #*** NoseCone/Spinner
        if spinnerMass == 0.0:
          spinnerCostEscalator = ppi.compute('IPPI_NAC')
          self.spinnerCost = spinnerCostEscalator * (5.57*spinnerMass)
        else:
          spinnerCostEscalator = ppi.compute('IPPI_NAC')
          self.spinnerCost = spinnerCostEscalator * (5.57*spinnerMass)         

        self.cost = self.hubCost + self.pitchMechCost + self.spinnerCost

    def getMass(self):
        """ 
        Provides the overall hub system mass.

        Returns
        -------
        mass : float
            Hub System mass [kg]
        """

        return self.mass
        
    def getCost(self):
        """ 
        Provides the overall hub system cost.

        Returns
        -------
        cost : float
            Hub system cost [USD]
        """

        return self.cost
        
    def getHubComponentMasses(self):
        """ 
        Provides the detail on hub system component masses.

        Returns
        -------
        detailedMasses : array_like of float
            Hub System component masses: hub, pitch system, spinner [kg]
        """     
        
        self.detailedMasses = [self.hubMass, self.pitchSysMass, self.spinnerMass]
        
        return self.detailedMasses
    
    def getHubComponentCosts(self):
        """ 
        Provides the overall hub system cost.

        Returns
        -------
        detailedCosts : float
            Hub system component costs: hub, pitch system, spinner [USD]
        """
        
        self.detailedCosts = [self.hubCost, self.pitchMechCost, self.spinnerCost]     
        
        return self.detailedCosts
        
#-------------------------------------------------------------------------------        

def example():

    # simple test of module
    
    ppi.ref_yr   = 2002
    ppi.ref_mon  = 9
    curr_yr = 2009
    curr_mon = 12
    ppi.curr_yr = curr_yr
    ppi.curr_mon = curr_mon
    
    hub = csmHub()
    blademass = 25614.377
    rotorDiam = 126.0
    nblades = 3
    hub.compute(blademass, rotorDiam, nblades, curr_yr, curr_mon, 1)

if __name__ == "__main__":

   example()
