# -*- coding: utf-8 -*-
# TH260Sorter is meant to sort data from a PicoQuant TimeHarp 260 Pico
# via TH260LIB.DLL v 3.1. for applications to positron annihilation
# lifetime spectroscopy.
#
# The class is designed so it use PyQt signals and slots to
# communicate between methods, so that it can be easily used with
# threads and GUI.
#
# (c) Aurelie Vancraeyenest 2018-2019
#
# Based on demo code from:
# Keno Goertz, PicoQuant GmbH, February 2018

from collections import deque

from PyQt5 import QtCore
import numpy as np

import toolbox.utils as ut


class SortingWorker(QtCore.QObject):
    """
        Data sotring class for data received for a TH260 PicoQuant card

        Inherit from QObect to use Qt signal and slot logic for receiving
        and sorting data. Can then be easily used in a GUI application

    """
    # TODO: Define here the signals
    COINCRATE = QtCore.pyqtSignal(int)
    NEW_OUTPUT = QtCore.pyqtSignal(str)

    T2WRAPAROUND_V1 = 33552000
    T2WRAPAROUND_V2 = 33554432
    VERSION = 2

    def __init__(self, **kwargs):
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
        # ???: QMutex here?

        self.dataDeck.clear()
        self.dataArray['01'] = list()
        self.dataArray['02'] = list()
        self.dataArray['12'] = list()
        self.sortingType = self.kwargs["sortingType"]
        self.timeGate = self.kwargs["timeGate"]
        self.timeRes = self.kwargs["timeRes"]
        self.file = self.kwargs["filename"]
        self.doHist = self.kwargs["doHist"]
        self.oflcorrection = 0
        self.islastEvent = False

    def saveData(self, noFile):
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
        if self.doHist:
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
                       header="histos \n bin\tsync-1\tsync-2\tbin\tchn1-chn2",
                       comments='#', delimiter='\t')

    def _gotPhoton(self, recNum, timeTag, channel, dtime):
        """ Deals with real photon events

            If global variable sortingType is not None, sort the events
            according to the specified sortingType (2C, 3C)

            parameters:
                timeTag: int

                channel: int

                dtime: int
        """
        self.dataDeck.append((recNum, channel, timeTag,
                              timeTag * self.globRes * 1e12))
        self.sortDeck()

    @QtCore.pyqtSlot()
    def processLastEvents(self):
        self.islastEvent = True
        self.sortDeck()

    def sortDeck(self):
        if ((len(self.dataDeck) == self.dataDeck.maxlen)
           or (self.islastEvent is True)):
            if self.sortingType is '2C':
                n2Dcoinc = self._2Cfiltering()
                self.COINCRATE.emit(n2Dcoinc)
            elif self.sortingType is '3C':
                n3Dcoinc = self._3Cfiltering()
                self.COINCRATE.emit(n3Dcoinc)

    def _2Cfiltering(self):
        """ # TODO: doc 2C"""

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
        """ # TODO: doc 3C """

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
