#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 12:52:50 2019

@author: tvt22
"""
from oneRelaxationTime import oneRelaxationTime
from ImportNmrData import NmrToolbox

# =============================================================================
# Driver for surface calculation of non porous material
# =============================================================================

# =============================================================================
# Surface Area calculation for new material/suspension
# =============================================================================

materialName = 'CarbonBlack_N375_mit_N134'

bulkName = 'Tetrahydrofuran'
user = 'Alexander Michalowski'

# General Remarks, e.g. sediment or suspension, measurement in Fow Cell, particles were still agglomerated during measurement, sedimentation occured during measurement, ...
remarks = '#177'

# Additional information about measurement
measurementDate = '20210521'
temperature = '25°C'

# Surface area of particles measured with BET-method and argon in m2/g
surfaceAreaArgon = 82.8

# Density of bulk liquid in g/cm3
densityBulk = 1

# Sceletal density of particles in g/cm3
densityParticle = 0.345

# Mass of particles in g 
particleWeight = 0.0603

# Mass of liquid in g 
liquidWeight = 1.9435

# Name of file with reference measurement
relaxivityFileName = '../surfaceRelaxivity/Tetrahydrofuran/20210525_CarbonBlack_N134_EinwaageMasse_AM_#172_#173_#174_#175_Tetrahydrofuran.xlsx'

# Relaxation time T1 and T2 and initial magnetization of Bulk 
T1_Bulk, Mz_Bulk, fileNames_T1_Bulk = NmrToolbox.getSurfaceAreaMeasuremntResults('T1', 'Bulk')
T2_Bulk, Mxy_Bulk, fileNames_T2_Bulk = NmrToolbox.getSurfaceAreaMeasuremntResults('T2', 'Bulk')

# Alternative: Set relaxation times without selecting measurement files
# T1_Bulk = [2637.1115,	2708.516693,	2564.65787]
# Mz_Bulk = [138.6811857,	138.7158395,	138.8231618]
# fileNames_T1_Bulk = ['M:\\AcornArea\\Ute Schmidt\\2020-05-27 120331_MP Wasser LFG-T₁ measurement.nmrdata', 'M:\\AcornArea\\Ute Schmidt\\2020-06-02 144500_MP Wasser LFG-T₁ measurement.nmrdata', 'M:\\AcornArea\\Ute Schmidt\\2020-06-03 110530_MP Wasser LFG-T₁ measurement.nmrdata']

# T2_Bulk = [2444.129524,	2434.198738,	2451.787886]
# Mxy_Bulk = [381.6910878,	375.9899039,	375.2244728]
# fileNames_T2_Bulk = ['M:\\AcornArea\\Ute Schmidt\\2020-05-27 103235_MP Wasser LFG-T₂ measurement.nmrdata', 'M:\\AcornArea\\Ute Schmidt\\2020-06-10 142055-MP Wasser LFG-T₂ measurement.nmrdata', 'M:\\AcornArea\\Ute Schmidt\\2020-06-10 142434-MP Wasser LFG-T₂ measurement.nmrdata']

# Relaxation time T1 and T2 and initial magnetization of suspension 
T1, Mz, fileNames_T1_Suspension = NmrToolbox.getSurfaceAreaMeasuremntResults('T1', 'Suspension')
T2, Mxy, fileNames_T2_Suspension = NmrToolbox.getSurfaceAreaMeasuremntResults('T2', 'Suspension')

# Alternative: Set relaxation times without selecting measurement files
# T1 = [2497.643177,2343.169759,2428.079764]
# Mz = [2398.884877,	2414.264733, 2344.511178]
# fileNames_T1_Suspension = ['M:\\AcornArea\\Ute Schmidt\\2020-10-01 153055_#132.6_Kalibriergerade_80nm_10wt%-T₁ measurement.nmrdata', 'M:\\AcornArea\\Ute Schmidt\\2020-10-01 151511_#132.4_Kalibriergerade_80nm_10wt%-T₁ measurement.nmrdata', 'M:\\AcornArea\\Ute Schmidt\\2020-10-01 145520_#132.2_Kalibriergerade_80nm_10wt%-T₁ measurement.nmrdata']

# T2 = [576.881929,	571.3010835,	559.349631]
# Mxy = [247.1628242,	246.8821993,	250.2724155]
# fileNames_T2_Suspension = ['M:\\AcornArea\\Ute Schmidt\\2020-10-01 153005_#132.5_Kalibriergerade_80nm_10wt%-T₂ measurement.nmrdata', 'M:\\AcornArea\\Ute Schmidt\\2020-10-01 151421_#132.3_Kalibriergerade_80nm_10wt%-T₂ measurement.nmrdata', 'M:\\AcornArea\\Ute Schmidt\\2020-10-01 144050_#132.1_Kalibriergerade_80nm_10wt%-T₂ measurement.nmrdata']


# Create object 'mat' of class nonporousMaterial with properties materialName and bulkName
mat = oneRelaxationTime(materialName,bulkName)
mat.setUser(user)
mat.setRemarks(remarks)

mat.setMeasurementFileNames(fileNames_T1_Bulk, fileNames_T2_Bulk, 'Bulk')
mat.setMeasurementFileNames(fileNames_T1_Suspension, fileNames_T2_Suspension, 'Suspension')

# Set values for density and mass in object 'mat' and calculate weightFraction 
mat.setDensity(densityBulk,densityParticle)
mat.setParticleMass(particleWeight)
mat.setLiquidMass(liquidWeight)
mat.calculateWeightFraction()

# Set name of relaxivity file, surface area of BET-measurement temperature and date in object
mat.setRelaxivityFileName(relaxivityFileName)
mat.setSurfaceArea(surfaceAreaArgon)
mat.setTemperature(temperature)
mat.setDate(measurementDate)

# Set relaxation times of suspension and bulk
mat.setRelaxationTime('T1',T1)
mat.setRelaxationTime('T2',T2)
mat.setRelaxationTimeBulk('T1',T1_Bulk)
mat.setRelaxationTimeBulk('T2',T2_Bulk)

# Set initial magnetization bulk
mat.setInitialMagnetizationBulk(Mxy_Bulk,'T2')
mat.setInitialMagnetizationBulk(Mz_Bulk,'T1')

# Set initial magnetization suspension
mat.setInitialMagnetization(Mxy,'T2')
mat.setInitialMagnetization(Mz,'T1')

# Calculate volume fraction using mass of particles and liquid
volFrac = mat.calculateVolumeFractionFromWeightFraction()

## Calculate surface area with T1
mat.calculateSurfaceArea('T1',calculationOfVolumeFraction='mass')
mat.calculateSurfaceArea('T1',calculationOfVolumeFraction='Mz')

# Calculate surface area with T2
mat.calculateSurfaceArea('T2',calculationOfVolumeFraction='mass')
mat.calculateSurfaceArea('T2',calculationOfVolumeFraction='Mxy')

# Create text file with all results
mat.createResultsFile()