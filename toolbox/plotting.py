#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 11:17:57 2018

@author: vancraa1
"""

# from statistics import mean
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
# import matplotlib.text as text

# TODO : DOC


def plotFitHist(data, figname='test.pdf', bins=161, rmin=2000, rmax=6000):
    # TODO: determine bins automatically
    # histo, bin_edges, _ = plt.hist(data, bins=bins, range=[rmin, rmax])
    histo, bin_edges = np.histogram(data, bins=bins, range=[rmin, rmax])
    bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])

    # Finding the guess parameters for Gaussian fitting
    x0_guess = bin_edges[np.argmax(histo)]
    sig_guess = np.std(histo)*4
    amp_guess = np.max(histo)

    paramL, covL = curve_fit(lorentz, bin_centers, histo)
    paramG, covG = curve_fit(gaussian, bin_centers, histo,
                             p0=[x0_guess, sig_guess, amp_guess])
    x_plot = np.linspace(rmin, rmax, 20000)
    plt.plot(bin_centers, histo, 'r-')
    plt.plot(x_plot, lorentz(x_plot, *paramL), ':m')
    plt.plot(x_plot, gaussian(x_plot, *paramG), '--b')
    plt.title("60Co resolution")
    plt.xlabel("Time")
    plt.ylabel("Counts")
    plt.legend(('data', 'Fit lorentz', 'Fit Gaussian'),
               loc='upper right', shadow=True)
    plt.text(rmin, 0.8*np.max(histo),
             'Fit parameters:\n FWHM Lor = {:.4}\n FWHM Gaus = {:.5}'
             .format(paramL[1], paramG[1]*2.35482))
    plt.savefig(figname)
    plt.show()


def plotHist(data, figname='test.pdf', bins=161, rmin=2000, rmax=6000, logY=False):
    # TODO: determine bins automatically
    # histo, bin_edges, _ = plt.hist(data, bins=bins, range=[rmin, rmax])
    histo, bin_edges = np.histogram(data, bins=bins, range=[rmin, rmax])
    bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])

    if logY is True:
        plt.semilogy(bin_centers, histo, 'b-')
    else:
        plt.plot(bin_centers, histo, 'r-')
    plt.title("Time spectrum")
    plt.xlabel("Time")
    plt.ylabel("Counts")
    plt.legend(("data"), loc='upper right', shadow=True)
    plt.savefig(figname)
    plt.show()


def plotHists(data, figname='test.pdf', bins=161, rmin=2000, rmax=6000,
              logY=False, style='-'):
    # TODO: determine bins automatically
    for data in data:
        histo, bin_edges = np.histogram(data, bins=bins, range=[rmin, rmax])
        bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
        if logY is True:
            plt.semilogy(bin_centers, histo, '-')
        else:
            plt.plot(bin_centers, histo, style)
    plt.title("Time spectrum")
    plt.xlabel("Time")
    plt.ylabel("Counts")
    plt.legend(("data01", "data02"), loc='upper right', shadow=True)
    plt.savefig(figname)
    plt.show()


def saveHists(data, filebase='test', bins=161, rmin=2000, rmax=6000, useChnEnding=False):
    ii = 0
    chnEndings = ('01', '02', '12')
    for data in data:
        histo, bin_edges = np.histogram(data, bins=bins, range=[rmin, rmax])
        if useChnEnding is True:
            filename = filebase + chnEndings[ii] + '.hst'
        else:
            filename = filebase + str(ii) + '.txt'
        np.savetxt(filename, histo, fmt='%i',
                   header="bins: {}\nrange: [{}:{}]".format(bins, rmin, rmax))
        ii += 1


def lorentz(x, x0, sig, amp):
    return (amp/(2*np.pi)*sig/((x-x0)**2+sig**2/4))


def gaussian(x, x0, sig, amp):
    return (amp/(sig*np.sqrt(2*np.pi))*np.exp(-((x-x0)**2)/(2*sig**2)))
