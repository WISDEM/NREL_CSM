""" 
csmPowerCurve.py
    
Created by George Scott 2012
Modified  by Katherine Dykes 2012
Copyright (c)  NREL. All rights reserved.

"""

from config import *
from csmFoundation import csmFoundation

class csmBOS:

    """ NREL Cost and Scaling Balance of Station cost model. """
 
    def __init__(self):
        """
           Initialize properties for balance of plant costs including default inputs
        """
        
        self.fdn = csmFoundation()
        self.transportation = 0.0
        self.roadsCivil     = 0.0
        self.portStaging    = 0.0
        self.installation   = 0.0
        self.electrical     = 0.0
        self.engPermits     = 0.0
        self.pai            = 0.0
        self.scour          = 0.0
        
    def compute(self,seaDepth,machineRating,hubHt,rtrDiam,tcc, year, month,verbose=0.0):
        """
        Computes the balance of station costs for a wind plant using the NREL Cost and Scaling Model method.
        
        Parameters
        ----------
        seaDepth : float
          sea depth [m] which is 0.0 or negative for an onshore project
        machineRating : float
          machine rating [kW] for the wind turbine at the site
        hubHt : float
          hub height [m] of the wind turbines at the site
        rtrDiam : float
          rotor diameter [m] of the wind turbines at the site
        tcc : float
          turbine capital costs [USD] for a single wind turbine in the project
        year : int
          project start year [year]
        month : int
          project start month [month]
        
        """

        lPrmtsCostCoeff1 = 9.94E-04 
        lPrmtsCostCoeff2 = 20.31 
        oPrmtsCostFactor = 37.0 # $/kW (2003)
        scourCostFactor =  55.0 # $/kW (2003)
        ptstgCostFactor =  20.0 # $/kW (2003)
        ossElCostFactor = 260.0 # $/kW (2003) shallow
        ostElCostFactor = 290.0 # $/kW (2003) transitional
        ostSTransFactor  =  25.0 # $/kW (2003)
        ostTTransFactor  =  77.0 # $/kW (2003)
        osInstallFactor  = 100.0 # $/kW (2003) shallow & trans
        suppInstallFactor = 330.0 # $/kW (2003) trans additional
        paiCost         = 60000.0 # per turbine
        
        suretyBRate     = 0.03  # 3% of ICC
        suretyBond      = 0.0

        #set variables
        if seaDepth == 0:            # type of plant # 1: Land, 2: < 30m, 3: < 60m, 4: >= 60m
            iDepth = 1
        elif seaDepth < 30:
            iDepth = 2
        elif seaDepth < 60:
            iDepth = 3
        else:
            iDepth = 4

        # foundation cost calculations
        self.fdn.compute(machineRating, hubHt, rtrDiam, seaDepth, year, month)

        # initialize self.ppi index calculator
        if iDepth == 1:
            ref_yr  = 2002                   
            ref_mon =    9
        else:
            ref_yr = 2003
            ref_mon = 9
        ppi.ref_yr = ref_yr
        ppi.ref_mon = ref_mon
        ppi.curr_yr = year
        ppi.curr_mon = month
        
        # cost calculations
        tpC1  =0.00001581
        tpC2  =-0.0375
        tpInt =54.7
        tFact = tpC1*machineRating*machineRating + tpC2*machineRating + tpInt   

        if (iDepth == 1):
            self.engPermits  = (lPrmtsCostCoeff1 * machineRating * machineRating) + \
                               (lPrmtsCostCoeff2 * machineRating)
            ppi.ref_mon = 3
            self.engPermits *= ppi.compute('IPPI_LPM') 
            ppi.ref_mon = 9
            
            elC1  = 3.49E-06
            elC2  = -0.0221
            elInt = 109.7
            eFact = elC1*machineRating*machineRating + elC2*machineRating + elInt
            self.electrical = machineRating * eFact * ppi.compute('IPPI_LEL')
            
            rcC1  = 2.17E-06
            rcC2  = -0.0145
            rcInt =69.54
            rFact = rcC1*machineRating*machineRating + rcC2*machineRating + rcInt
            self.roadsCivil = machineRating * rFact * ppi.compute('IPPI_RDC')
             
            iCoeff = 1.965
            iExp   = 1.1736
            self.installation = iCoeff * ((hubHt*rtrDiam)**iExp) * ppi.compute('IPPI_LAI')
          
            self.transportation = machineRating * tFact * ppi.compute('IPPI_TPT')
             
            pass
        elif (iDepth == 2):  # offshore shallow
            self.pai            = paiCost * ppi.compute('IPPI_PAE')
            self.portStaging    = ptstgCostFactor  * machineRating * ppi.compute('IPPI_STP') # 1.415538133
            self.engPermits     = oPrmtsCostFactor * machineRating * ppi.compute('IPPI_OPM')
            self.scour          = scourCostFactor  * machineRating * ppi.compute('IPPI_STP') # 1.415538133#
            self.installation   = osInstallFactor  * machineRating * ppi.compute('IPPI_OAI')            
            self.electrical     = ossElCostFactor  * machineRating * ppi.compute('IPPI_OEL')
            ppi.ref_yr  = 2002                   
            self.transportation = machineRating * tFact * ppi.compute('IPPI_TPT')
            ppi.ref_yr = 2003

            pass 
        elif (iDepth == 3):  # offshore transitional depth
            self.turbInstall   = osInstallFactor  * machineRating * ppi.compute('IPPI_OAI')
            self.supportInstall = suppInstallFactor * machineRating * ppi.compute('IPPI_OAI')
            self.installation = self.turbInstall + self.supportInstall
            self.pai            = paiCost                          * ppi.compute('IPPI_PAE')
            self.electrical     = ostElCostFactor  * machineRating * ppi.compute('IPPI_OEL')
            self.portStaging    = ptstgCostFactor  * machineRating * ppi.compute('IPPI_STP')
            self.engPermits     = oPrmtsCostFactor * machineRating * ppi.compute('IPPI_OPM')
            self.scour          = scourCostFactor  * machineRating * ppi.compute('IPPI_STP')
            ppi.ref_yr  = 2002
            self.turbTrans           = ostTTransFactor  * machineRating * ppi.compute('IPPI_TPT') 
            ppi.ref_yr = 2003
            self.supportTrans        = ostSTransFactor  * machineRating * ppi.compute('IPPI_OAI') 
            self.transportation = self.turbTrans + self.supportTrans
            
        elif (iDepth == 4):  # offshore deep
            print "\ncsmBOS: Add costCat 4 code\n\n"
            pass
       
        self.cost = self.fdn.getCost() + \
                    self.transportation + \
                    self.roadsCivil     + \
                    self.portStaging    + \
                    self.installation   + \
                    self.electrical     + \
                    self.engPermits     + \
                    self.pai            + \
                    self.scour       

        if (iDepth > 1):
            self.suretyBond = suretyBRate * (tcc + self.cost)
            self.cost = self.cost + self.suretyBond 

        if (verbose > 0):
            self.dump()

    def getCost(self):
        """ 
        Provides the overall balance of station costs for the plant.

        Returns
        -------
        cost : float
            Balance of plant costs [USD]
        """
        
        return self.cost

    def getDetailedCosts(self):
        """ 
        Provides the detailed balance of station costs for the plant.

        Returns
        -------
        detailedCosts : array_like of float
            Balance of plant costs [USD] broken down into components: foundation, transporation, roads & civil,
            ports and staging, installation and assembly, electrical, permits, miscenalleous, scour, surety bond
        """
        self.detailedCosts = [self.fdn.getCost(), self.transportation, self.roadsCivil, self.portStaging, self.installation, \
                self.electrical, self.engPermits, self.pai, self.scour, self.suretyBond] 
        
        return self.detailedCosts 
 
    def dump(self):
        print
        print "BOS: "
        print "  foundation     %8.3f $" % self.fdn.getCost()
        print "  transportation %8.3f $" % self.transportation 
        print "  roadsCivil     %8.3f $" % self.roadsCivil     
        print "  portStaging    %8.3f $" % self.portStaging    
        print "  installation   %8.3f $" % self.installation   
        print "  electrical     %8.3f $" % self.electrical     
        print "  engPermits     %8.3f $" % self.engPermits     
        print "  pai            %8.3f $" % self.pai            
        print "  scour          %8.3f $" % self.scour       
        print "TOTAL            %8.3f $" % self.cost       
        print "  surety bond    %8.3f $" % self.suretyBond       
        print
    
#------------------------------------------------------------------

def example():
  
    # simple test of module
    
    bos = csmBOS()
    
    seaDepth = 20.0
    machineRating = 5000.0
    hubHt = 90.0
    rtrDiam = 126.0
    year = 2009
    month = 12
    tcc = 6087803.555
    
    bos.compute(seaDepth,machineRating,hubHt,rtrDiam,tcc, year, month, 1)
    
    print 'BOS cost offshore   %9.3f '          % bos.getCost()    
    
if __name__ == "__main__":

    example()

#------------------------------------------------------------------