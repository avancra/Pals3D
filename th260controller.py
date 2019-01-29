# -*- coding: utf-8 -*-
# TH260Controller is meant to access a PicoQuant TimeHarp 260 Pico
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

import time
import ctypes as ct
from ctypes import byref
from PyQt5 import QtCore


class TH260Controller(QtCore.QObject):
    """
    TH260Controller is meant to access a PicoQuant TimeHarp 260 Pico
    via TH260LIB.DLL v 3.1. for applications to positron annihilation
    lifetime spectroscopy.

    """

    # Constants from the DLL th260defin.h
    LIB_VERSION = "3.1"
    MAXDEVNUM = 4
    MODE_T2 = 2
    MODE_T3 = 3
    MAXLENCODE = 5
    MAXINPCHAN = 2
    TTREADMAX = 131072
    FLAG_OVERFLOW = 0x0001
    FLAG_FIFOFULL = 0x0002
    CFDLVLMIN = -1200
    CFDLVLMAX = 0
    CFDZCMIN = -40
    CFDZCMAX = 0
    CHANOFFSMIN = -99999	   	# for TH260_SetSyncChannelOffset
    CHANOFFSMAX = 99999         # and TH260_SetInputChannelOffset
    ACQTMIN = 1		   	        # ms, for TH260_StartMeas
    ACQTMAX = 360000000         # ms  (100*60*60*1000ms = 100h)
    TH260LIB = ct.CDLL("th260lib64.dll")

    # signals
    NEW_OUTPUT = QtCore.pyqtSignal(str)
    WARNING = QtCore.pyqtSignal(str)
    PROGRESS = QtCore.pyqtSignal(str, int)  # str = "file"
    DATA = QtCore.pyqtSignal(object, int)
    ERROR = QtCore.pyqtSignal(tuple)
    ACQ_ENDED = QtCore.pyqtSignal()
    DEVINIT = QtCore.pyqtSignal(bool)
    UPDATECountRate = QtCore.pyqtSignal()

    def __init__(self):
        """
        """
        super(TH260Controller, self).__init__()
        # Setting variables
        self.mode = self.MODE_T2
        # Following variables are only meaningfull when used
        # without a GUI, otherwise they are set through GUI
        self.tacq = 60000               # Measurement time in millisec,
        self.syncDivider = 1            # you can change this, READ MANUAL!
        self.syncCFDZeroCross = -10     # you can change this (in mV)
        self.syncCFDLevel = -30         # you can change this (in mV)
        self.syncOffset = 0             # you can change this (in mV)
        self.inputCFDZeroCross = [-10, -10]  # you can change this (in mV)
        self.inputCFDLevel = [-30, -30]      # you can change this (in mV)
        self.inputOffset = [270, 1184]       # you can change this (in mV)
        self.countRates = [0, 0, 0, 0]

        # Variables to store information red from DLLs
        self.buffer = (ct.c_uint * self.TTREADMAX)()
        self.dev = []
        self.libVersion = ct.create_string_buffer(b"", 8)
        self.hwSerial = ct.create_string_buffer(b"", 8)
        self.hwPartno = ct.create_string_buffer(b"", 8)
        self.hwVersion = ct.create_string_buffer(b"", 16)
        self.hwModel = ct.create_string_buffer(b"", 16)
        self.errorString = ct.create_string_buffer(b"", 40)
        self.numChannels = ct.c_int()
        self.resolution = ct.c_double()
        self.syncRate = ct.c_int()
        self.countRate = ct.c_int()
        self.flags = ct.c_int()
        self.nRecords = ct.c_int()
        self.ctcstatus = ct.c_int()
        self.elapsedTime = ct.c_double()
        self.warnings = ct.c_int()
        self.warningstext = ct.create_string_buffer(b"", 16384)

        # Define here signals logic connections
        self.NEW_OUTPUT.connect(self.printOutput)
        self.WARNING.connect(self.printOutput)

    # Here define the default behaviour of slots to handle signals in
    # case no GUI and/or no other slots are defined.
    # REMEMBER to disconnect them before defining new slots, espcially
    # in case console output is not desired.
    @QtCore.pyqtSlot(str)
    def printOutput(self, text):
        print(text)

    # ----------------- dealing with device ---------------------- #
    def closeDevices(self):
        """ Close the currently opened devices
        """
        for i in range(0, self.MAXDEVNUM):
            self.TH260LIB.TH260_CloseDevice(ct.c_int(i))

    def tryfunc(self, retcode, funcName, measRunning=False):
        """ Check for errors when executing a function

            If an error is raised, print the corresponding error message,
            stop the TTTR measurement if needed and close the device

            Parameters
            -------
            retcode: int
                code return by the function funcName
            funcName: str
                Name of the function being executed
            measRunning: bool, default False
                specify if TTTR measurement is running.
                If True, the measurement will be stopped in case of
                an error is encountered before closing the device
        """
        if retcode < 0:
            self.TH260LIB.TH260_GetErrorString(self.errorString,
                                               ct.c_int(retcode))
