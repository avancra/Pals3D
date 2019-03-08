===============================================
Pals3D
===============================================

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

License
============

Pals3D is distributed under the BSD 3-Clause ("BSD New" or "BSD Simplified") License.
