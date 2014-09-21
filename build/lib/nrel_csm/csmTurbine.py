"""
csmTurbine.py

Created by George Scott on 2012-08-01.
Modified by Katherine Dykes 2012.
Copyright (c) NREL. All rights reserved.
"""

from config import *
from math import *

from csmBlades import csmBlades
from csmHub import csmHub
from csmNacelle import csmNacelle
from csmTower import csmTower
        
#-------------------------------------------------------------------------------

class csmTurbine(object):
    ''' Turbine class 
        inputs are adjusted to be only those needed for mass and cost calculations; these include:
            hubHeight=90.0, machineRating=5000.0, maxTipSpd=80.0, rotorDiam=126.0, dtDesign=1, nblades = 3, maxEfficiency=0.910201, ratedWindSpd=12.0, idepth=1)       
    '''
    def __init__(self):

        """
           Initialize properties for operations and maintenance costs.
        """
        
        # Initialize the components of the turbine
        self.blades  = csmBlades()
        self.hub     = csmHub()    
        self.nac     = csmNacelle()
        self.tower   = csmTower()

        pass
    
    def compute(self, hubHeight=90.0, machineRating=5000.0, maxTipSpd=80.0, rotorDiam=126.0, dtDesign=1, nblades = 3, \
                       maxEfficiency=0.90201, ratedWindSpd = 11.5064, altitude=0.0, thrustCoeff=0.50, seaDepth=20.0, crane=True, advancedBlade = False, \
                       advancedBedplate = 0, advancedTower = False, year = 2009, month = 12):
        """
        Computes the turbine component masses and costs using the NREL Cost and Scaling Model method.
        
        Parameters
        ----------
        hubHeight : float
          hub height [m] of the wind turbines at the site
        machineRating : float
          machine rating [kW] for the wind turbine at the site
        maxTipSpd : float
          maximum allowable tip speed [m/s] for the wind turbine
        rotorDiam : float
          rotor diameter [m] of the wind turbines at the site
        dtDesign : int
          drivetrain design [1 = 3-stage geared, 2 = single-stage, 3 = multi-gen, 4 = direct drive]
        nblades : int
          number of rotor blades
        maxEfficiency : float
          maximum efficiency of the drivetrain
        ratedWindSpd : float
          wind speed at which turbine produced rated power [m/s]
        altitude : float
          altitude [m] of wind farm above sea level for an onshore plant
        seaDepth : float
          sea depth [m] which is 0.0 or negative for an onshore project
        crane : bool
          boolean for the presence of an on-board service crane
        advancedBlade : bool
          boolean for the presence of an advanced wind turbine blade configuration
        advancedBedplate : int
          bedplate design for standard, modular or integrated
        year : int
          project start year [year]
        month : int
          project start month [month]
        
        """

        # input variable assignment
        if seaDepth == 0.0:            # type of plant # 1: Land, 2: < 30m, 3: < 60m, 4: >= 60m
            iDepth = 1
        elif seaDepth < 30:
            iDepth = 2
        elif seaDepth < 60:
            iDepth = 3
        else:
            iDepth = 4

        if (iDepth == 1):   # TODO - crane assignment should be an input
            offshore  = 0  # 0 = onshore
        else:
            offshore  = 1  # 1 = offshore

        # initialize ppi index calculator
        ppi.curr_yr = year
        ppi.curr_mon = month

        # Compute air density (todo: this is redundant from csm AEP, calculation of environmental variables of interest should probably be its own model)        
        ssl_pa     = 101300  # std sea-level pressure in Pa
        gas_const  = 287.15  # gas constant for air in J/kg/K
        gravity    = 9.80665 # standard gravity in m/sec/sec
        lapse_rate = 0.0065  # temp lapse rate in K/m
        ssl_temp   = 288.15  # std sea-level temp in K
        
        airDensity = (ssl_pa * (1-((lapse_rate*(altitude + hubHeight))/ssl_temp))**(gravity/(lapse_rate*gas_const))) / \
            (gas_const*(ssl_temp-lapse_rate*(altitude + hubHeight)))

        # calaculate derivative input parameters for nacelle calculations       # todo - these should come from AEP/rotor module
        ratedHubPower  = machineRating / maxEfficiency 
        rotorSpeed     = (maxTipSpd/(0.5*rotorDiam)) * (60.0 / (2*pi))
        maximumThrust  = airDensity * thrustCoeff * pi * rotorDiam**2. * (ratedWindSpd**2.) / 8.

        rotorTorque = ratedHubPower/(rotorSpeed*(pi/30))*1000   # NREL internal version

        # sub-component computations for mass, cost and dimensions          
        self.blades.compute(rotorDiam,advancedBlade,year,month)
        
        self.hub.compute(self.blades.getMass(), rotorDiam,nblades,year,month)

        self.rotorMass = self.blades.getMass() * nblades + self.hub.getMass()
        self.rotorCost = self.blades.getCost() * nblades + self.hub.getCost()
        
        self.nac.compute(rotorDiam, machineRating, self.rotorMass, rotorSpeed, \
                      maximumThrust, rotorTorque, dtDesign, offshore, \
                      crane, advancedBedplate, year, month)

        self.tower.compute(rotorDiam, hubHeight, advancedTower, year, month)        
        
        self.cost = \
            self.rotorCost + \
            self.nac.cost + \
            self.tower.cost

        self.marCost = 0.0
        if (offshore == 1): # offshore - add marinization - NOTE: includes Foundation cost (not included in CSM.xls)
            marCoeff = 0.10 # 10%
            self.marCost = marCoeff * self.cost
            
        self.cost += self.marCost
            
        self.mass = \
            self.rotorMass + \
            self.nac.mass + \
            self.tower.mass

    def getMass(self):
        """ 
        Provides the overall turbine mass.

        Returns
        -------
        mass : float
            Total mass for wind turbine [kg]
        """

        return self.mass
        
    def getCost(self):
        """ 
        Provides the turbine capital costs for a single turbine.

        Returns
        -------
        cost : float
            Turbine capital costs [USD]
        """

        return self.cost

    def cm_print(self):  # print cost and mass of components
        print 'Turbine Components Costs'       
        print '  Rotor      %9.2f $K %9.2f kg' % (self.rotorCost, self.rotorMass)
        print '  Nacelle    %9.2f $K %9.2f kg' % (self.nac.cost, self.nac.mass)
        print '  Tower      %9.2f $K %9.2f kg' % (self.tower.cost, self.tower.mass)
        print '  Marinization (for offshore) %9.2f $K' % (self.marCost)
        print 'TURBINE TOTAL %9.2f $K %9.2f kg' % (self.cost, self.mass)
        print        

# ------------------------------------------------------------

def example():

    # simple test of module

    ppi.ref_yr   = 2002
    ppi.ref_mon  = 9
    year = 2009
    month = 12
    ppi.curr_yr = year
    ppi.curr_mon = month

    hubHeight = 90.0
    machineRating = 5000.0
    maxTipSpd = 80.0
    rotorDiam = 126.0
    dtDesign = 1
    nblades = 3
    maxEfficiency = 0.90201
    ratedWindSpd = 11.5064
    altitude = 0.0
    thrustCoeff = 0.50
    seaDepth = 20.0
    crane = True
    advancedBlade = True
    advancedBedplate = 0
    advancedTower = False
    
    turb = csmTurbine()
    print "Offshore Configuration 5 MW turbine"
    turb.compute(hubHeight, machineRating, maxTipSpd, rotorDiam, dtDesign, nblades, \
                       maxEfficiency, ratedWindSpd, altitude, thrustCoeff, seaDepth, crane, advancedBlade, \
                       advancedBedplate, advancedTower, year, month)
    turb.cm_print()
    turb.nac.dump()


if __name__ == "__main__":  #TODO - update based on changes to csm Turbine

    example()