#            # TODO: transform that to logging
#            self.file.write("TH260_%s error %d (%s). Aborted."
#                            % (funcName, retcode,
#                               self.errorString.value.decode("utf-8")))
            self.WARNING.emit("TH260_%s error %d (%s). Aborted."
                              % (funcName, retcode,
                                 self.errorString.value.decode("utf-8")))
            if measRunning:
                self.stoptttr()
            else:
                self.closeDevices()

    def searchDevices(self):
        """ Search and list all available devices on the host computer
        """
        self.TH260LIB.TH260_GetLibraryVersion(self.libVersion)
        self.NEW_OUTPUT.emit("Library version is %s"
                             % self.libVersion.value.decode("utf-8"))
        if self.libVersion.value.decode("utf-8") != self.LIB_VERSION:
            self.WARNING.emit(
                    """Warning: The application was built for version %s
                    \nCurrent DDL version is  %s"""
                    % (self.LIB_VERSION,
                       self.libVersion.value.decode("utf-8")))

        self.NEW_OUTPUT.emit(
                "\nSearching for TimeHarp devices... \n Devidx     Status")

        for i in range(0, self.MAXDEVNUM):
            retcode = self.TH260LIB.TH260_OpenDevice(ct.c_int(i),
                                                     self.hwSerial)
            if retcode == 0:
                self.NEW_OUTPUT.emit("  %1d        S/N %s"
                                     % (i,
                                        self.hwSerial.value.decode("utf-8")))
                self.dev.append(i)
            else:
                if retcode == -1:  # TH260_ERROR_DEVICE_OPEN_FAIL
                    self.NEW_OUTPUT.emit("  %1d        no device" % i)
                else:
                    self.TH260LIB.TH260_GetErrorString(self.errorString,
                                                       ct.c_int(retcode))
                    self.WARNING.emit("  %1d        %s"
                                % (i, self.errorString.value.decode("utf8")))
        if len(self.dev) < 1:
            self.NEW_OUTPUT.emit("No device available.")
            self.WARNING.emit("Waring: no device available !")
            self.closeDevices()
        self.NEW_OUTPUT.emit("\nUsing device #%1d" % self.dev[0])

    def initialization(self):
        """
            Initialize communication with TH260 pico card

            When initializationg is successfuly done, emit a DEVINIT signal
            with True value
        """
        self.NEW_OUTPUT.emit("\nInitializing the device...")
        # with internal clock
        self.tryfunc(self.TH260LIB.TH260_Initialize(
                ct.c_int(self.dev[0]), ct.c_int(self.mode)), "Initialize")

        self.tryfunc(self.TH260LIB.TH260_GetHardwareInfo(self.dev[0],
                                                         self.hwModel,
                                                         self.hwPartno,
                                                         self.hwVersion),
                     "GetHardwareInfo")
        self.NEW_OUTPUT.emit("Found Model %s Part no %s Version %s"
                             % (self.hwModel.value.decode("utf-8"),
                                self.hwPartno.value.decode("utf-8"),
                                self.hwVersion.value.decode("utf-8")))

        self.tryfunc(self.TH260LIB.TH260_GetNumOfInputChannels(
                     ct.c_int(self.dev[0]),
                     byref(self.numChannels)),
                     "GetNumOfInputChannels")
        self.NEW_OUTPUT.emit("Device has %i input channels."
                             % self.numChannels.value)
        self.DEVINIT.emit(True)

    def configureSetting(self):
        """
            Set the card paramaters before starting a measurement

            Parameters are either change in the init function, or acquired
            through an external script or GUI.
            Here, we only set CFD parameters and channel offsets
            and the device resolution should always be 25 ns as we are
            running in T2 mode only
        """

        self.tryfunc(self.TH260LIB.TH260_SetSyncDiv(
                     ct.c_int(self.dev[0]),
                     ct.c_int(self.syncDivider)),
                     "SetSyncDiv")

        if self.hwModel.value.decode("utf-8") == "TimeHarp 260 P":
            self.tryfunc(self.TH260LIB.TH260_SetSyncCFD(
                         ct.c_int(self.dev[0]),
                         ct.c_int(self.syncCFDLevel),
                         ct.c_int(self.syncCFDZeroCross)),
                         "SetSyncCFD")
            # input settings for all channels
            for i in range(0, self.numChannels.value):
                self.tryfunc(self.TH260LIB.TH260_SetInputCFD(
                             ct.c_int(self.dev[0]), ct.c_int(i),
                             ct.c_int(self.inputCFDLevel[i]),
                             ct.c_int(self.inputCFDZeroCross[i])),
                             "SetInputCFD")

        self.tryfunc(self.TH260LIB.TH260_SetSyncChannelOffset(
                     ct.c_int(self.dev[0]),
                     ct.c_int(self.syncOffset)),
                     "SetSyncChannelOffset")

        for i in range(0, self.numChannels.value):
            self.tryfunc(self.TH260LIB.TH260_SetInputChannelOffset(
                         ct.c_int(self.dev[0]),
                         ct.c_int(i),
                         ct.c_int(self.inputOffset[i])),
                         "SetInputChannelOffset")
