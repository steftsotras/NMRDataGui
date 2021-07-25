#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 08:35:27 2020

@author: tvt22
"""
import comparisonPlots as comparisonPlots
import numpy as np
import matplotlib.pyplot as plt

class Driver_comparisonPlots:

    def runDriver(self, referenceMeasurementFiles, T1_T2, volumeFraction, legend, language, plotname):
        # Compare calibration lines for T1 and T2
        #referenceMeasurementFiles = ['../surfaceRelaxivity/Tetrahydrofuran/20210617_CarbonBlack_N134_THF_density_AM_#172_#173_#174_#175_Tetrahydrofuran.xlsx','../surfaceRelaxivity/Tetrahydrofuran/20210617_CarbonBlack_N375_THF_density_AM_#176_#177_#178_#179_Tetrahydrofuran.xlsx','../surfaceRelaxivity/Tetrahydrofuran/20210617_CarbonBlack_N774_THF_density_AM_#169_#170_#171_Tetrahydrofuran.xlsx']
        
        cal = comparisonPlots.comparisonPlots(referenceMeasurementFiles)
        cal.setReferenceMeasurementObjects()

        if T1_T2 == 'T1':
            cal.plotCalibration('T1', volumeFraction[0], legend, plotname[0]+'_'+language[:3], language)
        elif T1_T2 == 'T2': 
            cal.plotCalibration('T1', volumeFraction[1], legend, plotname[1]+'_'+language[:3], language)
        elif T1_T2 == 'both':
            cal.plotCalibration('T1', volumeFraction[0], legend, plotname[0]+'_'+language[:3], language)
            cal.plotCalibration('T2', volumeFraction[1], legend, plotname[1]+'_'+language[:3], language)


        #cal.plotCalibration(T1_T2 = 'T1',calculationOfVolumeFraction = 'mass', legend = ['N134','N375','N774'], figureName='Vergleich_CarbonBlack_with_newY_THF_T1')
        #cal.plotCalibration('T2','mass',['N134','N375','N774'],'Vergleich_CarbonBlack_with_newY_THF_T2')


        ## Compare T1_T2 ratio of different materials (depending on the surface area)
        # referenceMeasurementFiles = ['../surfaceRelaxivity/20200116_Silica 200 nm_Milipore-Wasser_ohne5wt%.json','../surfaceRelaxivity/20191218_Silica 120 nm_Milipore-Wasser.json','../surfaceRelaxivity/20200123_Silica 80 nm_Milipore-Wasser.json']
        # cal = comparisonPlots(referenceMeasurementFiles)
        # cal.setReferenceMeasurementObjects()
        # cal.plotT1_T2_Ratios('T1_T2_ratio','Silica_200_120_80nm_mass_calibration',language)


if __name__ == '__main__':
    driver = Driver_comparisonPlots()
    driver.runDriver()
