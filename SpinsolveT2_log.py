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


df = pd.read_csv (r'S:\Alexander Michalowski\Spinsolve\20210611-#187-silica120II\20210611-162046-T2 Bulk\spectrum_processed.csv', decimal=',', delimiter=';', header=0)

Intensity_list = np.asarray(df['Intensity'].tolist())
Frequency_list = np.asarray(df['Frequency(ppm)'].tolist())

plt.figure()
plt.scatter(Frequency_list,Intensity_list)
plt.xlabel('Time / s')
plt.ylabel('Intensity')
#plt.savefig('20210607-095459-T2 Bulk-Wasser_raw-data.png')
plt.show()

# Intensity_list_log = np.log(Intensity_list)
# plt.figure()
# plt.scatter(Frequency_list,Intensity_list_log)
# plt.xlabel('Time / s')
# plt.ylabel('ln(Intensity)')
# plt.savefig('20210607-095459-T2 Bulk-Wasser_log-raw-data.png')
# plt.show()

Frequency_list_short = Frequency_list[Frequency_list<0.8]  #evtl bis zur fehlermeldung
Intensity_list_short = Intensity_list[Frequency_list<0.8]


Intensity_list_log = np.log(Intensity_list_short)
# Intensity_list_log = Intensity_list_short

plt.figure()
plt.scatter(Frequency_list_short,Intensity_list_log)

#print (Intensity_list_log)
# A = np.max(Intensity_list_short)

def fit_func(x, y_0, A, R_0):
    # y = y_0 + -A * np.exp(- R_0*x)
    y = np.log(y_0 + A * np.exp(- R_0*x))
    return y

anonymous_fun = lambda x, y_0, R_0, A: fit_func(x, y_0, A, R_0) 

popt, pcov = curve_fit(anonymous_fun, xdata = Frequency_list_short, ydata = Intensity_list_log)

R_0_fit = popt[1]
T2 = 1/R_0_fit #s
print('T2 = ', T2, 's')

y_0 = popt[0]
A_fit = popt[2]
print('y_0 = ', y_0, ', A = ', A_fit)

fit_intensity = fit_func(Frequency_list_short, y_0, A_fit, R_0_fit)

plt.plot(Frequency_list_short,fit_intensity,'k-')
plt.xlabel('Time / s')
plt.ylabel('ln(Intensity)')
plt.savefig('20210607-095459-T2 Bulk-Wasser_log-data.png')
plt.show()
