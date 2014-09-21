""" 
csmOM.py
    
Created by George Scott 2012
Modified  by Katherine Dykes 2012
Copyright (c)  NREL. All rights reserved.

"""

from config import *

class csmOM(object):
    """ 
    O&M (operations & maintenance) cost module 
        costs are proportional to AEP, with different constants
        for land and offshore
    """
    
    def __init__(self):

        """
           Initialize properties for operations and maintenance costs.
        """
        
    def compute(self, aep, seaDepth, machineRating, year, month):
        """
        Computes the operations and maintenance costs for a wind plant using the NREL Cost and Scaling Model method.
        
        Parameters
        ----------
        aep : float
          annual energy production [kWh]
        seaDepth : float
          sea depth [m] which is 0.0 or negative for an onshore project
        machineRating : float
          machine rating [kW] for the wind turbine at the site
        year : int
          project start year [year]
        month : int
          project start month [month]
        
        """

        # initialize variables
        landCostFactor     = 0.0070  # $/kwH
        offshoreCostFactor = 0.0200  # $/kwH

        # initialize variables
        if seaDepth == 0:
            offshore = 0
        else:
            offshore = 1

        ppi.curr_yr = year
        ppi.curr_mon = month        
        if (offshore == 0):  # kld - place for an error check - iShore should be in 1:4
            self.cost = aep * landCostFactor
            costEscalator = ppi.compute('IPPI_LOM') 
        else:
            self.cost = aep * offshoreCostFactor
            ppi.ref_yr = 2003
            costEscalator = ppi.compute('IPPI_OOM')
            ppi.ref_yr = 2002 

        self.cost *= costEscalator # in $/year

        ''' returns levelized replacement cost ($/yr) '''
        # mR in kW
        # iShore - 1: land-based, 2: shallow, 3: 30-60m, 4: >60m
        
        if (offshore == 0): 
            lrcCF = 10.70 # land based
            costEscFactor = ppi.compute('IPPI_LLR')
        else:
            lrcCF = 17.00 # offshore
            ppi.ref_yr = 2003
            costEscFactor = ppi.compute('IPPI_OLR')
            ppi.ref_yr = 2002 
                
        self.lrc = machineRating * lrcCF * costEscFactor # in $/yr
    
        ''' returns lease cost ($/yr) '''
        # aep in kWh
        # iShore - 1: land-based, 2: shallow, 3: 30-60m, 4: >60m
        
        # in CSM spreadsheet, land and offshore leases cost the same
        if (offshore == 0): 
            leaseCF = 0.00108 # land based
            costEscFactor = ppi.compute('IPPI_LSE')
        else:
            leaseCF = 0.00108 # offshore
            costEscFactor = ppi.compute('IPPI_LSE')

        self.llc = aep * leaseCF * costEscFactor # in $/yr

        pass

    def getOMCost(self):
        """ 
        Provides the operations and maintenance costs for the plant.

        Returns
        -------
        cost : float
            Operations and maintenance costs [USD]
        """

        return self.cost

    def getLLC(self):
        """ 
        Provides the land lease costs costs for the plant.

        Returns
        -------
        llc : float
            Land lease costs [USD]
        """

        return self.llc

    def getLRC(self):
        """ 
        Provides the levelized replacement costs costs for the plant.

        Returns
        -------
        lrc : float
            Levelized replacement costs [USD]
        """

        return self.lrc

#------------------------------------------------------------------

def example():

    # simple test of module
    
    aep = 1701626526.28
    machineRating = 5000.0
    year = 2010
    month = 12
    seaDepth = 20.0
    
    om = csmOM()

    om.compute(aep, seaDepth, machineRating, year, month)

    print 'OM cost offshore   %9.3f LevRep %9.3f Lease %9.3f'  % \
        (om.getOMCost(), om.getLRC(), om.getLLC())
    
    seaDepth = 0.0

    om.compute(aep, seaDepth, machineRating, year, month)

    print 'OM cost offshore   %9.3f LevRep %9.3f Lease %9.3f'  % \
        (om.getOMCost(), om.getLRC(), om.getLLC())

if __name__ == "__main__":

    example()
