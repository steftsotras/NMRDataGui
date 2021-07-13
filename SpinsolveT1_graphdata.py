# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 15:08:20 2021

@author: Alexander Michalowski
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit



# Import Graph data

df = pd.read_csv (r'S:\Alexander Michalowski\Spinsolve\20210607-Wasser\20210616-150919-T1\data_graph.csv', decimal='.', delimiter='\t', header=None)

print (df)
Intensity_list_graph = np.asarray(df[1].tolist())
Frequency_list_graph = np.asarray(df[0].tolist())

plt.figure()
plt.scatter(Frequency_list_graph,Intensity_list_graph)
plt.xlabel('Time / s')
plt.ylabel('Intensity')
# plt.savefig('20210607-095459-T2 Bulk-Wasser_raw-data.png')
plt.show()

def fit_func(x, y_0, A, R_0):
    y = y_0 + A * np.exp(- R_0*x)
    return y

anonymous_fun = lambda x, y_0, R_0, A: fit_func(x, y_0, A, R_0) 

popt, pcov = curve_fit(anonymous_fun, xdata = Frequency_list_graph, ydata = Intensity_list_graph)

R_0_fit = popt[1]
T2 = 1/R_0_fit #s
print('T2 = ', T2, 's')

y_0 = popt[0]
A_fit = popt[2]
print('y_0 = ', y_0, ', A = ', A_fit)

fit_intensity = fit_func(Frequency_list_graph, y_0, A_fit, R_0_fit)

plt.plot(Frequency_list_graph,fit_intensity,'k-')
plt.xlabel('Time / s')
plt.ylabel('Intensity')
# plt.savefig('20210607-095459-T2 Bulk-Wasser_log-data.png')
plt.show()



