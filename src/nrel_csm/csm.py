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

    def compute(self, hubHeight, ratedPower, maxTipSpd, rotorDiam, dtDesign, nblades, altitude, thrustCoeff, seaDepth, crane, advancedBlade,  advancedBedplate, advancedTower, year, month, maxCp, maxTipSpdRatio, cutInWS, cutOutWS, \
                      airDensity, shearExp, ws50m, weibullK, soilingLosses, arrayLosses, availability, fcr, taxrate, discountrate, constructiontime, projlifetime, turbineNum):

        self.powerCurve.compute(self.drivetrain, hubHeight, ratedPower,maxTipSpd,rotorDiam,  \
                   maxCp, maxTipSpdRatio, cutInWS, cutOutWS, \
                   altitude, airDensity)

        self.powercurve = np.array(self.powerCurve.powerCurve)
  
        self.aep.compute(self.powercurve, ratedPower, hubHeight, shearExp,ws50m,weibullK, \
                  soilingLosses, arrayLosses, availability)
  
        self.turb.compute(hubHeight, ratedPower, maxTipSpd, rotorDiam, dtDesign, nblades, \
                         self.drivetrain.getMaxEfficiency(), self.powerCurve.ratedWindSpeed, altitude, thrustCoeff, seaDepth, crane, advancedBlade, \
                         advancedBedplate, advancedTower, year, month)

        self.bos.compute(seaDepth,ratedPower,hubHeight,rotorDiam,self.turb.cost, turbineNum, year, month)

        self.om.compute(self.aep.aep, seaDepth, ratedPower, year, month)

        self.fin.compute(ratedPower, self.turb.cost, self.om.cost, self.om.llc, self.om.lrc, \
                 self.bos.cost, self.aep.aep, fcr, taxrate, discountrate, \
                 constructiontime, projlifetime, turbineNum, seaDepth)

def example():

    #Default Cost and Scaling Model inputs for 5 MW turbine (onshore)    
    ppi.curr_yr  = 2009
    ppi.curr_mon = 12

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
    taxrate = 0.4
    discountrate = 0.07
    constructiontime = 1
    projlifetime = 20
    turbineNum = 100
    
    csmtest = csm(dtDesign)
    csmtest.compute(hubHeight, ratedPower, maxTipSpd, rotorDiam, dtDesign, nblades, altitude, thrustCoeff, seaDepth, crane, advancedBlade,  advancedBedplate, advancedTower, year, month, maxCp, maxTipSpdRatio, cutInWS, cutOutWS, \
                      airDensity, shearExp, ws50m, weibullK, soilingLosses, arrayLosses, availability, fcr, taxrate, discountrate, constructiontime, projlifetime, turbineNum)
           
    print "LCOE %9.8f" % (csmtest.fin.LCOE)
    print "COE %9.8f"%(csmtest.fin.COE)
    print "AEP %9.5f"%(csmtest.aep.aep / 1000.0)
    print "BOS %9.5f"%(csmtest.bos.cost / 1000.0)
    print "TCC %9.5f"%(csmtest.turb.cost / 1000.0)
    print "OM %9.5f"%(csmtest.om.cost / 1000.0)
    print "LRC %9.5f"%(csmtest.om.lrc / 1000.0)
    print "LLC %9.5f"%(csmtest.om.llc / 1000.0)
    print
    csmtest.turb.cm_print()
    csmtest.turb.nac.dump()
    csmtest.bos.dump()

if __name__ == "__main__":

    example()