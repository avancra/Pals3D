# This file is part of Pals3D
#
# ---------------------------------------------
#
# Copyright (c) 2018-2019 Aurelie Vancraeyenest 
# ---------------------------------------------
#
# Pals3D is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pals3D is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Pals3D.  If not, see <http://www.gnu.org/licenses/>.
#

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


def plotFitHist(data, figname='fig.pdf', bins=161, rmin=2000, rmax=6000):
    """
    Plot an histogramm and fit with Gaussian and Lorentzian functions

    Parameters
    ----------
    data : np.array
        Input data
    figname : str
        Output filename of the file to save the figure
    bins : int
        Number of equal-width bins in the given range
    rmin : int
        max (most right-end bin edge) of the histogramm
    rmax : int
        min (most left-end bin edge) of the histogramm

    See Also
    --------
    plotHist, plotHists, saveHists
    """
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


def plotHist(data, figname='fig.pdf', bins=161, rmin=2000, rmax=6000,
             logY=False):
    """
    Plot an histogramm and save the output spectrum as a figure

    Parameters
    ----------
    data : np.array_like
        Input data
    figname : str
        Output filename of the file to save the figure
    bins : int
        Number of equal-width bins in the given range
    rmin : int
        max (most right-end bin edge) of the histogramm
    rmax : int
        min (most left-end bin edge) of the histogramm
    logY : bool
        Allow to plot the histogram in a logarithmique scale

    See Also
    --------
    plotHist, plotHists, saveHists
    """
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


def plotHists(data, figname='fig.pdf', bins=161, rmin=2000, rmax=6000,
              logY=False, style='-'):
    """
    Plot multiple histograms and save the output spectrum as a figure

    Parameters
    ----------
    data : np.array_like
        Input data as multiple numpy arrays
    figname : str
        Output filename of the file to save the figure
    bins : int
        Number of equal-width bins in the given range
    rmin : int
        max (most right-end bin edge) of the histogramm
    rmax : int
        min (most left-end bin edge) of the histogramm
    logY : bool
        Allow to plot the histogram in a logarithmique scale
    style : str
        Plotting style, see matplotlib for more info

    See Also
    --------
    plotHist, plotHists, saveHists
    """
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


def saveHists(data, filebase='histo', bins=161, rmin=2000, rmax=6000,
              useChnEnding=False):
    """
    Sort each data-set in data into histogram and save as text files

    Parameters
    ----------
    data : list of np.array_like
        Input data asa list of several numpy arrays
    filebase : str
        Output filename base that will serve to form the output
        filename of each text file generated.
        Output file format is ASCII
    bins : int
        Number of equal-width bins in the given range
    rmin : int
        max (most right-end bin edge) of the histogramm
    rmax : int
        min (most left-end bin edge) of the histogramm
    useChnEnding : bool
        If Ture, channel ending type are inserted in the filename
        before the file extension. In False, an integer reprenseting
        the position in the input dataset is inserted instead

    See Also
    --------
    plotHist, plotHists, saveHists
    """
    ii = 0
    chnEndings = ('01', '02', '12')
    for data in data:
        histo, bin_edges = np.histogram(np.array(data), bins=bins,
                                        range=[rmin, rmax])
        if useChnEnding is True:
            filename = filebase + '_' + chnEndings[ii] + '.hst'
        else:
            filename = filebase + '_' + str(ii) + '.txt'
        np.savetxt(filename, histo, fmt='%i',
                   header="bins: {}\nrange: [{}:{}]".format(bins, rmin, rmax))
        ii += 1


def lorentz(x, x0, sig, amp):
    """ Formula for a Lorentzian
    """
    return (amp/(2*np.pi)*sig/((x-x0)**2+sig**2/4))


def gaussian(x, x0, sig, amp):
    """ Formula for a Gaussian
    """
    return (amp/(sig*np.sqrt(2*np.pi))*np.exp(-((x-x0)**2)/(2*sig**2)))
