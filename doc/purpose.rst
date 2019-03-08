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

License
========

**Host software**
  If not stated otherwise, the present software is distributed under the BSD 3-Clause (“BSD New” or “BSD Simplified”) License:

  Note: This license has also been called the "New BSD License" or "Modified BSD License". See also the 2-clause BSD License.

  Copyright 2019 Aurélie Vancraeyenest

  Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

  1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.

  2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.

  3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


**Firmware**
  The PicoQuant DLL is not included with the current software and is subject to its own License and restriction. It can be purchase from PicoQuant directly together with the TimeHarp 260 system.