#        uncomment for console output in needed
#        print("\nMeasurement settings:")
#        print("SyncCFDZeroCross  : %d" % self.syncCFDZeroCross)
#        print("SyncCFDLevel      : %d" % self.syncCFDLevel)
#        print("InputCFDZeroCross : %d" % self.inputCFDZeroCross[0])
#        print("InputCFDLevel     : chn1: %d" % self.inputCFDLevel[0])

#        self.tryfunc(self.TH260LIB.TH260_SetBinning(
#              ct.c_int(self.dev[0]), ct.c_int(self.binning)), "SetBinning")
#        self.tryfunc(self.TH260LIB.TH260_SetOffset(
#              ct.c_int(self.dev[0]), ct.c_int(self.offset)), "SetOffset")
        self.tryfunc(self.TH260LIB.TH260_GetResolution(
              ct.c_int(self.dev[0]), byref(self.resolution)), "GetResolution")
        self.NEW_OUTPUT.emit("Resolution is %1.1lfps" % self.resolution.value)

        self.NEW_OUTPUT.emit("\nMeasuring input rates...")

        # After Init or SetSyncDiv allow 150 ms for valid count rate readings
        time.sleep(0.15)

        self.getCountRates()
        self.NEW_OUTPUT.emit("\nCountrate[sync]=%1d/s" % self.countRates[0])
        self.NEW_OUTPUT.emit("Countrate[chn 1]=%1d/s" % (self.countRates[1]))
        self.NEW_OUTPUT.emit("Countrate[chn 2]=%1d/s" % (self.countRates[2]))

        # after getting the count rates you can check for warnings
        self.tryfunc(self.TH260LIB.TH260_GetWarnings(
                     ct.c_int(self.dev[0]),
                     byref(self.warnings)),
                     "GetWarnings")

        if self.warnings.value != 0:
            self.TH260LIB.TH260_GetWarningsText(ct.c_int(self.dev[0]),
                                                self.warningstext,
                                                self.warnings)
            self.WARNING.emit("%s" % self.warningstext.value.decode("utf-8"))

    # ----------- data aqcuisition ---------------- #
    def getCountRates(self):
        """ Get the count rates for each channels and store them as a list
        """
        self.tryfunc(self.TH260LIB.TH260_GetSyncRate(
                     ct.c_int(self.dev[0]),
                     byref(self.syncRate)),
                     "GetSyncRate")
        self.countRates[0] = self.syncRate.value

        for i in range(0, self.numChannels.value):
            self.tryfunc(self.TH260LIB.TH260_GetCountRate(
                         ct.c_int(self.dev[0]),
                         ct.c_int(i),
                         byref(self.countRate)),
                         "GetCountRate")
            self.countRates[i+1] = self.countRate.value

    def stoptttr(self):
        """ Stop the ongoing TTTR measurement
        """
        self.tryfunc(self.TH260LIB.TH260_StopMeas(ct.c_int(self.dev[0])),
                     "StopMeas")

    def startAcquisition(self):
        """
            Start an acquisition
        """
        # TODO: clean up a bit
        self.NEW_OUTPUT.emit("Starting data collection...\n")

        progress = 0
        # Uncomment following 2 lines in case of console oupput
        # remember to add "import sys" in header file
