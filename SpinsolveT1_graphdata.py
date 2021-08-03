# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 15:08:20 2021

@author: Alexander Michalowski
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import warnings 

# warnings.filterwarnings("ignore")



    # Import Graph data

# df = pd.read_csv (r'M:\AcornArea\Alexander Michalowski\Spinsolve\20210607-Wasser\20210616-123132-T1\data_graph.csv', decimal='.', delimiter='\t', header=None)
# df = pd.read_csv (r'M:\AcornArea\Alexander Michalowski\Spinsolve\20210711-#217-Koestrosol4450\20210712-152324-T1\data_graph.csv', decimal='.', delimiter='\t', header=None)
df = pd.read_csv (r'M:\AcornArea\Alexander Michalowski\Spinsolve\20210711-#217-Koestrosol4450\20210712-155249-T1\data_graph.csv', decimal='.', delimiter='\t', header=None)
    # print (df) 1. geht und Richtiger wert, 2. geht aber fit falsch 3. geht nicht -> Error
Intensity_list_graph = np.asarray(df[1].tolist())
Frequency_list_graph = np.asarray(df[0].tolist())

#Intensity_list_log = np.log(Intensity_list_graph)
Intensity_list_graph_shot2 = Intensity_list_graph#[Intensity_list_graph>0]  #[np.logical_not(np.isnan(Intensity_list_graph))] 
Frequency_list_graph_shot2 = Frequency_list_graph#[Intensity_list_graph>0] 

Intensity_list_graph_shot = Intensity_list_graph_shot2#[Frequency_list_graph_shot2<4]  #[np.logical_not(np.isnan(Intensity_list_graph))] 
Frequency_list_graph_shot = Frequency_list_graph_shot2#[Frequency_list_graph_shot2<4] 
print(Intensity_list_graph_shot)
print(Frequency_list_graph_shot)

plt.figure()
plt.scatter(Frequency_list_graph_shot,Intensity_list_graph_shot)
plt.xlabel('Time / s')
plt.ylabel('Intensity')
# plt.savefig('20210607-095459-T2 Bulk-Wasser_raw-data.png')
plt.show()

def fit_func(x, y_0, A, R_0):
    y = y_0 + A * np.exp(- R_0*x)
    return y

anonymous_fun = lambda x, y_0, R_0, A: fit_func(x, y_0, A, R_0) 

popt, pcov = curve_fit(anonymous_fun, xdata = Frequency_list_graph_shot, ydata = Intensity_list_graph_shot)

R_0_fit = popt[1]
T1_long = (1/R_0_fit)*1000 #ms
T1 = round(T1_long, 1)

print('T1 = ', T1, 'ms')

y_0 = popt[0]
A_fit = popt[2]
print('y_0 = ', y_0, ', A = ', A_fit)

fit_intensity = fit_func(Frequency_list_graph, y_0, A_fit, R_0_fit)

plt.plot(Frequency_list_graph,fit_intensity,'k-')
plt.xlabel('Time / s')
plt.ylabel('Intensity')
plt.savefig('20210607-095459-T2 Bulk-Wasser_log-data.png')
plt.show()


