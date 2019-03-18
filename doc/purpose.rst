#######
Purpose
#######

Introduction
============

The Pals3D software is meant for performing Positron Annihilation Lifetime Spectroscopy measurements with two different modes for double and triple coincidences. It is designed to support the use of a PicoQuant Time-Correlated Single Photon Counting (TCSPC) TimeHarp 260 Pico PCIe card as acquisition system. The TimeHarp 260 (TH260) allows the accurate determination of arrival times of photons with high counting rates. Timestamped events are then filtered and sorted to produce lifetime spectrum histograms as output files, that could be further processed by dedicated tools for lifetime extraction (not provided by Pals3D).


.. _install-sect:

Installation
==============

Pals3D source code is freely available on `Github <https://github.com/avancra/Pals3D>`_ 

To start using Pals3D, you can simply clone the repository:

.. code-block:: bash

    git clone https://github.com/avancra/Pals3D.git
    cd Pals3D/pals3D
    python pals3D.py

Citation
========

If you used Pals3D in research work of any kind or in a publication, please acknowledge its author(s) by one of the following methods

If you want to cite all versions of Pals3D, please use the DOI 10.5281/zenodo.2590978

Alternatively, you may prefer to cite the current version of Pals3D:
DOI 10.5281/zenodo.2590979

For citation format, you can either use the one below, or go to `the project publication page <https://doi.org/10.5281/zenodo.2590979>`_ to get other citation export options.

Default citation format:

*Aurélie Vancraeyenest. (2019, March 12). Pals3D - A data acquisition software for positron annihilation lifetime spectroscopy (Version v1.0). Zenodo. http://doi.org/10.5281/zenodo.2590979*


License
========

**Host software**

The present software is distributed under the GNU General Public License version 3 (GPL-3.0) :

Copyright (c) 2018-2019 Aurelie Vancraeyenest

Pals3D is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

Pals3D is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with Pals3D.  If not, see <http://www.gnu.org/licenses/>.


**Firmware**
  The PicoQuant DLL is not included with the current software and is subject to its own License and restriction. It can be purchase from PicoQuant directly together with the TimeHarp 260 system.
