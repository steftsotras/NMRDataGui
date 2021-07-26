# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 17:21:19 2020

@author: qu86rave
"""

# import packages
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
#import matplotlib2tikz

import locale
locale.setlocale(locale.LC_NUMERIC, "de_DE")
plt.rcdefaults()
plt.rcParams['axes.formatter.use_locale'] = True
plt.rcParams.update({'font.size': 12})


import referenceMeasurement as reference

# Define class calibration for plotting calibration plots and T1/T2-ratio plots 
class comparisonPlots():

    def __init__(self, fileNames = []):
        # File names of reference measurement files which are compared in the plots
        self.referenceMeasurementFiles = fileNames
        
        # Reference measurement objects
        self.referenceMeasurements = []
        
    def setReferenceMeasurementFiles(self,referenceMeasurementFiles):
        self.referenceMeasurementFiles = referenceMeasurementFiles
        
    def setReferenceMeasurementObjects(self):
        # Set all reference measurement objects
        for referenceMeasurementFileName in self.referenceMeasurementFiles:
            ref = reference.referenceMeasurement()
            ref.particleMass=[]
            ref.liquidMass=[]
            ref.readRelaxivityFile(referenceMeasurementFileName)
            self.referenceMeasurements.append(ref)
            
# =============================================================================
# Calibration Plots            
# =============================================================================
    
    def plotCalibration(self,T1_T2,calculationOfVolumeFraction,legend,figureName=[],language = 'german'):
        # Plot calibraiton curves of different materials for T1 or T2 and volume fraction calculated with 'mass', 'Mz' or 'Mxy'
        plt.figure()
        plt.ticklabel_format(axis='y',style='sci',scilimits=(1,4))

        color = ['r','b','g','k', 'c', 'm']
        # color_fit = ['r--','b--','g--','k--', 'c--', 'm--']

        # color = ['red', 'darkred', 'orange', 'lightcoral', 'royalblue', 'deepskyblue', 'darkblue']
        # color_fit = ['b--','g--','k--', 'c--', 'm--', 'y--', 'r--', 'g--']

        # Loop through different reference measurement objects and plot each calibration curve
        for counter, referenceMeasurement in enumerate(self.referenceMeasurements):
            # calculate volume fraction using the mass or initial magnetization
            volumeFraction = referenceMeasurement.volumeFraction[calculationOfVolumeFraction]
            surfaceArea_Argon = referenceMeasurement.surfaceArea_Argon
            
            # Define x- values for the calibration plot
            
            x = np.asarray(volumeFraction)*surfaceArea_Argon
            
            # Define y-values for the calibration plot
            relaxationRates, standardDeviation = referenceMeasurement.calculateRelaxationRateVector(T1_T2)
            plt.errorbar(x,relaxationRates, yerr = standardDeviation, marker= 'o', linestyle='None', color=color[counter], ecolor='k',capsize=2,label=legend[counter])
            
            # Calculate slope and y-intercept for linear fit (Trendlinie)
            slope, y_intercept, r_value, p_value, std_err = stats.linregress(x,relaxationRates)
            
            # Plot linear fit
            plt.plot(x,slope*x+y_intercept,linestyle='--',color = color[counter])
        if language=='english':
            plt.xlabel('$V_P \cdot V_L^{-1} \cdot$ $A$ / $\mathrm{m}^\mathrm{2} \mathrm{g}^\mathrm{-1}$')
            plt.legend(loc='best', fontsize='medium')
        elif language=='german':
            #r'$\Psi_P \cdot \mathrm{S}$ / $\mathrm{m}^\mathrm{2}\mathrm{g}^\mathrm{-1}$'
            plt.xlabel(r'$\Psi_P \cdot \mathrm{S}$ / $\mathrm{m}^\mathrm{2}\mathrm{g}^\mathrm{-1}$', fontsize='large')
            plt.legend(loc='best', fontsize='medium')
        # Check if calibration is for T1 or T2
        if language=='english':
            if T1_T2 == 'T1':
                plt.ylabel('$T_1^{-1}$ / $\mathrm{ms}^\mathrm{-1}$')
            elif T1_T2 == 'T2':
                plt.ylabel('$T_2^{-1}$ / $\mathrm{ms}^\mathrm{-1}$')
        elif language=='german':
            if T1_T2 == 'T1':
                plt.ylabel('$T_1^{-1}$ / $\mathrm{ms}^\mathrm{-1}$', fontsize='medium')
                #plt.ylim([0,0.0006])
               #HIER
            elif T1_T2 == 'T2':
                plt.ylabel('$T_2^{-1}$ / $\mathrm{ms}^\mathrm{-1}$', fontsize='medium')
                #plt.ylim([0,0.001])
               #HIER
        plt.tight_layout()
        plt.legend(fontsize='medium', loc='upper left')
        # plt.xticks([0,1,2,3,4],[0,1,2,3,4])
        
        
        plt.savefig('../CalibrationPlots/' + figureName + '.png',dpi=500)
        # matplotlib2tikz.save('../CalibrationPlots/' + figureName +'.tex',encoding="utf-8")
        #plt.show()
    
    
    def plotVolumeRateVsRelaxationRate(self,T1_T2,calculationOfVolumeFraction,legend,figureName=[],language = 'german'):
        # Plot calibraiton curves of different materials for T1 or T2 and volume fraction calculated with 'mass', 'Mz' or 'Mxy'
        plt.figure()
        plt.ticklabel_format(axis='y',style='sci',scilimits=(1,4))
        color = ['ro','bo','go','ko', 'co', 'mo']
        
        # color = ['ro','bo','go','ko', 'co', 'mo']
        
        color_fit = ['r--','b--','g--','k--', 'c--', 'm--']
        # color = ['bo','co','mo','ro']
        # color_fit = ['b--','c--','m--','r--']
        # Loop through different reference measurement objects and plot each calibration curve
        for counter, referenceMeasurement in enumerate(self.referenceMeasurements):
            # calculate volume fraction using the mass or initial magnetization
            volumeFraction = referenceMeasurement.volumeFraction[calculationOfVolumeFraction]
            surfaceArea_Argon = referenceMeasurement.surfaceArea_Argon
            
            # Define x- values for the calibration plot
            
            x = np.asarray(volumeFraction)
            
            # Define y-values for the calibration plot
            relaxationRates, standardDeviation = referenceMeasurement.calculateRelaxationRateVector(T1_T2)
            plt.errorbar(x,relaxationRates, yerr = standardDeviation, fmt=color[counter],ecolor='k',capsize=2,label=legend[counter])
            
            # Calculate slope and y-intercept for linear fit (Trendlinie)
            slope, y_intercept, r_value, p_value, std_err = stats.linregress(x,relaxationRates)
            
            # Plot linear fit
            plt.plot(x,slope*x+y_intercept,color_fit[counter])
        if language=='englisch':
            plt.xlabel('$V_P \cdot V_L^{-1}$ / -')
            plt.legend(loc='best')
        elif language=='german':
            
            plt.xlabel(r'$\Psi_P$ / -', fontsize='large')
            plt.legend(loc='best')
        # Check if calibration is for T1 or T2
        if language=='englisch':
            if T1_T2 == 'T1':
                plt.ylabel('$T_1^{-1}$ / $\mathrm{ms}^\mathrm{-1}$')
            elif T1_T2 == 'T2':
                plt.ylabel('$T_2^{-1}$ / $\mathrm{ms}^\mathrm{-1}$')
        elif language=='german':
            if T1_T2 == 'T1':
                plt.ylabel('$T_1^{-1}$ / $\mathrm{ms}^\mathrm{-1}$', fontsize='large')
                
            elif T1_T2 == 'T2':
                plt.ylabel('$T_2^{-1}$ / $\mathrm{ms}^\mathrm{-1}$', fontsize='large')
                
               
        plt.tight_layout()
        plt.legend(fontsize='large', loc='upper left')
        # plt.xticks([0,1,2,3,4],[0,1,2,3,4])
        
        plt.savefig('../RelaxationRateVsVolumeFractionPlots/' + figureName + '.png',dpi=500)
        # matplotlib2tikz.save('../CalibrationPlots/' + figureName +'.tex',encoding="utf-8")
        plt.show()
# =============================================================================
#       T1_T2_Ratio
# =============================================================================
        
    def plotT1_T2_Ratios(self,T1_T2_ratio,figureName=[],language = 'german'):
        plt.figure()
        
        color = ['r','b','g','k']
        
        # Loop through reference Measurement objects and plot T1/T2 ratio        
        for counter, referenceMeasurement in enumerate(self.referenceMeasurements):
            particleMass = self.referenceMeasurements[counter].particleMass
            surfaceArea_Argon = referenceMeasurement.surfaceArea_Argon
            liquidMass = self.referenceMeasurements[counter].liquidMass
            
            # Calculate absolute amount of surface area
            x = np.asarray(particleMass)*surfaceArea_Argon/np.asarray(liquidMass)
            
                         
            # Get relaxation time for each concentration
            relaxationTimes = referenceMeasurement.calculateRelaxationTimes()
            
            # Calculate relaxation time ratio
            relaxationTimesRatio = np.asarray(relaxationTimes['T1']) / np.asarray(relaxationTimes['T2'])
            if counter == 0:
                legend = '80 nm'
            elif counter == 1:
                legend = '120 nm'
            elif counter == 2:
                legend = '200 nm (I)'
            else:
                legend = '200 nm (II)'
            # Plot relaxation time ratio vs. absolute amount of surface area
            plt.plot(x,relaxationTimesRatio,'o', c=color[counter],label=legend)#referenceMeasurement.materialName)
            
            # Calculate linear fit (Slope and y-intercept)
            slope_surf, y_intercept, r_value, p_value, std_err = stats.linregress(x,relaxationTimesRatio)
            
            # Plot linear fit 
            plt.plot(x,slope_surf*x+y_intercept,color[counter])
        
        plt.ticklabel_format(style='sci',axis='y',scilimits=(0,0))
        if language=='englisch':
            plt.xlabel('absolute surface area $m_P \cdot S$ / $\mathrm{m}^\mathrm{2}$')
            plt.ylabel('r$\frac{T_1}{T_2}$')
        elif language=='german':
            plt.xlabel('$\mathrm{m_P} \cdot \mathrm{m_L^{-1}} \cdot S $ / $\mathrm{m}^\mathrm{2}$ ${g}^\mathrm{-1}$')
            plt.ylabel('$\mathrm{T_1} \cdot \mathrm{T_2^{-1}}$ / -')
        plt.legend(loc='best')
    
    
        plt.tight_layout()
        
        figureName = '../T1_T2_ratio/' + figureName + '.png'
        plt.savefig(figureName,dpi=500)
        plt.show()
        
        
# =============================================================================
# Examples
# =============================================================================

# T1_T2_Ratio 
#referenceMeasurementFiles = ['../surfaceRelaxivity/Milipore-Wasser_LFG/20200928_80nm_Kalibriergerade_Milipore-Wasser_LFG.xlsx','../surfaceRelaxivity/Milipore-Wasser_LFG/20200527_120nm_Kalibriergerade_Messung 1_Milipore-Wasser_LFG.xlsx','../surfaceRelaxivity/Milipore-Wasser_LFG/20200928_200nm Kalibriergerade_Milipore-Wasser_LFG.xlsx','../surfaceRelaxivity/Milipore-Wasser_LFG/20200428_Silica_200_nm_Milipore-Wasser_LFG.xlsx']
#cal = comparisonPlots(referenceMeasurementFiles)
#cal.setReferenceMeasurementObjects()
# cal.plotCalibration('T1','mass','Silica_80_120_200_T1_mass_calibration')
# cal.plotCalibration('T2','mass','Silica_80_120_200_T2_mass_calibration')
#cal.plotT1_T2_Ratios('T1_T2_ratio','Silica_80_120_2x200nm_Ute')

### Vergleich 200 nm ausgeheizt - nicht  ausgeheizt
# referenceMeasurementFiles = ['../surfaceRelaxivity/Milipore-Wasser_LFG/20200505_Silica_200_nm_ausgeheizt_Milipore-Wasser_LFG.xlsx','../surfaceRelaxivity/Milipore-Wasser_LFG/20200428_Silica_200_nm_Milipore-Wasser_LFG.xlsx','../surfaceRelaxivity/Milipore-Wasser_LFG/20200928_200nm Kalibriergerade_Milipore-Wasser_LFG.xlsx']
# cal = comparisonPlots(referenceMeasurementFiles)
# cal.setReferenceMeasurementObjects()
# legend = ['200 nm ausgeheizt (Darius)', '200 nm (Darius)', '200 nm (Ute)']
# cal.plotCalibration(T1_T2 = 'T1',calculationOfVolumeFraction = 'mass', legend=legend, figureName='Vergleich_200nm_ausgeheizt_T1')
# cal.plotCalibration('T2','mass',legend,'Vergleich_200nm_ausgeheizt_T2')


# Vergleich 120 nm Kalibriergeraden
# language = 'german'        
# Calibration  

# referenceMeasurementFiles = ['../surfaceRelaxivity/Milipore-Wasser_LFG/20201111_120nm Kalibriergerade_1,5wt%_Tragacanth_#1_Milipore-Wasser_LFG.xlsx','../surfaceRelaxivity/Milipore-Wasser_LFG/20201111_120nm Kalibriergerade_1,5wt%_Tragacanth_#2_Milipore-Wasser_LFG.xlsx']
# cal = comparisonPlots(referenceMeasurementFiles)
# cal.setReferenceMeasurementObjects()
# cal.plotCalibration(T1_T2 = 'T1',calculationOfVolumeFraction = 'mass', legend = ['Kalibriergerade 1','Kalibriergerade 2'], figureName='Reproduzierbarkeit_Kalibriergeraden_1,5wt%_Tragacanth_T1_neu')
# cal.plotCalibration('T2','mass',['Kalibriergerade 1','Kalibriergerade 2'],'Reproduzierbarkeit_Kalibriergeraden_1,5wt%_Tragacanth_T2_neu')

# referenceMeasurementFiles = ['../surfaceRelaxivity/Milipore-Wasser_LFG/20201123_Silica_10um_Milipore-Wasser_LFG.xlsx','../surfaceRelaxivity/Milipore-Wasser_LFG/20201123_Silica_1um_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20201120_Silica_500nm_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20201120_Silica_150nm_Milipore-Wasser_LFG.xlsx']
# referenceMeasurementFiles = ['../surfaceRelaxivity/Milipore-Wasser_LFG/20200527_120nm_Kalibriergerade_Messung 1_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20200928_80nm_Kalibriergerade_Milipore-Wasser_LFG.xlsx']

# referenceMeasurementFiles = ['../surfaceRelaxivity/Milipore-Wasser_LFG/20200527_120nm_Kalibriergerade_Messung 1_Milipore-Wasser_LFG.xlsx','../surfaceRelaxivity/Milipore-Wasser_LFG/20200615_120nm Kalibriergerade Messung 2_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser/20191218_Silica 120 nm_Milipore-Wasser.xlsx', '../surfaceRelaxivity/Milipore-Wasser/20200428_Silica_120_nm_Milipore-Wasser.xlsx']
# cal = comparisonPlots(referenceMeasurementFiles)
# cal.setReferenceMeasurementObjects()
# cal.plotCalibration(T1_T2 = 'T1',calculationOfVolumeFraction = 'mass', legend = ['Kalibriergerade 1','Kalibriergerade 2', 'Kalibriergerade Darius 1', 'Kalibriergerade Darius 2'], figureName='Reproduzierbarkeit_Kalibriergerade_120nm_T1_mitKalibriergeradeDarius')
# cal.plotCalibration('T2','mass',['Kalibriergerade 1','Kalibriergerade 2', 'Kalibriergerade Darius 1', 'Kalibriergerade Darius 2'],'Reproduzierbarkeit_Kalibriergerade_120nm_T2_mitKalibriergeradeDarius')


# Tragacanth Kalibriergeraden
# referenceMeasurementFiles = ['../surfaceRelaxivity/Milipore-Wasser_LFG/20200527_120nm_Kalibriergerade_Messung 1_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20201019_120nm Kalibriergerade_1wt%_Tragacanth_#2_neu_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20201111_120nm Kalibriergerade_1,5wt%_Tragacanth_#1_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20200911_120nm Kalibriergerade_2wt%_Tragacanth_#1_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20201112_120nm Kalibriergerade_2,5wt%_Tragacanth_Milipore-Wasser_LFG.xlsx']
# cal = comparisonPlots(referenceMeasurementFiles)
# cal.setReferenceMeasurementObjects()
# cal.plotCalibration(T1_T2 = 'T1',calculationOfVolumeFraction = 'mass', legend = ['0 Gew.-% Tragacanth', '1,0 Gew.-% Tragacanth', '1,5 Gew.-% Tragacanth','2,0 Gew.-% Tragacanth','2,5 Gew.-% Tragacanth'], figureName='Einfluss_Tragacanth_Kalibriergerade_120nm_T1_komplett_neu')
# cal.plotCalibration('T2','mass',['0 Gew.-% Tragacanth', '1,0 Gew.-% Tragacanth', '1,5 Gew.-% Tragacanth','2,0 Gew.-% Tragacanth','2,5 Gew.-% Tragacanth'],'Einfluss_Tragacanth_Kalibriergerade_120nm_T2_komplett_neu')

## Vergleich alle Kalibriergeraden Ute
# referenceMeasurementFiles = ['../surfaceRelaxivity/Milipore-Wasser_LFG/20200928_80nm_Kalibriergerade_Milipore-Wasser_LFG.xlsx','../surfaceRelaxivity/Milipore-Wasser_LFG/20200928_80nm_Kalibriergerade_#2_Milipore-Wasser_LFG.xlsx','../surfaceRelaxivity/Milipore-Wasser_LFG/20200527_120nm_Kalibriergerade_Messung 1_Milipore-Wasser_LFG.xlsx','../surfaceRelaxivity/Milipore-Wasser_LFG/20200615_120nm Kalibriergerade Messung 2_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20200928_200nm_Kalibriergerade_neu_Milipore-Wasser_LFG.xlsx','../surfaceRelaxivity/Milipore-Wasser_LFG/20200928_200nm_Kalibriergerade_#2_Milipore-Wasser_LFG.xlsx',]
# cal = comparisonPlots(referenceMeasurementFiles)
# cal.setReferenceMeasurementObjects()
# cal.plotCalibration(T1_T2 = 'T1',calculationOfVolumeFraction = 'mass', legend = ['80 nm Messung 1', '80 nm Messung 2', '120 nm Messung 1', '120 nm Messung 2', '200 nm Messung 1','200 nm Messung 2'], figureName='Vergleich_aller_Kalibriergeraden_Ute_T1')
# cal.plotCalibration('T2','mass',['80 nm Messung 1', '80 nm Messung 2', '120 nm Messung 1', '120 nm Messung 2', '200 nm Messung 1','200 nm Messung 2'],'Vergleich_aller_Kalibriergeraden_Ute_T2')



# referenceMeasurementFiles = ['../surfaceRelaxivity/Milipore-Wasser_LFG/20200527_120nm_Kalibriergerade_Messung 1_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20200928_200nm Kalibriergerade_Milipore-Wasser_LFG.xlsx']

# cal = comparisonPlots(referenceMeasurementFiles)
# cal.setReferenceMeasurementObjects()
# cal.plotVolumeRateVsRelaxationRate('T1','mass', ['120 nm', '200 nm'],'Auswertung_mit_2_Geraden_200nm_T1')
# cal.plotVolumeRateVsRelaxationRate('T2','mass',['120 nm', '200 nm'],'Auswertung_mit_2_Geraden_200nm_T2')

##### Vergleich Messungen Ute und Darius
# referenceMeasurementFiles = [ '../surfaceRelaxivity/Milipore-Wasser_LFG/20200527_120nm_Kalibriergerade_Messung 1_Milipore-Wasser_LFG.xlsx','../surfaceRelaxivity/Milipore-Wasser_LFG/20200615_120nm Kalibriergerade Messung 2_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser/20191218_Silica 120 nm_Milipore-Wasser.xlsx', '../surfaceRelaxivity/Milipore-Wasser/20200428_Silica_120_nm_Milipore-Wasser.xlsx','../surfaceRelaxivity/Milipore-Wasser/20200123_Silica 80 nm_Milipore-Wasser.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20200429_Silica_80_nm_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20200928_80nm_Kalibriergerade_Milipore-Wasser_LFG.xlsx']
# cal = comparisonPlots(referenceMeasurementFiles)
# cal.setReferenceMeasurementObjects()
# legend = ['120 nm, Ute 1','120 nm, Ute 2', '120 nm, Darius 1', '120 nm, Darius 2', '80 nm, Darius 1', '80 nm, Darius 2', '80 nm, Ute ']
# cal.plotCalibration('T1','mass', legend,'Vergleich_80nm_120nm_Ute_Darius_T1')
# cal.plotCalibration('T2','mass',legend,'Vergleich_80nm_120nm_Ute_Darius_T2')

#### Vergleich 80 nm, 120 nm, 200 nm
# referenceMeasurementFiles = [ '../surfaceRelaxivity/Milipore-Wasser_LFG/20200428_Silica_200_nm_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20200527_120nm_Kalibriergerade_Messung 1_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20200928_80nm_Kalibriergerade_Milipore-Wasser_LFG.xlsx']
# cal = comparisonPlots(referenceMeasurementFiles)
# cal.setReferenceMeasurementObjects()
# legend = ['200 nm','120 nm', '80 nm']
# cal.plotCalibration('T1','mass', legend,'Vergleich_80nm_120nm_200nm_T1')
# cal.plotCalibration('T2','mass',legend,'Vergleich_80nm_120nm_200nm_T2')


# referenceMeasurementFiles = ['../surfaceRelaxivity/Milipore-Wasser_LFG/20200428_Silica_200_nm_Milipore-Wasser_LFG.xlsx']

# cal = comparisonPlots(referenceMeasurementFiles)
# cal.setReferenceMeasurementObjects()
# cal.plotCalibration('T1','mass', ['200 nm'],'200nm_Kalibriergerade_Darius_T1')
# cal.plotCalibration('T2','mass',['200 nm'],'200nm_Kalibriergerade_Darius_T2')

####### Silica 1 µm, 500 nm, 150 nm, 120 nm, 200 nm und 80 nm Vergleich
# referenceMeasurementFiles = ['../surfaceRelaxivity/Milipore-Wasser_LFG/20201123_Silica_1um_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20201120_Silica_500nm_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20201120_Silica_150nm_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20200428_Silica_200_nm_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20200615_120nm Kalibriergerade Messung 2_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20200429_Silica_80_nm_Milipore-Wasser_LFG.xlsx']

# cal = comparisonPlots(referenceMeasurementFiles)
# cal.setReferenceMeasurementObjects()
# cal.plotCalibration('T1','mass', ['Silica 1 µm', 'Silica 500 nm', 'Silica 150 nm', 'Silica 200 nm', 'Silica 120 nm', 'Silica 80 nm'],'Silica_nonporous_SigmaAldrich_80nm-1µm_MPWasser_T1')
# cal.plotCalibration('T2','mass',['Silica 1 µm', 'Silica 500 nm', 'Silica 150 nm', 'Silica 200 nm', 'Silica 120 nm', 'Silica 80 nm'],'Silica_nonporous_SigmaAldrich_80nm-1µm_MPWasser_T2')

# referenceMeasurementFiles = ['../surfaceRelaxivity/Milipore-Wasser_LFG/20200928_200nm_Kalibriergerade_neu_Milipore-Wasser_LFG.xlsx','../surfaceRelaxivity/Milipore-Wasser_LFG/20200428_Silica_200_nm_Milipore-Wasser_LFG.xlsx']

# cal = comparisonPlots(referenceMeasurementFiles)
# cal.setReferenceMeasurementObjects()
# cal.plotCalibration('T1','mass', ['Ute','Darius'],'200nm_Kalibriergeraden_UteDarius_T1')
# cal.plotCalibration('T2','mass',['Ute','Darius'],'200nm_Kalibriergeraden_UteDarius_T2')

# referenceMeasurementFiles = ['../surfaceRelaxivity/Milipore-Wasser_LFG/20201005_120nm_Kalibriergerade_1,5wt%_Phytagel_#1_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20201021_120nm_Kalibriergerade_1,5wt%_Phytagel_#2_Milipore-Wasser_LFG.xlsx']

# cal = comparisonPlots(referenceMeasurementFiles)
# cal.setReferenceMeasurementObjects()
# cal.plotCalibration(T1_T2 = 'T1',calculationOfVolumeFraction = 'mass', legend = ['1. Messung', '2. Messung'], figureName='Reproduzierbarkeit_Kalibriergerade_Phytagel_T1')
# cal.plotCalibration('T2','mass',['1. Messung', '2. Messung'],'Reproduzierbarkeit_Kalibriergerade_Phytagel_T2')

# cal.plotCalibration('T1','Mz',['LUDOX TM-40','LUDOX SM'],'Comparison_LUDOX_Versuch1_Mz')
# cal.plotCalibration('T2','Mxy',['LUDOX TM-40','LUDOX SM'],'Comparison_LUDOX_Versuch1__Mxy')

# Vergleich 120 nm Kalibriergeraden mit und ohne Verdickungsmittel
# referenceMeasurementFiles = ['../surfaceRelaxivity/Milipore-Wasser_LFG/20200527_120nm_Kalibriergerade_Messung 1_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20200907_120nm Kalibriergerade_1wt%_Tragacanth_#2_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20200911_120nm Kalibriergerade_2wt%_Tragacanth_#2_Milipore-Wasser_LFG.xlsx']
# cal = comparisonPlots(referenceMeasurementFiles)
# cal.setReferenceMeasurementObjects()
# cal.plotCalibration(T1_T2 = 'T1',calculationOfVolumeFraction = 'mass', legend = ['0wt% Tragacanth', '1wt% Tragacant', '2wt% Tragacanth'], figureName='Einfluss_Tragacanth_Kalibriergerade_120nm_T1')
# cal.plotCalibration('T2','mass',['0wt% Tragacanth', '1wt% Tragacant', '2wt% Tragacanth'],'Einfluss_Tragacanth_Kalibriergerade_120nm_T2')

# Vergleich Silica Proben
# referenceMeasurementFiles = ['../surfaceRelaxivity/Milipore-Wasser_LFG/20200527_120nm_Kalibriergerade_Messung 1_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20200928_Koestrosol_9550_Kalibriergerade_S_BET_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20200917_Koestrosol_4550_Kalibriergerade_S_BET_Milipore-Wasser_LFG.xlsx','../surfaceRelaxivity/Milipore-Wasser_LFG/20200914_Koestrosol_1430_Kalibriergerade_S_BET_Milipore-Wasser_LFG.xlsx', '../surfaceRelaxivity/Milipore-Wasser_LFG/20200914_Koestrosol_0730_Kalibriergerade_S_BET_Milipore-Wasser_LFG.xlsx']
# cal = comparisonPlots(referenceMeasurementFiles)
# cal.setReferenceMeasurementObjects()
# cal.plotCalibration(T1_T2 = 'T1',calculationOfVolumeFraction = 'mass', legend = ['120 nm Silica', 'Köstrosol 9550', 'Köstrosol 4550', 'Köstrosol 1430', 'Köstrosol 0730'], figureName='Vergleich_Silica120nm_Köstrosol_T1')
# cal.plotCalibration('T2','mass',['120 nm Silica', 'Köstrosol 9550', 'Köstrosol 4550', 'Köstrosol 1430', 'Köstrosol 0730'],'Vergleich_Silica120nm_Köstrosol_T2')

#referenceMeasurementFiles = ['../surfaceRelaxivity/20190522_Silica_200nm_VE-water.json','../surfaceRelaxivity/20200116_Silica 200 nm_Milipore-Wasser_ohne5wt%.json']
#cal = comparisonPlots(referenceMeasurementFiles)
#cal.setReferenceMeasurementObjects()
#cal.plotCalibration('T1','mass','Silica_200nm_Messung_Carola_MessungDarius_T1_mass_calibration')
#cal.plotCalibration('T2','mass','.Silica_200nm_Messung_Carola_MessungDarius_T2_mass_calibration')
 
