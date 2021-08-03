# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 15:08:20 2021

@author: Alexander Michalowski
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import optimize
from scipy.optimize import curve_fit

df = pd.read_csv (r'C:\Users\Hephaistos\Desktop\20210607-Wasser\20210607-095459-T2 Bulk-Wasser\spectrum_processed.csv', decimal=',', delimiter=';', header=0)

Intensity_list = np.asarray(df['Intensity'].tolist())
Frequency_list = np.asarray(df['Frequency(ppm)'].tolist())
#print (Intensity_list)
y_0 = np.max(Intensity_list)
def fit_func(x, y_0, A, R_0):
    y = y_0 + A * np.exp(-R_0*x)
    return y

anonymous_fun = lambda x, A, R_0: fit_func(x, y_0, A, R_0) 

popt, pcov = curve_fit(anonymous_fun, xdata = Frequency_list, ydata = Intensity_list, p0=[780000,0.35])
A_fit = popt[0]
R_0_fit = popt[1]

fit_intensity = fit_func(Frequency_list, y_0, A_fit, R_0_fit)
print (popt)
print (y_0)
#print (fit_intensity)

plt.scatter(Frequency_list,Intensity_list)
plt.scatter(Frequency_list,fit_intensity)
#plt.xlabel('Time / xx')
#plt.ylabel('Intensity / xx')
plt.show()
