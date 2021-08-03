# -*- coding: utf-8 -*-
"""
Created on Mon Jun 14 15:08:20 2021

@author: Alexander Michalowski
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
from scipy.optimize import curve_fit
import pylab as plb
from scipy import special
import math as math

#Import NNR data

df = pd.read_csv (r'S:\Alexander Michalowski\Spinsolve\20210607-Wasser\20210616-150919-T1\data.csv', decimal='.', delimiter='\t', header=None)

Intensity_list = np.asarray(df[1].tolist())
Frequency_list = np.asarray(df[0].tolist())

plt.figure()
plt.scatter(Frequency_list,Intensity_list)
plt.xlabel('Time / s')
plt.ylabel('Intensity')
# #plt.savefig('20210607-095459-T2 Bulk-Wasser_raw-data.png')
plt.show()

x_bound = Frequency_list[Frequency_list>3.8]
y_bound = Intensity_list[Frequency_list>3.8]

x_gaus = x_bound[x_bound<5.5]
y_gaus = y_bound[x_bound<5.5]

np.trapz(y_gaus, x_gaus)

# n = len(x_gaus)                          #the number of data
# mean = sum(x_gaus*y_gaus)/n                   #note this correction
# sigma = sum(y_gaus*(x_gaus-mean)**2)/n        #note this correction

# def gaus(x,a,x0,sigma):
#     return a*np.exp(-(x-x0)**2/(2*sigma**2))

# popt,pcov = curve_fit(gaus,x_gaus,y_gaus) #start parameter ,p0=[max(y),mean,sigma]
# print (popt, "popt")
# y_gaus_fit = gaus(x_gaus,*popt)


# mü = popt[1]
# a = popt[0]
# sigma = popt[2]
# x0 = max(y_gaus_fit)

# plt.plot(x_gaus,y_gaus,'b+:',label='data')
# plt.plot(x_gaus,y_gaus_fit,'ro:',label='fit')
# plt.legend()
# plt.title('Fig. 1 - Fit with Gauss')
# plt.xlabel('Time (s)')
# plt.ylabel('Intensity')
# plt.show()

# #x_gaus_minus1 = x_gaus[:-1]
# y_verteilung = 0.5 * a * (1+special.erf((x_gaus-mü) /(math.sqrt(2)*sigma)))
# # y_verteilung = integrate.quad(gaus(x_gaus,a, x0, sigma),-np.inf,np.inf)

# plt.plot(x_gaus, y_verteilung)
# plt.xlabel('Time (s)')
# plt.ylabel('Intensity')
# plt.show()

# x_fit_bound = np.array(x_gaus[x_gaus<5.5])
# y_fit_bound = np.array(y_verteilung[x_gaus<5.5])


# # print (y_fit_2, x_fit_2)

# x_fit = x_fit_bound[x_fit_bound>4]
# y_fit = y_fit_bound[x_fit_bound>4.]


def fit_func(x, y_0, A, R_0):
    y = y_0 + A * np.exp(- R_0*x)
    return y

anonymous_fun = lambda x, y_0, R_0, A: fit_func(x, y_0, A, R_0) 

popt, pcov = curve_fit(anonymous_fun, xdata = x_fit, ydata = y_fit)

R_0_fit = popt[1]
T2 = 1/R_0_fit #s
print('T2 = ', T2, 's')

y_0 = popt[0]
A_fit = popt[2]
print('y_0 = ', y_0, ', A = ', A_fit)

fit_intensity = fit_func(x_fit, y_0, A_fit, R_0_fit)

plt.plot(x_fit,fit_intensity,'k-')
plt.xlabel('Time / s')
plt.ylabel('ln(Intensity)')
# plt.savefig('20210607-095459-T2 Bulk-Wasser_log-data.png')
plt.show()

















#Import Graph data

# df2 = pd.read_csv (r'F:\Spinsolve\20210607-Wasser\20210616-150919-T1\data_graph.csv', decimal='.', delimiter='\t', header=None)

# print (df)
# Intensity_list_graph = np.asarray(df2[1].tolist())
# Frequency_list_graph = np.asarray(df2[0].tolist())

# plt.figure()
# plt.scatter(Frequency_list_graph,Intensity_list_graph)
# plt.xlabel('Time / s')
# plt.ylabel('Intensity')
# plt.savefig('20210607-095459-T2 Bulk-Wasser_raw-data.png')
# plt.show()

#Gauss




# # Intensity_list_log = np.log(Intensity_list)
# # plt.figure()
# # plt.scatter(Frequency_list,Intensity_list_log)
# # plt.xlabel('Time / s')
# # plt.ylabel('ln(Intensity)')
# # plt.savefig('20210607-095459-T2 Bulk-Wasser_log-raw-data.png')
# # plt.show()

# Frequency_list_short = Frequency_list[Frequency_list<0.8]  #evtl bis zur fehlermeldung
# Intensity_list_short = Intensity_list[Frequency_list<0.8]


# Intensity_list_log = np.log(Intensity_list_short)

# plt.figure()
# plt.scatter(Frequency_list_short,Intensity_list_log)

# #print (Intensity_list_log)
# # A = np.max(Intensity_list_short)

# def fit_func(x, y_0, A, R_0):
#     y = np.log(y_0 + A * np.exp(- R_0*x))
#     return y

# anonymous_fun = lambda x, y_0, R_0, A: fit_func(x, y_0, A, R_0) 

# popt, pcov = curve_fit(anonymous_fun, xdata = Frequency_list_short, ydata = Intensity_list_log)

# R_0_fit = popt[1]
# T2 = 1/R_0_fit #s
# print('T2 = ', T2, 's')

# y_0 = popt[0]
# A_fit = popt[2]
# print('y_0 = ', y_0, ', A = ', A_fit)

# fit_intensity = fit_func(Frequency_list_short, y_0, A_fit, R_0_fit)

# plt.plot(Frequency_list_short,fit_intensity,'k-')
# plt.xlabel('Time / s')
# plt.ylabel('ln(Intensity)')
# plt.savefig('20210607-095459-T2 Bulk-Wasser_log-data.png')
# plt.show()
