"""
csmBlades.py

Created by George Scott on 2012-08-01.
Modified by Katherine Dykes 2012.
Copyright (c) NREL. All rights reserved.
"""

from config import *

#-------------------------------------------------------------------------------

class csmBlades(object):
    ''' csmBlades class
    
          This class provides a representation of a wind turbine blade.
            
    '''
    
    def __init__(self):
        """
        Initialize the parameters for the wind turbine blade
        
        Parameters
        ----------
        mass : float
          Individual wind turbine blade mass [kg]
        cost : float
          individual wind turbine blade cost [USD]
        """
        
    def compute(self, diam=126.0,advanced=False,curr_yr=2009,curr_mon=9,verbose=0):
        """
        Compute mass and cost for a single wind turbine blade by calling computeMass and computeCost
        
        Parameters
        ----------
        diam : float
          rotor diameter [m] of the turbine
        advanced : bool
          advanced blade configuration boolean
        curr_yr : int
          year of project start
        curr_mon : int
          month of project start
        """
        self.computeMass(diam,advanced)
        
        self.computeCost(diam,advanced,curr_yr,curr_mon)

        if (verbose > 0):
            print '  blade        %6.3f K$  %8.3f kg' % (self.getCost()   , self.getMass())
            print '  blades        %6.3f K$  %8.3f kg' % (self.getCost()*3   , self.getMass()*3)
    
    def computeMass(self,diam,advanced=False):
        """
        Compute mass for a single wind turbine blade using NREL cost and scaling model
        
        Parameters
        ----------
        diam : float
          rotor diameter [m] of the turbine
        advanced : bool
          advanced blade configuration boolean
        """
         
        if (advanced == True):
            massCoeff = 0.4948
            massExp   = 2.5300
        else:
            massCoeff = 0.1452 
            massExp   = 2.9158
        
        self.mass = (massCoeff*(diam/2.0000)**massExp)
      
    def computeCost(self,diam,advanced=False,curr_yr=2009,curr_mon=9):
        """
        Compute cost for a single wind turbine blade using NREL cost and scaling model
        
        Parameters
        ----------
        diam : float
          rotor diameter [m] of the turbine
        advanced : bool
          advanced blade configuration boolean
        curr_yr : int
          year of project start
        curr_mon : int
          month of project start
        """
        ppi.curr_yr = curr_yr
        ppi.curr_mon = curr_mon

        ppi_labor  = ppi.compute('IPPI_BLL')

        if (advanced == True):
            ref_yr = ppi.ref_yr
            ppi.ref_yr = 2003
            ppi_mat   = ppi.compute('IPPI_BLA')
            ppi.ref_yr = ref_yr
            slopeR3   = 0.4019376
            intR3     = -21051.045983
        else:
            ppi_mat   = ppi.compute('IPPI_BLD')
            slopeR3   = 0.4019376
            intR3     = -955.24267
            
        laborCoeff    = 2.7445
        laborExp      = 2.5025
        
        bladeCostCurrent = ( (slopeR3*(diam/2.0000)**3.0000 + (intR3))*ppi_mat + \
                                  (laborCoeff*(diam/2.0000)**laborExp)*ppi_labor    ) / (1.0000-0.2800)
        self.cost = bladeCostCurrent

    def getMass(self):
        """ 
        Provides the mass for the wind turbine blade.

        Returns
        -------
        mass : float
            Wind turbine blade mass [kg]
        """

        return self.mass
        
    def getCost(self):
        """ 
        Provides the cost for the wind turbine blade.

        Returns
        -------
        cost : float
            Wind turbine blade cost [USD]
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
    
    blades = csmBlades()
    print "Conventional blade design:"
    blades.compute(126.0,False,curr_yr, curr_mon, 1)
    print "Advanced blade design:"
    blades.compute(126.0,True,curr_yr, curr_mon, 1)

if __name__ == "__main__":  #TODO - update based on changes to csm Turbine

    example()
