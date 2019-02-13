.. _features-sect:

##########
Features
##########

.. _standard-acq-sect:

Standard acquisition mode
==========================

This is the standard acquisition mode for PALS measurements. It is provided with two selectable options from the GUI: double and triple coincidence.

.. _double-mode-sect:

Double coincidence mode
----------------------------

In this mode, only events composed of two consecutive photon events recorded within a given time gate will be considered as meaningful events. The time gate (in ps) for the coincidence is set in the GUI application under the *time gate long* field.

For sorting the double coincidence events, the algorithm make use of a pairwise iterator that go through each pair of successive photon events and check for some conditions to be met.

.. image:: figures/timeScheme2D.png
    :align: center

The scheme above represents a typical event stream as red from the FIFO buffer. The gray box is a representation of the time gate as defined earlier. The sorter will go through each pair of successive photon events and check if the time difference between those two events is lower than the given time gate called *time gate long*. In addition, it makes sure that both events had occurred in different channels. If so, the relative time difference will be stored into an array corresponding to the channels involved.

.. note:: 
    In the current version of the software, the time difference will be count as positive or negative depending on which channel the first event has occurred in. So all events involving channel 1 and 2 will be recorded in the same array, only changing the sign in case the channel 2 event happened before the one in channel 1. This way, both detectors can be aligned with a zero time delay and we still get the full time spectrum at once. By convention, all events with one of the following time structure: (chn0, chn1), (chn0, chn2) or (chn1, chn2) will be recorded with a positive time, whereas every event with time structure (chn1, chn0), (chn2, chn0) or (chn2, chn1) will be considered negative.

At the end of each standard acquisition, histogramming of the three arrays is performed and the resulting histograms are saved to file (see :ref:`standard-output-sect` section).

.. important::
    In the case 2 of the figure example, three events occur in the same time gate and all pair combinations are valid candidates for being considered as double coincidence events. However in the current state of the sorter algorithm only pairs (event 1, event 2) and (event 2, event 3) are examined. The pair (event 1, event 3) is not considered, so in case of a real triple decay event, this pair will be lost. This will not have any consequence for two photon decay physical events (such as :sup:`60`\ Co), but can lead to a loss of statistic in case of three-photon decay physical events. Also, as we have no means to know which pair is a meaningful coincidence event or is not, we decided to keep both events as valid coincidence events. Thus, both time differences will be stored in the corresponding arrays. As the ratio false over real coincidences is expected to be highly is favor of true ones, we expect this to have little effect, and do not distort the time spectrum. 

.. _triple-mode-sect:

Triple coincidence mode
---------------------------

The triple coincidence mode is the standard acquisition mode for PALS measurement with radioactive samples producing high gamma ray background. This requires the additional condition that all of the three photons emitted in the physical process to be detected in a selected time gate.

As in the case of double coincidence mode (see :ref:`double-mode-sect`) the algorithm make use of an iterator to go through each triplet of successive photon events and check for some conditions to be met.

.. image:: figures/timeScheme3D.png
   :align: center

The scheme above represents a typical event stream as read from the FIFO buffer. The gray box is a representation of the time gates. The sorter will go through each triplet of successive photon events and check the following conditions by step:

1. The *is3D* condition is fulfilled when:

   * the first event is recorded in the sync channel (chn 0)
   * the second and third events occurred in channel 1 and channel 2 (regardless of the order)

2. The *isInGate* condition requires to have all the three photons detected within the *time gate long* as in the double coincidence mode. Additionally a second time condition is required to ensure that the time difference between the second and third photons is lower than the *time gate 511* (also called *timeRes* in the code as it is related to the time resolution of the detection system)

If those two conditions are fulfilled, the relative time differences between each channel pair will be stored into an array.

.. important::
    In order for the first condition of the *is3D* condition to be met, it is important to carefully set the time offsets of the channels so that the sync channel timestamp is always lower than the channel 1 and 2.

.. note:: 
    As in the double coincidence mode the time difference between two channels will be count as positive or negative depending on which channel the first event of the pair has occurred in. However, if the time offsets are set as explained in the :ref:`hardware-sect` section, events in sync channel should always occur before those in channel 1 and 2, leading to positive time differences.
    
.. _standard-output-sect:

Output files
-------------

At the end of each standard acquisition, histogramming of the three arrays is performed and the resulting histograms are saved to file. The resulting filename is based on a name base supplied by the user in the GUI application. To the name base is automatically append an additional suffix in the form *_XXX.hst* with XXX being the number of the current acquisition in a three digit format.

By default, a binning of 25 ps is used and the edges of the histograms are defined as follows:

* Sync channel - channel 1 or 2: lower (left end) edge is always 0, and the upper (right end) edge is set as the value of the selected time gate.

* Channel 1 - channel 2: the edges are calculated so that the histogram is centered on the time 0 and its total span is set to the width of the selected time gate. So it will have edges such as [-time gate / 2, time gate / 2].

As the PicoQuant TimeHarp 260 pico has an internal resolution of 25 ps, the central value of the bins has been chosen to be a multiple of 25 ps. Indeed, due to the machine internal round of numbers, having bins edges multiple of 25 ps leads to spectrum distortion.

In addition to the histogram data the output files contain information on the hardware settings and acquisition parameter of the corresponding measurement. Below is an example of the header and first rows of a typical output file.

 | #Measurement date : Tue Feb 12 17:01:22 2019
 | #CFD settings:
 | #Channel |	CFD ZeroCross |	CFD level |	Offset
 | #Sync 	 -10 mV 	 -200 mV 	0 ps
 | #Chn1 	 -10 mV 	 -60 mV 	270 ps
 | #Chn2 	 -10 mV 	 -60 mV 	1184 ps
 | #Acquisition settings:
 | #Mode: 2C |	 long gate: 10000 ps 	|	 short gate: None ps
 | #Acquisition time: 10 min 	|	 file #1 out of 3
 | #
 | #time	sync-1	sync-2	time	chn1-chn2
 | 0	  0 0 -5000  0
 | 25  0 0 -4975  0
 | 50  0 0 -4950  0
 | 75  0 0 -4925  0
 | 100 0 0 -4900  0
 | 125 0 0 -4875  0 

For the triple coincidence mode, an additional output file is produced to allow further filtering of the events. Each triple event is recorded as a list of time differences of the kind: [ :math:`{\Delta}`\ (sync-chn1); :math:`{\Delta}`\ (sync-chn2); :math:`{\Delta}`\ (chn1-chn2)]. All events are then stored in a numpy array that is saved via the *numpy.save* method to an output file with the same file name as the histogram file but with the *.npy* extension.


.. _settings-mode-sect:

Settings mode
==============

Not yet available

.. todo:: implement this

.. _calibration-mode-sect:

60Co calibration
-------------------

.. _offset-opt-mode-sect:

Offset optimization
--------------------

.. _det-char-mode-sect:

Detector characterization
--------------------------


