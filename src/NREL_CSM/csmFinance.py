"""
csmFin.py

Created by George Scott on 2012-08-01.
Copyright (c) NREL. All rights reserved.
"""

from math import *

#----------------------------------------------------------------------

class csmFinance(object):
    """
    This class is a simplified model used to determine the cost of energy and levelized cost of energy for a wind plant based on the NREL Cost and Scaling Model.   
    """

    def __init__(self):
        """
           Initialize properties for csmFinance
        """
        
    def compute(self, ratedpwr, tcc, om, llc, lrc, bos, aep, fcr, constructionrate, taxrate, discountrate, constructiontime, projlifetime, turbineNum, seaDepth):
        """
        Computes a wind plant cost of energy and levelized cost of energy using the NREL Cost and Scaling Model method.
        
        Parameters
        ----------
        ratedpwr : float
           Wind turbine rated power [kW]
        tcc : float
           Turbine Capital Costs (for entire plant) [USD]
        om : float
           Annual Operations and Maintenance Costs (for entire plant) (USD)
        llc : float
           Annual Land Lease Costs for wind plant [USD]
        lrc : float
           Levelized Replacement Costs (for entire plant) [USD]
        bos : float
           Balance of Station Costs (for entire plant) [USD]
        aep : float
           Annual energy production (for entire plant) [kWh]
        fcr : float
           Fixed charge rate
        constructionrate : float
           Construction financing rate
        taxrate : float
           Project tax rate
        discountrate : float
           Project discount rate
        constructiontime : float
           Time for construction of plant [years]
        projlifetime : float
           Project lifetime [years]
        turbineNum : float
           Number of turbines in plant
        
        """

        if seaDepth > 0.0:
           warrantyPremium = (tcc / 1.10) * 0.15
           icc = tcc + warrantyPremium + bos
        else:
           icc = tcc + bos

        #compute COE and LCOE values
        self.COE = ((icc)* fcr / aep) + (om * (1-taxrate) + llc + lrc) / aep                        
        iccKW = (icc) / (ratedpwr * turbineNum)
        amortFactor = (1 + 0.5*((1+discountrate)**constructiontime-1)) * \
                      ((discountrate)/(1-(1+discountrate)**(-1.0*projlifetime)))
        capFact = aep / (8760 * ratedpwr * turbineNum)
        self.LCOE = (iccKW*amortFactor) / (8760*capFact) + (om/aep)

    def getCOE(self):
        """
        Returns the wind plant cost of energy
        
        Returns
        -------
        COE : float
           Wind Plant Cost of Energy [$/kWh]
        """

        return self.COE

    def getLCOE(self):
        """
        Returns the wind plant levelized cost of energy
        
        Returns
        -------
        LCOE : float
           Wind Plant Levelized Cost of Energy [$/kWh]
        """
        return self.LCOE
        
# --------------------------------------------

def example():
  
    # simple test of module
    
    lcoe = csmFinance()

    ratedpwr = 5000.0
    tcc = 6087803.555
    om = 401819.023
    llc = 22225.395
    lrc = 91048.387
    bos = 7668775.3
    aep = 15756299.843
    fcr = 0.12
    constructionrate = 0.0
    taxrate = 0.4
    discountrate = 0.07
    constructiontime = 1
    projlifetime = 20
    turbineNum = 50
    seaDepth = 20.0

    print "Offshore"
    lcoe.compute(ratedpwr, tcc, om, llc, lrc, bos, aep, \
         fcr, constructionrate, taxrate, discountrate, constructiontime, projlifetime, turbineNum, seaDepth)
    print "LCOE %6.6f" % (lcoe.getLCOE())
    print "COE %6.6f" % (lcoe.getCOE())
    print


if __name__ == "__main__":

    example()