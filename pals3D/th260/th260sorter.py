# This file is part of Pals3D
#
# TH260Sorter is meant to sort data from a PicoQuant TimeHarp 260 Pico
# via TH260LIB.DLL v 3.1. for applications to positron annihilation
# lifetime spectroscopy.
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
# Based on demo code from:
# Keno Goertz, PicoQuant GmbH, February 2018
#

from collections import deque
import time

from PyQt5 import QtCore
import numpy as np

from toolbox import utils as ut


class SortingWorker(QtCore.QObject):
    """
    Data sorting class for data received from a TH260 PicoQuant card

    Inherit from QObect to use Qt signal and slot logic for receiving
    and sorting data. Can then be easily used in a GUI application

    Parameters
    ----------
    kwargs : kwargs
        Keyword arguments passed from the main thread

    Attributes
    ----------
    dataArray : dict
    dataDeck : deque
    islastEvent : bool
    globRes : double
    resultArray_01 : list
    resultArray_02 : list
    resultArray_12 : list

    Keyword Args
    ------------
    sortingType : str
        '2C' or '3C'
    timeGate : int
        Long time gate for positron lifetime (in ps)
    timeRes : int
        Short time gate for 511 MeV photons (in ps)
    filename : str
        Filename base for output file
    CFDset : dict
        Dictionnary of all the CFD settings for all channels
    acqTime : int
        Acquisition time (in min)
    nftot : int
        Total number of files during current measurement

    """

    COINCRATE = QtCore.pyqtSignal(int)  #: :obj:pyqtSignal(int)
    NEW_OUTPUT = QtCore.pyqtSignal(str)  #: :obj:pyqtSignal(str)

    T2WRAPAROUND_V1 = 33552000  #: int : Wraparound for version 1
    T2WRAPAROUND_V2 = 33554432  #: int : Wraparound for version 2
    VERSION = 2  #: int: Version ==> remove?

    def __init__(self, **kwargs):
        """Constructor method of the TH260sorter class"""
        super(SortingWorker, self).__init__()
        self.kwargs = kwargs
        self.globRes = 25.0e-12
        self.resultArray_01 = list()
        self.resultArray_02 = list()
        self.resultArray_12 = list()
        self.dataArray = dict([('01', self.resultArray_01),
                               ('02', self.resultArray_02),
                               ('12', self.resultArray_12)])

        self.dataDeck = deque(maxlen=500)
        self.islastEvent = False

    def newMeasurement(self, noFile):
        """
        Initialise class attributes for new measurement

        Parameters
        ----------
        noFile : int
            File numero in case of multiple file acquisition

        """

        self.dataDeck.clear()
        self.dataArray['01'] = list()
        self.dataArray['02'] = list()
        self.dataArray['12'] = list()
        self.sortingType = self.kwargs["sortingType"]
        self.timeGate = self.kwargs["timeGate"]
        self.timeRes = self.kwargs["timeRes"]
        self.file = self.kwargs["filename"]
        self.cfd = self.kwargs["CFDset"]
        self.oflcorrection = 0
        self.islastEvent = False

    def saveData(self, noFile, **kwargs):
        """
        Do histogramming of the whole data set and save to files

        Parameters
        ----------
        noFile : int
            Numero of the current acquisition file to be appended to
            the filename base.
        """

        self.NEW_OUTPUT.emit("Saving data...")
        try:
            filebase, extension = self.file.rsplit(sep=".", maxsplit=1)
        except ValueError:
            filebase = self.file

        outputFileName = "".join((filebase,
                                  "_",
                                  str(noFile).zfill(3)))

        # Saving raw dT for each channel for triple coinc mode
        if self.sortingType == '3C':
            evtl = [(self.dataArray['01'][i],
                     self.dataArray['02'][i],
                     self.dataArray['12'][i])
                    for i in range(len(self.dataArray['01']))]
            np.save(outputFileName, evtl)

        # Do histogramming
        rmax = int(self.timeGate)
        # We want bins centered on multiple of 25ps
        bins_sync = np.arange(-12.5, rmax+13, 25)
        bins_chn = np.arange(-(rmax//2+12.5), rmax//2+13, 25)
        histo01, bin_edges01 = np.histogram(np.array(self.dataArray['01']),
                                            bins=bins_sync,
                                            range=[-12.5, rmax+13])
        histo02, bin_edges02 = np.histogram(np.array(self.dataArray['02']),
                                            bins=bins_sync,
                                            range=[0, rmax])
        histo12, bin_edges12 = np.histogram(np.array(self.dataArray['12']),
                                            bins=bins_chn,
                                            range=[(rmax//2+12.5),
                                                   rmax//2+12.5])
        # Saving all 3 hist at once
        # bincenters01/02  histo01  histo02  bincenters12  histo12
        histos = np.array([0.5*(bin_edges01[1:]+bin_edges01[:-1]),
                           histo01, histo02,
                           0.5*(bin_edges12[1:]+bin_edges12[:-1]),
                           histo12])
        np.savetxt(outputFileName+'.hst', histos.T, fmt='%10i',
                   header=("Measurement date : {0}"
                           "\nCFD settings:"
                           "\nChannel |\tCFD ZeroCross |\tCFD level |\tOffset"
                           "\nSync \t {z0} mV \t {l0} mV \t{o0} ps"
                           "\nChn1 \t {z1} mV \t {l1} mV \t{o1} ps"
                           "\nChn2 \t {z2} mV \t {l2} mV \t{o2} ps"
                           "\nAcquisition settings:"
                           "\nMode: {m} |\t long gate: {lg} ps \t"
                           "|\t short gate: {sg} ps"
                           "\nAcquisition time: {at:.0f} min \t"
                           "|\t file #{nf} out of {nftot}"
                           "\n\ntime\tsync-1 \t sync-2 \t time \t chn1-chn2")
                   .format(time.asctime(),
                           z0=self.cfd['zero0'],
                           l0=self.cfd['lev0'],
                           o0=self.cfd['off0'],
                           z1=self.cfd['zero1'],
                           l1=self.cfd['lev1'],
                           o1=self.cfd['off1'],
                           z2=self.cfd['zero2'],
                           l2=self.cfd['lev2'],
                           o2=self.cfd['off2'],
                           m=self.sortingType,
                           lg=self.timeGate,
                           sg=self.timeRes,
                           at=self.kwargs['acqTime'],
                           nf=noFile+1,
                           nftot=self.kwargs['nftot']),
                   comments='#', delimiter='\t')

    def _gotPhoton(self, recNum, timeTag, channel, dtime):
        """
        Append real photon events to dataDeck

        parameters
        ----------
        recNum : int
            Record numero
        timeTag: int
            Timetag corrected by the overflow tags with respect to the
            overall measurment start (tick resolution 25 ps)
        channel: int
            Channel number: 0 (sync), 1-2 (channel)
        dtime: int
            Real time : timeTag * self.globRes * 1e12
        """
        self.dataDeck.append((recNum, channel, timeTag,
                              timeTag * self.globRes * 1e12))
        self.sortDeck()

    @QtCore.pyqtSlot()
    def processLastEvents(self):
        """Force the processing of the last events to empty dataDeck"""

        self.islastEvent = True
        self.sortDeck()

    def sortDeck(self):
        """
        Check if the data deque is full to start the sorting according
        to the sortingType ('2C' or '3C')
        """

        if ((len(self.dataDeck) == self.dataDeck.maxlen)
           or (self.islastEvent is True)):
            if self.sortingType is '2C':
                n2Dcoinc = self._2Cfiltering()
                self.COINCRATE.emit(n2Dcoinc)
            elif self.sortingType is '3C':
                n3Dcoinc = self._3Cfiltering()
                self.COINCRATE.emit(n3Dcoinc)

    def _2Cfiltering(self):
        """
        Process the events into double coincidence events

        Use the pairwise function of the utils module to look at each
        pair of successive photons and determine if they are recorded
        in the timeGate time interval, and if they are issued from
        different channels.
        If so, store the time difference into the corresponding list
        of the dataArray dict.

        Warnings
        --------
        Note that we are looking at paires only, so in case of true
        triple coinc, we might miss the coinc between first and 3rd
        event. It doesn't matter for resolution with Co measurements,
        but can have a slight impact for true experiments
        """

        # !!! Note that we are looking at paires only, so in case of
        # true triple coinc, we might miss the coinc between first and 3rd evt.
        # Doesn't matter for resolution with Co, but can have a slight impact
        # for true experiments

        keeplast = False
        ncoinc = 0
        for pair in ut.pairwise(self.dataDeck):
            is2D = (pair[0][1] != pair[1][1])
            if not is2D:
                keeplast = True
                continue
            chnPair = str(int(pair[0][1])) + str(int(pair[1][1]))
            dtime = pair[1][3] - pair[0][3]
            isInGate = (dtime < self.timeGate)
            if not isInGate:
                keeplast = True
                continue
            if chnPair in {'01', '02', '12'}:
                self.dataArray[chnPair].append(dtime)
            else:
                self.dataArray[chnPair[::-1]].append(-dtime)
            keeplast = False
            ncoinc += 1
        if keeplast is True:
            lastEvent = self.dataDeck.pop()
            self.dataDeck.clear()
            self.dataDeck.append(lastEvent)
        else:
            self.dataDeck.clear()
        return ncoinc

    def _3Cfiltering(self):
        """
        Process the events into triple coincidence events

        Use the tripletwise function of the utils module to look at each
        triplet of successive photons and determine if they are real
        triple coincidence events.

        A triple coicidence event is defined as follow:
        three successive events are recorded from three different
        channels and the first event should be recorded in the sync
        channel (chan 0). Further requirements are that the time
        difference between records in channel 1 and 2 should be less
        than timeRes and that the three events are recorded within the
        timeGate time interval.

        If so, store the time difference into the corresponding list
        of the dataArray dict.

        """

        keeplast = False
        ncoinc = 0
        for triplet in ut.tripletwise(self.dataDeck):
            is3D = (triplet[0][1] == 0 and
                    triplet[1][1] != 0 and
                    triplet[2][1] != 0 and
                    triplet[1][1] != triplet[2][1])

            if not is3D:
                keeplast = True
                continue

            isEv1inChn1 = triplet[1][1] == 1
            dtimeS1 = triplet[1][3] - triplet[0][3]
            dtimeS2 = triplet[2][3] - triplet[0][3]
            dtime12 = triplet[2][3] - triplet[1][3]
            isInGate = (dtimeS1 < self.timeGate and
                        dtimeS2 < self.timeGate and
                        dtime12 < self.timeRes)
            if not isInGate:
                keeplast = True
                continue

            if isEv1inChn1:
                self.dataArray['01'].append(dtimeS1)
                self.dataArray['02'].append(dtimeS2)
                self.dataArray['12'].append(dtime12)
            else:
                self.dataArray['01'].append(dtimeS2)
                self.dataArray['02'].append(dtimeS1)
                self.dataArray['12'].append(-dtime12)

            keeplast = False
            ncoinc += 1

        # Clear the deque and keep the last 2 events if keeplast is True
        if keeplast is True:
            lastEvents = [self.dataDeck.pop() for _ in range(2)
                          if keeplast is True]
            self.dataDeck.clear()
            self.dataDeck.append(lastEvents[-1])
            self.dataDeck.append(lastEvents[-2])
        else:
            self.dataDeck.clear()
        return ncoinc

    def sortBuffer(self, buffer, nrecords):
        """
        Decode buffer individual events to produce a time tagged event

        Parameters
        ----------
        buffer : object - ctype array buffer
            Raw data buffer received over a signal from the acquisition
            thread.
        nrecords : int
            Total number of records in the buffer
        """
        # data received over a signal
        self.dataToSort = buffer  # received from a signal ctype array
        self.numRecords = nrecords  # received from a signal
        for recNum in range(0, self.numRecords):
            try:
                recordData = "{0:0{1}b}".format(self.dataToSort[recNum], 32)
            except:  # TODO: deal with this bare exception
                print("The file ended earlier than expected, at record %d/%d."
                      % (recNum, self.numRecords))

            special = int(recordData[0:1], base=2)
            channel = int(recordData[1:7], base=2)
            timetag = int(recordData[7:32], base=2)

            if special == 1:
                if channel == 0x3F:  # Overflow
                    # Number of overflows in nsync. If old version, it's an
                    # old style single overflow

                    if self.VERSION == 1:
                        self.oflcorrection += self.T2WRAPAROUND_V1
                    else:
                        if timetag == 0:  # old style overflow shouldn't happen
                            self.oflcorrection += self.T2WRAPAROUND_V2
                        else:
                            self.oflcorrection += self.T2WRAPAROUND_V2*timetag

                if channel >= 1 and channel <= 15:   # markers
                    truetime = self.oflcorrection + timetag
                if channel == 0:   # sync
                    truetime = self.oflcorrection + timetag
                    self._gotPhoton(recNum, truetime, 0, 0)
            else:   # regular input channel
                truetime = self.oflcorrection + timetag
                self._gotPhoton(recNum, truetime, channel+1, 0)
