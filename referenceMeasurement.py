#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 17:30:03 2019

@author: tvt22
"""

# import packages
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import json
#import matplotlib2tikz
import pandas as pd
import glob
import os




from NMR import NMR

# Define class referenceMeasurement which inherits from class NMR 
class referenceMeasurement(NMR):

        def __init__(self,materialName=[],bulk=[],surfaceArea_Argon=[],temperature=[],date=[],weightFraction=[],densityBulk=[],densityParticle=[],relaxivityFileName=[],particleMass=[],liquidMass=[]):
            NMR.__init__(self,materialName,bulk,surfaceArea_Argon,temperature,date,weightFraction,densityBulk,densityParticle,relaxivityFileName)   

            directory = os.path.dirname('../surfaceRelaxivity/' + self.bulk+'/')
            if not os.path.exists(directory):
                os.makedirs(directory) 
            
        
            
        def calculateVolumeFractionFromMagnetization(self,T1_T2='T2'):
            # Create first entry for pure bulk
            initialMagnetizationSuspensionList =[]
            # Append list for all concentrations measured for the calibration plot
            for initialMagnetizationOfConcentration in self.initialMagnetization[T1_T2]:
                initialMagnetizationSuspensionList.append(np.mean(initialMagnetizationOfConcentration))
                
            # Calculate volume fraction with difference of initial magnetization of bulk and suspension 
            particleVolume = initialMagnetizationSuspensionList[0]-np.asarray(initialMagnetizationSuspensionList)
            if T1_T2 == 'T1':
                self.volumeFraction['Mz'] = particleVolume/np.asarray(initialMagnetizationSuspensionList)
            elif T1_T2 == 'T2':
                self.volumeFraction['Mxy'] = particleVolume/np.asarray(initialMagnetizationSuspensionList)
            return particleVolume/np.asarray(initialMagnetizationSuspensionList) 
        
        def calculateRelaxationRateVector(self,T1_T2 = 'T2'):
            # Preallocate Lists
            relaxationTimesList = []
            standardDeviationList = []
            
            for relTimesOfConcentration in self.relaxationTime[T1_T2]:
                relaxationTimesList.append(np.mean(relTimesOfConcentration))
                standardDeviationList.append(np.std(1/np.asarray(relTimesOfConcentration)))
                
            # Calculate relaxation rates
            relaxationRates = 1/np.asarray(relaxationTimesList)
            return relaxationRates, standardDeviationList
        
        def calculate_surfaceRelaxivity(self,T1_T2='T2',evaluation='single', language='english', calculationOfVolFraction='mass', plot=False):
            """Get surface relaxivity ka from slope of plot of relaxationRates vs. (volumeFraction * surfaceArea) or from plot of relaxationRates vs. volumeFraction
 
             Parameters
             ----------
             T1_T2 : string
                 String containing 'T1' or 'T2' which defines if surface relaxivity is calculated for T1 or T2.
             evaluation : string
                 String containing 'single' or 'multiple' which determines the created plot: relaxationRates vs. (volumeFraction*surfaceArea_Argon) or relaxationRates vs. volumeFraction
             calculationOfVolumeFraction : string
                 String containing 'mass' or 'Mz' or 'Mxy' which determines how the volumeFraction is calculated for calculating the surface relaxivity
             plot : Boolean
                 Boolean which determines if a plot is created or not. If True the plot is created and saved
             language: string
                 String containing 'german' or 'english' which determines the language of axis labels
                 
             Returns
             -------
             surfaceRelaxivity : float
                 Float which determines the surfaceRelaxivity calculated from the slope of the calibration curve
             """
           
           # Get surface relaxivity ka from slope of plot of relaxationRates vs. (volumeFraction * surfaceArea)
            if evaluation == 'single':
                # Define x-values (volumeFraction*surfaceArea) for linear plot, 3 different calcuation methods for volume fraction possible
                if calculationOfVolFraction == 'mass':
                    x = np.asarray(self.volumeFraction['mass']) * self.surfaceArea_Argon
                elif calculationOfVolFraction == 'Mxy':
                    if T1_T2=='T2':
                        x = np.asarray(self.volumeFraction['Mxy']) * self.surfaceArea_Argon
                    else:
                        print('Initial magnetization Mxy can only be used for T2!')
                elif calculationOfVolFraction == 'Mz':
                    if T1_T2=='T1':
                        x = np.asarray(self.volumeFraction['Mz']) * self.surfaceArea_Argon
                    else:
                        print('Initial magnetization Mz can only be used for T1!')
                        
                # Define y-values (relaxationRates) for linear plot
                relaxationRates, standardDeviationList = self.calculateRelaxationRateVector(T1_T2)
                
                # Get slope of the linear plot, ka = slope
                slope, y_intercept, r_value, p_value, std_err = stats.linregress(x,relaxationRates)
                
                surfaceRelaxivity = slope
                
                # Save slope as surfaceRelaxivity
                if calculationOfVolFraction == 'mass':
                    self.surfaceRelaxivity['mass'][T1_T2] = slope
                else:
                    self.surfaceRelaxivity[calculationOfVolFraction] = slope
                
                # Plot linear calibration plot
                if plot:
                    self.plotCalibrationPlot(x,T1_T2,calculationOfVolFraction, evaluation, language)
            
            
            # Get surface relaxivity ka from slope/surfaceAreaArgon of plot of relaxationRates vs. volumeFraction
            else:
                 # Define x-values (volumeFraction*surfaceArea) for linear plot, 3 different calcuation methods for volume fraction possible
                if calculationOfVolFraction == 'mass':
                    x = np.asarray(self.volumeFraction['mass'])
                elif calculationOfVolFraction == 'Mxy':
                    if T1_T2=='T2':
                        x = np.asarray(self.volumeFraction['Mxy'])
                    else:
                        print('Initial magnetization Mxy can only be used for T2!')
                elif calculationOfVolFraction == 'Mz':
                    if T1_T2=='T1':
                        x = np.asarray(self.volumeFraction['Mz'])
                    else:
                        print('Initial magnetization Mz can only be used for T1!')
                        
                # Define y-values (relaxationRates) for linear plot
                relaxationRates, standardDeviationList = self.calculateRelaxationRateVector(T1_T2)
                
                # Get slope of the linear plot, ka = slope
                slope, y_intercept, r_value, p_value, std_err = stats.linregress(x,relaxationRates)
                
                # Save slope as surfaceRelaxivity
                if calculationOfVolFraction == 'mass':
                    self.surfaceRelaxivity['mass'][T1_T2] = slope / self.surfaceArea_Argon
                else:
                    self.surfaceRelaxivity[calculationOfVolFraction] = slope / self.surfaceArea_Argon
                
                # Plot linear calibration plot
                if plot:
                    self.plotCalibrationPlot(x,T1_T2,calculationOfVolFraction, evaluation, language)
                surfaceRelaxivity = slope/ self.surfaceArea_Argon
                return surfaceRelaxivity    
        
        
        def plotCalibrationPlot(self,x,T1_T2,calculationOfVolumeFraction='mass', evaluation = 'single', language = 'english', fontsize=14):
            # Plot linear calibration plot: relaxationRates vs. (volumeFraction * surfaceArea)
            
            # Define font size of the plot
            plt.rcParams.update({'font.size': fontsize})
            
            relaxationRates, standardDeviation = self.calculateRelaxationRateVector(T1_T2)
            
            # Create new plot
            plt.figure()
            
            # Linear plotvolFrac_Mxy'volFrac_Mxy'
            # for LUDOX & Köstrosol no standard deviations in both cases - outcomment if/else-case
            # plt.errorbar(x,relaxationRates, yerr = None, fmt='o',ecolor='k',capsize=2)
            if T1_T2 == 'T1':
                plt.errorbar(x,relaxationRates, yerr = standardDeviation, fmt='o',ecolor='k',capsize=2, barsabove=True)
            else:
                plt.errorbar(x,relaxationRates, yerr = None, fmt='o',ecolor='k',capsize=2)

            
            slope, y_intercept, r_value, p_value, std_err = stats.linregress(x,relaxationRates)
            plt.plot(x, slope*x+y_intercept,'k--')
            
            # Check if volume ratio or mass ratio was used for calculation of surface relaxivity and create x-label
            if evaluation == 'single':
                if language=='english':
                    plt.xlabel(r'$\Psi_P \cdot \mathrm{S}$ / $\mathrm{m}^\mathrm{2} \mathrm{g}^\mathrm{-1}$')
                elif language=='german':
                    plt.xlabel(r'$\Psi_P \cdot \mathrm{S}$ / $\mathrm{m}^\mathrm{2} \mathrm{g}^\mathrm{-1}$')
            else:
                if language=='english':
                    plt.xlabel(r'$\Psi_P \cdot \mathrm{S}$ / $\mathrm{m}^\mathrm{2} \mathrm{g}^\mathrm{-1}$')
                elif language=='german':
                    plt.xlabel(r'$\Psi_P \cdot \mathrm{S}$ / $\mathrm{m}^\mathrm{2} \mathrm{g}^\mathrm{-1}$')
                    
            
            # Check if calibration is for T1 or T2
            if language=='english':
                if T1_T2 == 'T1':
                    plt.ylabel('$T_1^{-1}$ / $\mathrm{ms}^\mathrm{-1}$')
                elif T1_T2 == 'T2':
                    plt.ylabel('$T_2^{-1}$ / $\mathrm{ms}^\mathrm{-1}$')
            elif language=='german':
                if T1_T2 == 'T1':
                    plt.ylabel(r'$T_1^{-1}$ / $\mathrm{ms}^\mathrm{-1}$')
                elif T1_T2 == 'T2':
                    plt.ylabel(r'$T_2^{-1}$ / $\mathrm{ms}^\mathrm{-1}$')
            
            # Define Name of the figure and save figure
            if evaluation == 'single':
                folder = 'surfaceRelaxivity/'
            else:
                folder = 'surfaceRelaxivityTwoCurves/'
            
            if language=='english':
                figureName = '../' + folder + self.bulk + '/' + self.date + '_' + self.materialName + '_' + self.remarks + '_' + self.bulk + '_' + T1_T2 + '_volFrac_' + calculationOfVolumeFraction +'_calibration.png'
                #figureName_tex = '../surfaceRelaxivity/' + self.date + '_' + self.materialName + '_' + self.bulk + '_' + T1_T2 + '_volFrac_' + calculationOfVolumeFraction + '_calibration.tex'
            elif language=='german':
                figureName = '../' + folder + self.bulk + '/' + self.date + '_' + self.materialName + '_' + self.remarks + '_' + self.bulk + '_' + T1_T2 + '_volFrac_' + calculationOfVolumeFraction + '_calibration_german.png'
                #figureName_tex = '../surfaceRelaxivity/' + self.date + '_' + self.materialName + '_' + self.bulk + '_' + T1_T2 + '_volFrac_' + calculationOfVolumeFraction + '_calibration_german.tex'
            plt.tight_layout()
            plt.savefig(figureName,dpi=500)
            #matplotlib2tikz.save(figureName_tex,encoding="utf-8")
            #plt.show()
         
            
        def plotCalibrationWithThickener(self, T1_T2='T2', calculationOfVolFraction='mass', language ='german', fontsize=14):
            
            if calculationOfVolFraction == 'mass':
                x = np.asarray(self.volumeFraction['mass'])
            elif calculationOfVolFraction == 'Mxy':
                if T1_T2=='T2':
                    x = np.asarray(self.volumeFraction['Mxy'])
                else:
                    print('Initial magnetization Mxy can only be used for T2!')
            elif calculationOfVolFraction == 'Mz':
                if T1_T2=='T1':
                    x = np.asarray(self.volumeFraction['Mz'])
                else:
                    print('Initial magnetization Mz can only be used for T1!')
            
            relaxationRates, standardDeviation = self.calculateRelaxationRateVector(T1_T2)
            slope, y_intercept, r_value, p_value, std_err = stats.linregress(x,relaxationRates)
            
            plt.rcParams.update({'font.size': fontsize})
            plt.figure()
            
            if T1_T2 == 'T1':
                plt.errorbar(x,relaxationRates, yerr = standardDeviation, fmt='o',ecolor='k',capsize=2, barsabove=True)
            else:
                plt.errorbar(x,relaxationRates, yerr = None, fmt='o',ecolor='k',capsize=2)
            
            plt.plot(x, slope*x+y_intercept,'k--')
            
            # Check if volume ratio or mass ratio was used for calculation of surface relaxivity and create x-label
            if language=='english':
                plt.xlabel(r'$\Psi_P \cdot \mathrm{S}$ / $\mathrm{m}^\mathrm{2} \mathrm{g}^\mathrm{-1}$')
            elif language=='german':
                plt.xlabel(r'$\Psi_P \cdot \mathrm{S}$ / $\mathrm{m}^\mathrm{2} \mathrm{g}^\mathrm{-1}$')
        
            
            # Check if calibration is for T1 or T2
            if language=='english':
                if T1_T2 == 'T1':
                    plt.ylabel('$T_1^{-1}$ / $\mathrm{ms}^\mathrm{-1}$')
                elif T1_T2 == 'T2':
                    plt.ylabel('$T_2^{-1}$ / $\mathrm{ms}^\mathrm{-1}$')
            elif language=='german':
                if T1_T2 == 'T1':
                    plt.ylabel(r'$T_1^{-1}$ / $\mathrm{ms}^\mathrm{-1}$')
                elif T1_T2 == 'T2':
                    plt.ylabel(r'$T_2^{-1}$ / $\mathrm{ms}^\mathrm{-1}$')
            
            # Define Name of the figure and save figure 
            if language=='english':
                figureName = '../CalibrationWithThickener/' + self.bulk + '/' + self.date + '_' + self.materialName + '_' + self.remarks + '_' + self.bulk + '_' + T1_T2 + '_volFrac_' + calculationOfVolFraction + '_calibration.png'
                #figureName_tex = '../surfaceRelaxivity/' + self.date + '_' + self.materialName + '_' + self.bulk + '_' + T1_T2 + '_volFrac_' + calculationOfVolumeFraction + '_calibration.tex'
            elif language=='german':
                figureName = '../CalibrationWithThickener/' + self.bulk + '/' + self.date + '_' + self.materialName + '_' + self.remarks + '_' + self.bulk + '_' + T1_T2 + '_volFrac_' + calculationOfVolFraction + '_calibration_german.png'
                #figureName_tex = '../surfaceRelaxivity/' + self.date + '_' + self.materialName + '_' + self.bulk + '_' + T1_T2 + '_volFrac_' + calculationOfVolumeFraction + '_calibration_german.tex'
            plt.tight_layout()
            plt.savefig(figureName,dpi=500)
            #matplotlib2tikz.save(figureName_tex,encoding="utf-8")
            plt.show()
            
            return
            
        def calculateRelaxationTimes(self):
            relaxationTimesList = {'T1':[],'T2':[]}
            for relTimesOfConcentration in self.relaxationTime['T1']:
                relaxationTimesList['T1'].append(np.mean(relTimesOfConcentration))
                
            for relTimesOfConcentration in self.relaxationTime['T2']:
                relaxationTimesList['T2'].append(np.mean(relTimesOfConcentration))
            return relaxationTimesList
            
        def plot_T1_T2_ratio(self, language = 'english'):
            
            relaxationTimesList = self.calculateRelaxationTimes()
            
            self.relaxationTime['T1_T2_ratio'] = self.calculateT1_T2_ratio(relaxationTimesList['T1'],relaxationTimesList['T2'])
            plt.figure()
            plt.plot(np.asarray(self.weightFraction)*100,self.relaxationTime['T1_T2_ratio'],'o')
            slope_conc, y_intercept, r_value, p_value, std_err = stats.linregress(np.asarray(self.weightFraction)*100,self.relaxationTime['T1_T2_ratio'])
            plt.plot(np.asarray(self.weightFraction)*100,np.asarray(self.weightFraction)*100*slope_conc+y_intercept,'k--')
            if language == 'german':
                plt.xlabel('Konzentration / gew%')
            elif language == 'english':
                plt.xlabel('concentration / wt%')
            plt.ylabel('$T_1 T_2^{-1}$ / -')
            plt.tight_layout()
            figureName = '../T1_T2_ratio/' + self.date + '_' +  self.materialName + '_' + self.remarks + '_' + self.bulk + '_' + 'T1_T2_ratio_conc' + '.png'
            plt.savefig(figureName)
            
            plt.figure()
            plt.plot(np.asarray(self.weightFraction)*self.surfaceArea_Argon,self.relaxationTime['T1_T2_ratio'],'o')
            slope_surf, y_intercept, r_value, p_value, std_err = stats.linregress(np.asarray(self.weightFraction)*self.surfaceArea_Argon,self.relaxationTime['T1_T2_ratio'])
            plt.plot(np.asarray(self.weightFraction)*self.surfaceArea_Argon,np.asarray(self.weightFraction)*self.surfaceArea_Argon*slope_surf+y_intercept,'k--')
            if language == 'german':
                plt.xlabel('absolute Oberfläche / $\mathrm{m}^\mathrm{2}$')
            elif language == 'english':    
                plt.xlabel('absolute surface area / $\mathrm{m}^\mathrm{2}$')
            plt.ylabel('$T_1 T_2^{-1}$ / -')
            plt.tight_layout()
            figureName = '../T1_T2_ratio/' + self.date + '_' +  self.materialName + '_' + self.remarks + '_' + self.bulk + '_' + 'T1_T2_ratio_surf' + '.png'
            plt.savefig(figureName)
            return slope_conc, slope_surf
        
        
        def createRelaxivityFile(self, evaluation):
            # Create excel file with all information and the calculated surface relaxivity
            


            # Define file name 
            if evaluation == 'single':

                #CREATE SELF.BULK FOLDER DYNAMICALLY

                self.relaxivityFileName = '../surfaceRelaxivity/' + self.bulk + '/' + str(self.date) + '_' + self.materialName + '_' + self.remarks + '_' + self.bulk + '.xlsx'
            else:
                self.relaxivityFileName = '../surfaceRelaxivityTwoCurves/' + self.bulk + '/' + str(self.date) + '_' + self.materialName + '_' + self.remarks + '_' + self.bulk + '.xlsx'
                
            if not isinstance(self.volumeFraction['Mz'],list):
                self.volumeFraction['Mz'] = self.volumeFraction['Mz'].tolist()
            if not isinstance(self.volumeFraction['Mxy'],list):
                self.volumeFraction['Mxy'] = self.volumeFraction['Mxy'].tolist()
                
            # Define list with general information for first excel sheet    
            excel_list = []
            excel_list.append(["materialName", self.materialName])
            excel_list.append([ "bulkName", self.bulk])
            excel_list.append(["User", self.user])
            excel_list.append(["remarks", self.remarks])
            excel_list.append(["surfaceArea(Argon)", self.surfaceArea_Argon])
            excel_list.append(["measurementDate", self.date])
            excel_list.append(["temperature", self.temperature])
            excel_list.append(["densityParticle", self.densityParticle])
            excel_list.append(["densityBulk", self.densityBulk])
            excel_list.append([])
            excel_list.append(['volumeFraction', 'relaxationTime', 'surfaceRelaxivity'])
            excel_list.append(['mass', 'T1', self.surfaceRelaxivity['mass']['T1']])
            excel_list.append(['mass', 'T2', self.surfaceRelaxivity['mass']['T2']])
            excel_list.append(['Mz', 'T1', self.surfaceRelaxivity['Mz']])
            excel_list.append(['Mxy', 'T2', self.surfaceRelaxivity['Mxy']])
            
            fileContent = pd.DataFrame(excel_list)
            
            # Define list with information on each calibration point for second excel sheet
            excel_list_calibration = []
            
            for index in range(0,len(self.relaxationTime['T2'])):
                excel_list_calibration.append([str(int(round(self.weightFraction[index]*100, 0))) + 'wt%'])
                
                # Check if particle mass was set, if no particle mass was set, the value is set to nan
                if self.particleMass:
                    excel_list_calibration.append(["particleMass", self.particleMass[index]])
                else:
                    excel_list_calibration.append(["particleMass", np.nan])
                
                if self.liquidMass:
                    excel_list_calibration.append(["liquidMass", self.liquidMass[index]])
                else:
                    excel_list_calibration.append(["liquidMass", np.nan])
                    
                excel_list_calibration.append(["weightFraction", self.weightFraction[index]])
                excel_list_calibration.append([])
                excel_list_calibration.append(['determinationOfCalculation','volumeFraction'])
                
                excel_list_calibration.append(['mass', self.volumeFraction['mass'][index]])
                
                if self.volumeFraction['Mz']:
                    excel_list_calibration.append(['Mz', self.volumeFraction['Mz'][index]])
                else:
                    excel_list_calibration.append(['Mz', np.nan])
                if self.volumeFraction['Mxy']:
                    excel_list_calibration.append(['Mxy',self.volumeFraction['Mxy'][index]])
                else:
                    excel_list_calibration.append(['Mxy', np.nan])
                excel_list_calibration.append([])
                
                if self.initialMagnetization['T1'][0]:
                    excel_list_calibration.append(["initial magnetization Mz"]+ self.initialMagnetization['T1'][index])
                else:
                    excel_list_calibration.append(['initial magnetization Mz', np.nan])
                if self.initialMagnetization['T2'][0]:
                    excel_list_calibration.append(["initial magnetization Mxy"]+ self.initialMagnetization['T2'][index])
                else:
                    excel_list_calibration.append(["initial magnetization Mxy", np.nan])
                
                if self.relaxationTime['T1']:
                    excel_list_calibration.append(['relaxationTime T1']+ self.relaxationTime['T1'][index])
                else:
                    excel_list_calibration.append(['relaxatioTime T1']+ [np.nan])
                excel_list_calibration.append(['relaxationTime T2']+ self.relaxationTime['T2'][index])
                excel_list_calibration.append([])
                excel_list_calibration.append([])
                
            excel_sheet_calibration = pd.DataFrame(excel_list_calibration)
            
            # Define list with measurement file names for third excel sheet
            excel_list_fileNames = []
            if self.measurementFileNames['T1'] and self.measurementFileNames['T2']:
                for index in range(0,len(self.relaxationTime['T1'])):
                    excel_list_fileNames.append([str(int(round(self.weightFraction[index]*100, 0))) + 'wt%'])
                    excel_list_fileNames.append(["T1", self.measurementFileNames['T1'][index]])
                    excel_list_fileNames.append(["T2", self.measurementFileNames['T2'][index]])
                    excel_list_fileNames.append([])
            
            excel_sheet_fileNames = pd.DataFrame(excel_list_fileNames)
            
            # Write to excel file
            writer = pd.ExcelWriter(self.relaxivityFileName, engine='openpyxl')
            fileContent.to_excel(writer, 'general',header = None, index=False)
            excel_sheet_calibration.to_excel(writer, 'calibration',header = None, index=False)
            excel_sheet_fileNames.to_excel(writer, 'measurement files',header = None, index=False)
            writer.save()
        
        
        def readRelaxivityFile(self, relaxivityFileName):
            # Load all properties from exisitng relaxivity file
            
            # Read general information
            data = pd.read_excel(relaxivityFileName, sheet_name='general',header=None)
                
            self.materialName = data[1][0]
            self.bulk = data[1][1]
            self.user = data[1][2]
            self.remarks = data[1][3]
            self.surfaceArea_Argon=data[1][4]
            self.date = data[1][5]
            self.temperature=data[1][6]
            
            self.densityParticle = data[1][7]
            self.densityBulk = data[1][8]
            
            self.surfaceRelaxivity['mass']['T1'] = data[2][11]
            self.surfaceRelaxivity['mass']['T2'] = data[2][12]
            self.surfaceRelaxivity['Mz'] = data[2][13]
            self.surfaceRelaxivity['Mxy'] = data[2][14]
            
            # Read calibration data
            data = pd.read_excel(relaxivityFileName, sheet_name='calibration',header=None)
            
            # Get information on initial magnetization, relaxationtime, ... of ech concentration (The information of each concentration needs 16 columns)
            for index in range(0,int((len(data)+2)/16)):
                
                # Read particle mass, liquid mass and weight fraction
                self.particleMass.append(data[1][16*index+1])
                self.liquidMass.append(data[1][16*index+2])
                self.weightFraction.append(data[1][16*index+3])
                
                # Read volume fraction
                self.volumeFraction['mass'].append(data[1][16*index+6])
                self.volumeFraction['Mz'].append(data[1][16*index+7])
                self.volumeFraction['Mxy'].append(data[1][16*index+8])
                
                # Read initial magnetization (remove nan)
                Mz = data.to_numpy()[16*index+10,1:].tolist()
                self.initialMagnetization['T1'].append([x for x in Mz if ~np.isnan(x)])
                Mxy = data.to_numpy()[16*index+11,1:].tolist()
                self.initialMagnetization['T2'].append([x for x in Mxy if ~np.isnan(x)])
                
                # Read relaxationTime and calculate T1/T2 ratio
                T1 = data.to_numpy()[16*index+12,1:].tolist()
                # Remove NaN
                self.relaxationTime['T1'].append([x for x in T1 if ~np.isnan(x)])
                
                T2 = data.to_numpy()[16*index+13,1:].tolist()
                self.relaxationTime['T2'].append([x for x in T2 if ~np.isnan(x)])
                
            
            # Read calibration data
            data = pd.read_excel(relaxivityFileName, sheet_name='measurement files',header=None)
            
            for index in range(0,int((len(data)+1)/4)):
                self.measurementFileNames['T1'].append(data[1][4*index+1])
                self.measurementFileNames['T2'].append(data[1][4*index+2])
                
            
            # Save relaxivity file name
            self.relaxivityFileName = relaxivityFileName
                
        def readRelaxivityFileFromJson(self, relaxivityFileName):
            # Load all properties from exisitng relaxivity file
            with open(relaxivityFileName) as json_file:
                data = json.load(json_file)
                self.materialName = data['materialName']
                self.bulk = data['bulkName']
                self.user = data['User']
                self.remarks = data['remarks']
                self.surfaceArea_Argon=data['surfaceArea(Argon)']
                self.temperature=data['temperature']
                self.weightFraction = data['weightFraction']
                self.densityParticle = data['densityParticle']
                self.densityBulk = data['densityBulk']
                self.surfaceRelaxivity=data['surfaceRelaxivity']
                self.date = data['measurementDate']
                self.volumeFraction = data['volumeFraction']
                self.relaxationTime = data['RelaxationTime']
                self.relaxivityFileName = relaxivityFileName
                self.initialMagnetization['T1'] = [data['initial magnetization(Bulk)']['T1']]
                self.initialMagnetization['T2'] = [data['initial magnetization(Bulk)']['T2']]
                self.initialMagnetization['T1'] = self.initialMagnetization['T1'] + data['initial magnetization(Suspension)']['T1']
                self.initialMagnetization['T2'] = self.initialMagnetization['T2'] + data['initial magnetization(Suspension)']['T2']
                self.particleMass = data['particleMass']
                self.liquidMass = data['liquidMass']

# for fileCounter, filename in enumerate(glob.glob("%s/*.json" % '../surfaceRelaxivity/Milipore-Wasser/')):
#     print(filename)
#     test = referenceMeasurement()  
#     test.readRelaxivityFileFromJson(filename)
#     test.createRelaxivityFile()
