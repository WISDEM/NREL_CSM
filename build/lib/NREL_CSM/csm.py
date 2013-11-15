"""
csm.py

Created by George Scott on 2012-08-01.
Modified by Katherine Dykes 2012.
Copyright (c) NREL. All rights reserved.
"""

from csmTurbine import csmTurbine
from csmAEP import csmAEP
from csmPowerCurve import csmPowerCurve
from csmDriveEfficiency import DrivetrainEfficiencyModel, csmDriveEfficiency
from csmBOS import csmBOS
from csmOM import csmOM
from csmFinance import csmFinance

from math import *
import numpy as np
from config import *

class csm(object):

    """
    Integrating class for all the NREL Cost and Scaling Model
    """

    def __init__(self, drivetrainDesign=1):
        
        self.turb = csmTurbine()
        self.aep = csmAEP()
        self.powerCurve = csmPowerCurve()
        self.drivetrain = csmDriveEfficiency(drivetrainDesign)
        self.bos = csmBOS()
        self.om = csmOM()
        self.fin = csmFinance()
        print "initialization done"

    def compute(self, hubHeight, ratedPower, maxTipSpd, rotorDiam, dtDesign, nblades, \
                       altitude, thrustCoeff, seaDepth, crane, advancedBlade, \
                       advancedBedplate, advancedTower, year, month, maxCp, maxTipSpdRatio, cutInWS, cutOutWS, \
                       airDensity,shearExp,ws50m,weibullK, \
                       soilingLosses, arrayLosses, availability, \
                       fcr, constructionrate, taxrate, discountrate, \
                       constructiontime, projlifetime, turbineNum):

        self.powerCurve.compute(self.drivetrain, hubHeight, ratedPower,maxTipSpd,rotorDiam,  \
                   maxCp, maxTipSpdRatio, cutInWS, cutOutWS, \
                   altitude, airDensity)
        print "powercurve done"
        self.powercurve = np.array(self.powerCurve.powerCurve)
  
        self.aep.compute(self.powercurve, ratedPower, hubHeight, shearExp,ws50m,weibullK, \
                  soilingLosses, arrayLosses, availability)
        print "aep done"
      
        self.turb.compute(hubHeight, ratedPower, maxTipSpd, rotorDiam, dtDesign, nblades, \
                         self.drivetrain.getMaxEfficiency(), self.powerCurve.ratedWindSpeed, altitude, thrustCoeff, seaDepth, crane, advancedBlade, \
                         advancedBedplate, advancedTower, year, month)
        print "turb done"

        self.bos.compute(seaDepth,ratedPower,hubHeight,rotorDiam,self.turb.cost, year, month)
        print "bos done"
        self.om.compute(self.aep.aep, seaDepth, ratedPower, year, month)
        print "om done"
        self.fin.compute(ratedPower, self.turb.cost, self.om.cost, self.om.llc, self.om.lrc, \
                 self.bos.cost, self.aep.aep, fcr, constructionrate, taxrate, discountrate, \
                 constructiontime, projlifetime, turbineNum, seaDepth)
        print "fin done"