#        sys.stdout.write("\nProgress:%12u" % progress)
#        sys.stdout.flush()

        self.tryfunc(self.TH260LIB.TH260_StartMeas(
                     ct.c_int(self.dev[0]),
                     ct.c_int(self.tacq)),
                     "StartMeas")

        measEnded = False
        measCrashed = False
        while not (measEnded or measCrashed):
            self.tryfunc(self.TH260LIB.TH260_GetFlags(
                         ct.c_int(self.dev[0]),
                         byref(self.flags)),
                         "GetFlags")

            if self.flags.value & self.FLAG_FIFOFULL > 0:
                self.WARNING.emit("Measurment failed: \nFiFo Overrun!")
                self.stoptttr()
                measCrashed = True
                continue

            self.tryfunc(self.TH260LIB.TH260_ReadFiFo(
                        ct.c_int(self.dev[0]),
                        byref(self.buffer),
                        self.TTREADMAX,
                        byref(self.nRecords)),
                        "ReadFiFo", measRunning=True)

            if self.nRecords.value > 0:
                # We could just iterate through our buffer with a for loop,
                # however, this is slow and might cause a FIFO overrun.
                # So instead, we shrinken the buffer to its appropriate
                # length with array slicing, which gives us a python list.
                # This list then needs to be converted back into a ctype
                # array which can be written at once to the output file
                self.DATA.emit((ct.c_uint*self.nRecords.value)
                               (*self.buffer[0:self.nRecords.value]),
                               self.nRecords.value)
                progress += self.nRecords.value
                self.countRates[3] += self.nRecords.value
#                Uncomment following 2 lines in case of console oupput
#                remember to add "import sys" in header file
#                sys.stdout.write("\rProgress:%12u" % progress)
#                sys.stdout.flush()

                self.tryfunc(self.TH260LIB.TH260_GetElapsedMeasTime(
                                self.dev[0],
                                ct.byref(self.elapsedTime)),
                             "GetElapsedMeasTime")
#                Uncomment following 2 lines in case of console oupput
#                remember to add "import sys" in header file
#                sys.stdout.write("\n time  %4f " % self.elapsedTime.value)
#                sys.stdout.flush()
                self.PROGRESS.emit("file", self.elapsedTime.value)

            else:
                self.tryfunc(self.TH260LIB.TH260_CTCStatus(
                             ct.c_int(self.dev[0]),
                             byref(self.ctcstatus)),
                             "CTCStatus")
                if self.ctcstatus.value > 0:
                    self.ACQ_ENDED.emit()
                    self.NEW_OUTPUT.emit(
                            "\nMeasurement ended normally with {} events"
                            .format(progress))
                    self.tryfunc(self.TH260LIB.TH260_StopMeas(
                                 ct.c_int(self.dev[0])),
                                 "StopMeas")
                    measEnded = True

            self.getCountRates()
            self.UPDATECountRate.emit()
            # ??? look for warnings here?
            if measCrashed:
                self.NEW_OUTPUT.emit("Measurement crashed after {} sec"
                                     .format(self.elapsedTime.value*1000))
                break
