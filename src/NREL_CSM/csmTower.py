"""
csmTower.py

Created by George Scott on 2012-08-01.
Modified by Katherine Dykes 2012.
Copyright (c) NREL. All rights reserved.
"""

from config import *
from math import *

#-------------------------------------------------------------------------------        

class csmTower(object):  # TODO: advanced tower not included here
    ''' Tower class 
          twr = csmTower()
          twr.compute(rotorDiam,hubHt[curr_yr,curr_mon,verbose]) : computes twr.mass, twr.cost
    '''
    
    def __init__(self):
        """
        Initialize the parameters for the wind turbine tower

        """
        
    def compute(self, RotorDiam, HubHeight, Advanced=False, curr_yr=2009, curr_mon=12, verbose=0):
        """
        Compute mass and cost for a wind turbine tower by calling computeMass and computeCost
        
        Parameters
        ----------
        RotorDiam : float
          rotor diameter [m] of the turbine
        HubHeight : float
          hub height [m] of the turbine
        curr_yr : int
          year of project start
        curr_mon : int
          month of project start
        """

        self.computeMass(RotorDiam, HubHeight, Advanced)
        
        self.computeCost(curr_yr, curr_mon)
        
        if verbose > 0:
          
          print "Tower Mass: {0}".format(self.mass)
          print "Tower Cost: {0}".format(self.cost)
      
    def computeMass(self,RotorDiam, HubHeight, Advanced):
        """
        Compute mass for a wind turbine tower using the NREL Cost and Scaling Model
        
        Parameters
        ----------
        RotorDiam : float
          rotor diameter [m] of the turbine
        HubHeight : float
          hub height [m] of the turbine
        """

        windpactMassSlope = 0.397251147546925
        windpactMassInt   = -1414.381881
        
        if Advanced:
           windpactMassSlope = 0.269380169
           windpactMassInt = 1779.328183


        self.mass = windpactMassSlope * pi * (RotorDiam/2.)**2 * HubHeight + windpactMassInt
    
    def computeCost(self,curr_yr, curr_mon, towerMass=0.0):
        """
        Compute cost for a wind turbine tower by calling computeMass and computeCost
        
        Parameters
        ----------
        curr_yr : int
          year of project start
        curr_mon : int
          month of project start
        towerMass : float
          mass [kg] of the wind turbine tower
        """

        ppi.curr_yr = curr_yr
        ppi.curr_mon = curr_mon

        twrCostEscalator  = 1.5944
        twrCostEscalator  = ppi.compute('IPPI_TWR')
        
        twrCostCoeff      = 1.5 # $/kg    
        
        if towerMass == 0.0:
          self.towerCost2002 = self.mass * twrCostCoeff  
        else:
          self.towerCost2002 = towerMass * twrCostCoeff               
        self.cost = self.towerCost2002 * twrCostEscalator

    def getMass(self):
        """ 
        Provides the mass for the wind turbine tower.

        Returns
        -------
        mass : float
            Wind turbine tower mass [kg]
        """

        return self.mass
        
    def getCost(self):
        """ 
        Provides the cost for the wind turbine tower.

        Returns
        -------
        cost : float
            Wind turbine tower cost [USD]
        """

        return self.cost
        
#-------------------------------------------------------------------------------       

def example():

    # simple test of module
    
    ppi.ref_yr   = 2002
    ppi.ref_mon  = 9
    curr_yr  = 2009
    curr_mon = 12
    ppi.curr_yr = curr_yr
    ppi.curr_mon = curr_mon
    
    twrsub = csmTower()
    
    rotorDiameter = 126.0
    hubHeight = 90.0
    advanced = False
    
    twrsub.compute(rotorDiameter, hubHeight, advanced, curr_yr, curr_mon, 1)

if __name__ == "__main__":  

    example()