def example():

    ppi.curr_yr  = 2009
    ppi.curr_mon = 12

    #Default Cost and Scaling Model inputs for 5 MW turbine (onshore)    
    hubHeight=90.0
    ratedPower=5000.0
    maxTipSpd=80.0
    rotorDiam=126.0
    dtDesign=1
    nblades = 3
    altitude=0.0
    thrustCoeff=0.50
    seaDepth=20.0
    crane=True
    advancedBlade = True
    advancedBedplate = 0
    advancedTower = False
    year = 2009
    month = 12
    maxCp=0.488
    maxTipSpdRatio = 7.525
    cutInWS = 3.0
    cutOutWS = 25.0
    airDensity = 0.0
    shearExp=0.1
    ws50m=8.02
    weibullK=2.15
    soilingLosses = 0.0
    arrayLosses = 0.10
    availability = 0.941
    fcr = 0.12
    constructionrate = 0.0
    taxrate = 0.4
    discountrate = 0.07
    constructiontime = 1
    projlifetime = 20
    turbineNum = 100
    
    csmtest = csm(dtDesign)
    csmtest.compute(hubHeight, ratedPower, maxTipSpd, rotorDiam, dtDesign, nblades, \
                       altitude, thrustCoeff, seaDepth, crane, advancedBlade, \
                       advancedBedplate, advancedTower, year, month, maxCp, maxTipSpdRatio, cutInWS, cutOutWS, \
                       airDensity,shearExp,ws50m,weibullK, \
                       soilingLosses, arrayLosses, availability, \
                       fcr, constructionrate, taxrate, discountrate, \
                       constructiontime, projlifetime, turbineNum)
           
    print "%9.8f" % (csmtest.fin.LCOE)
    print "%9.8f"%(csmtest.fin.COE)
    print "%9.5f"%(csmtest.aep.aep / 1000.0)
    print "%9.5f"%(csmtest.bos.cost / 1000.0)
    print "%9.5f"%(csmtest.turb.cost / 1000.0)
    print "%9.5f"%(csmtest.om.cost / 1000.0)
    print
    csmtest.turb.cm_print()
    csmtest.turb.nac.dump()
#
#    end = 2007
#    step = 1
#    while (year <= end):
#        csmtest.compute(hubHeight, ratedPower, maxTipSpd, rotorDiam, dtDesign, nblades, \
#                           maxEfficiency, ratedWindSpd, altitude, thrustCoeff, seaDepth, crane, advancedBlade, \
#                           advancedBedplate, year, month, maxCp, maxTipSpdRatio, cutInWS, cutOutWS, \
#                           airDensity,shearExp,ws50m,weibullK, \
#                           soilingLosses, arrayLosses, availability, \
#                           fcr, constructionrate, taxrate, discountrate, \
#                           constructiontime, projlifetime, turbineNum)
#                           
#
#        print year            
#        print "%9.5f" % (csmtest.fin.LCOE)
#        print "%9.5f"%(csmtest.fin.COE)
#        print "%9.5f"%(csmtest.aep.aep / 1000.0)
#        print "%9.5f"%(csmtest.bos.cost / 1000.0)
#        print "%9.5f"%(csmtest.turb.cost / 1000.0)
#        print "%9.5f"%(csmtest.om.cost / 1000.0)
#        print
#        year += step  


    # print "%9.5f"%(csmtest.aep.getCapacityFactor())
    # print
    
   # print "Rotor Cost: {0}".format(csmtest.turb.rotorCost)
   # print "Rotor Mass: {0}".format(csmtest.turb.rotorMass)
   # print "Blade Cost *3: {0}".format(csmtest.turb.blades.getCost()*3.0)
   # print "Blade Mass *3: {0}".format(csmtest.turb.blades.getMass()*3.0)
   # print "Hub Cost: {0}".format(csmtest.turb.hub.getCost())
   # print "Hub Mass: {0}".format(csmtest.turb.hub.getMass())
   # print

    # print '%9.2f \n %9.2f' % (csmtest.turb.rotorCost / 1000.0, csmtest.turb.rotorMass)
    # print '%9.2f \n %9.2f' % (csmtest.turb.nac.cost / 1000.0, csmtest.turb.nac.mass)
    # print '%9.2f' % (csmtest.turb.tower.cost / 1000.0)
    # print '%9.2f' % (csmtest.turb.tower.mass)
    # print '%9.2f' % (csmtest.turb.mass)

    # print "LCOE: {0}".format(csmtest.fin.LCOE)
    # print "COE: {0}".format(csmtest.fin.COE)
    # print "AEP: {0}".format(csmtest.aep.aep)
    # print "TCC: {0}".format(csmtest.turb.cost)
    # print "Turbine mass: {0}".format(csmtest.turb.mass)
    # print "BOS: {0}".format(csmtest.bos.cost)
    # print "OnM: {0} {1} {2}".format(csmtest.om.cost, csmtest.om.lrc, csmtest.om.llc)

if __name__ == "__main__":

    example()