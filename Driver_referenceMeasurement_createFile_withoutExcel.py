#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:03:42 2019

@author: tvt22
"""

import referenceMeasurement as ref
import numpy as np
import matplotlib.pyplot as plt

from ImportNmrData import NmrToolbox

#import locale
#locale.setlocale(locale.LC_NUMERIC, "de_DE")
#plt.rcdefaults()
#plt.rcParams['axes.formatter.use_locale'] = True
#plt.rcParams.update({'font.size': 12})

from matplotlib import rcParams
rcParams.update({'figure.autolayout': True})

# Material name and name of bulk

# Material name and name of bulk
materialName = 'Silica200nm'
bulkName = 'Milipore-Wasser_LFG'
user = 'Alexander Michalowski'
# german oder english
language = 'german'
thickener = False
evaluation = 'single'

# General Remarks, e.g. sediment or suspension, particles were still agglomerated during measurement, sedimentation occured during measurement, ...
remarks = 'Spinsolve #184-#187'

## Additional information about measurement
date = '20210615'
temperature = '25°C'

## Surface area of particles measured with BET-method and argon in m2/g (Necessary to calculate ka)
surfaceArea_Argon = 15.80

# Density of bulk liquid in g/cm3
densityBulk = 1

# Sceletal density of particles in g/cm3
particleDensity = 2.15

# Mass of particles in g 
particleMass = [0,0.1023,0.2042,0.3001,0.4032]

# Mass of liquid in g
liquidMass = [1,1.9008,1.8110,1.7028,1.6085]

# WeightFraction calculated with particleMass and liquidMass (not necessary if particle Mass and liquidMass are defined)
#weightFraction = [0,10,20,30,40]
#volumeFraction = ([0,0.0478,0.1076,0.1845,0.287])

# Relaxation times T1 and T2, defined as T = [[relaxation times of 1st concentration] [relaxation times of 2nd concentration] [...]]
T1 = [[1771.9,1791.7,1746.1],[1766.7,1786.4,1854.4],[1843.2,1832.5,1757],[1762.5,1749.3,1733.6],[1774.2,1838.6,1739.1]]
T2 = [[2619.9,2639.4,2642.4],[662.1,675.6,677.6],[363.8,362.7,363.0],[220.8,224.0,224.1],[165.0,167.3,167.5]]

# T1 and Mz lists are generated - only select files for T1 here
#T1, Mz, fileNames_T1 = NmrToolbox.getCalibrationResults('T1', 5)

# T2 an Mxy lists are generated - only select files for T2 here
#T2, Mxy, fileNames_T2 = NmrToolbox.getCalibrationResults('T2', 5)


# If porousMaterial=1: Set surface relaxivity calculated from porous material with 2 relaxation times with class porous material
# If porousMaterial=0; Calculate surface relaxivity of nonporous material (1 relaxation time)
porousMaterial=0
surfaceRelaxivity_T2_Mxy =[]

# Initial magnetization
# Mz = [[103,105,101],[98,100,97],[92,94,92],[86,83,85]]
# Mxy = [[288,286,282],[275,274,270],[258,255,258],[227,227,227],[209,206,205]]

# Mz_Bulk = [102,100,101]
# Mxy_Bulk = [283,284,285]



# Create object 'ref' of class referenceMeasurement with properties materialName and bulkName
ref = ref.referenceMeasurement(materialName, bulkName) 
ref.setDate(date)
ref.setTemperature(temperature)
ref.setUser(user)
ref.setRemarks(remarks)

# Set liquid density and particle density
ref.setDensity(densityBulk,particleDensity)

## Set particle mass and liquid mass and calculate weightFraction or alternatively set weightFraction
ref.setParticleMass(particleMass)
ref.setLiquidMass(liquidMass)
ref.calculateWeightFraction()
# ref.setWeightFraction(weightFraction)

# Set surface area calculated with BET method and argon
ref.setSurfaceArea(surfaceArea_Argon)

# Set relaxation times T1 and T2
ref.setRelaxationTime('T1',T1)
if not porousMaterial:
    ref.setRelaxationTime('T2',T2)
else:
    ref.surfaceRelaxivity['volFrac_Mxy'] = surfaceRelaxivity_T2_Mxy

# # Set initial magnetization of suspension and bulk
# ref.setInitialMagnetization(Mz,'T1')
# ref.setInitialMagnetization(Mxy,'T2')

# Calculate and set volume Fraction
volFrac = ref.calculateVolumeFractionFromWeightFraction()
# volFrac = ref.calculateVolumeFractionFromMagnetization('T1')
# volFrac = ref.calculateVolumeFractionFromMagnetization('T2')
# ref.setVolumeFraction(volumeFraction,'mass')


# Calculate surface relaxivity ka for T1 and T2 measurement
if thickener == False:
    ref.calculate_surfaceRelaxivity('T1', evaluation, calculationOfVolFraction='mass', plot=True, language='german')
    # ref.calculate_surfaceRelaxivity('T1', evaluation, calculationOfVolFraction='Mz', plot=True, language='german')
    
    # Create T1/T2 vs. concentration and T1/T2 vs. absolute surface area (information about surface chemistry?)
    # slope_conc, slope_surf = ref.plot_T1_T2_ratio('german')
    
    # Calculate surface relaxivity in case of nonporous material
    if not porousMaterial:
        ref.calculate_surfaceRelaxivity('T2', evaluation, calculationOfVolFraction='mass', plot=True,  language='german')
        # ref.calculate_surfaceRelaxivity('T2', evaluation, calculationOfVolFraction='Mxy', plot=True,  language='german')
    
    # ref.setMeasurementFileNames(fileNames_T1, fileNames_T2)
    ref.createRelaxivityFile(evaluation)    
    
# Plot calibration for thickener in dispersant    
else:
    ref.plotCalibrationWithThickener('T1',calculationOfVolFraction='mass', language='german')
    # ref.plotCalibrationWithThickener('T1',calculationOfVolFraction='Mz', language='german')
    
    ref.plotCalibrationWithThickener('T2',calculationOfVolFraction='mass', language='german')
    # ref.plotCalibrationWithThickener('T2',calculationOfVolFraction='Mxy', language='german')
    
    