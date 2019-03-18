===============================================
Pals3D
===============================================
|zenodo-doi| |rtd-status| 

.. |zenodo-doi| image:: https://zenodo.org/badge/DOI/10.5281/zenodo.2590979.svg
    :target: https://doi.org/10.5281/zenodo.2590979
    :alt: DOI
    
.. |rtd-status| image::  https://readthedocs.org/projects/pals3d/badge/?version=latest
    :target: https://pals3d.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

The Pals3D software is meant for performing Positron Annihilation Lifetime Spectroscopy measurements with two different modes for double and triple coincidences. It is designed to support the use of a PicoQuant Time-Correlated Single Photon Counting (TCSPC) `TimeHarp 260 PCIe card <https://www.picoquant.com/products/category/tcspc-and-time-tagging-modules/timeharp-260-tcspc-and-mcs-board-with-pcie-interface>`_ as acquisition system. The TimeHarp 260 (TH260) allows the accurate determination of arrival times of photons with high counting rates. Timestamped events are then filtered and sorted to produce lifetime spectrum histograms as output files, that could be further processed by dedicated tools for lifetime extraction (not provided by Pals3D).

Documentation
=============

Full documentation and description of the features of Pals3D can be found under: http://pals3d.readthedocs.io

The Pals3D software was based on the demos code from PicoQuant:

`Github PicoQuant-Time-Tagged-File-Format-Demos repository <https://github.com/PicoQuant/PicoQuant-Time-Tagged-File-Format-Demos>`_

`PicoQuant GitHub TH260Lib demos repository <https://github.com/PicoQuant/TH260-Demos>`_

Installation
============

Clone the repository to get a copy of the source code:

.. code-block:: bash

    git clone https://github.com/avancra/Pals3D.git
    cd Pals3D/pals3D
    python pals3D.py

Citation
========

If you used Pals3D in research work of any kind or in a publication, please acknowledge its author(s) by one of the following methods.

If you want to cite all versions of Pals3D, please use the DOI 10.5281/zenodo.2590978

Alternatively, you may prefer to cite the current version of Pals3D:
DOI 10.5281/zenodo.2590979

For citation format, you can either use the one below, or go to `the project publication page <https://doi.org/10.5281/zenodo.2590979>`_ to get other citation export options.

Default citation format:

*Aurélie Vancraeyenest. (2019, March 12). Pals3D - A data acquisition software for positron annihilation lifetime spectroscopy (Version v1.0). Zenodo. http://doi.org/10.5281/zenodo.2590979*





License
============

Pals3D is distributed under the GNU General Public License Version 3 (GPL-3.0).
