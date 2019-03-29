# This file is part of Pals3D
#
# Pals3D is a data acquisition software for TimeHarp260 Pico
# for use with positron annihilation lifetime spectroscpoy
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

import sys
import traceback
import os.path
import time
import webbrowser

from PyQt5 import QtWidgets, QtCore, QtGui

import toolbox.utils as ut
import acqGUI
from th260 import th260controller, th260sorter

# put here visual ressources
ICON_OK = ":/icons/ok.png"
ICON_WARNING = ":/icons/warning.png"
VERSION = '1.0'


class MainWindow(QtWidgets.QMainWindow, acqGUI.Ui_MainWindow):
    """ Main instance for the GUI of the hv controller panel """

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.T2applySetBtn.setEnabled(False)
        self.T2startBtn.setEnabled(False)
        self.settings = QtCore.QSettings('Aalto-Antimatter', 'Pals3D')
        self.warnings = 'No warnings'

        self.th260 = th260controller.TH260Controller()
        self.sortingWorker = th260sorter.SortingWorker()
        self.sortingWorker.COINCRATE.connect(self.updateCoincRates)
        self.sortingThread = QtCore.QThread()
        self.sortingWorker.moveToThread(self.sortingThread)

        self.threadpool = QtCore.QThreadPool()

        # timer for picking counting rates when no acquisition running
        self.countRatesTimer = QtCore.QTimer()
        self.countRatesTimer.setInterval(100)
        self.countRatesTimer.timeout.connect(self.th260.getCountRates)
        self.countRatesTimer.timeout.connect(self.updateCountRates)

        # disconnect the default slots defined in TH260Controller
        self.th260.NEW_OUTPUT.disconnect()
        self.th260.WARNING.disconnect()
#        self.th260.PROGRESS.disconnect()
#        self.th260.DATA.disconnect()
#        self.th260.ACQ_ENDED.disconnect()
#        self.th260.DEVINIT.disconnect()
#        self.th260.UPDATECountRate.disconnect()
#        self.th260.ERROR.disconnect()

        # connecting signals to new slots:
        self.th260.NEW_OUTPUT.connect(self.printOutput)
        self.th260.WARNING.connect(self.updateWarning)
        self.th260.PROGRESS.connect(self.updateProgress)
        self.th260.DATA.connect(self.sortingWorker.sortBuffer,
                                type=QtCore.Qt.QueuedConnection)
        self.th260.ACQ_ENDED.connect(self.sortingWorker.processLastEvents,
                                     type=QtCore.Qt.QueuedConnection)
        self.th260.DEVINIT.connect(self.devInit)
        self.th260.UPDATECountRate.connect(self.updateCountRates)
#        self.th260.ERROR.connect()

        self.sortingWorker.NEW_OUTPUT.connect(self.printOutput)

        self.th260.searchDevices()
        self.setupWidgetLimits()

        self.T2settingDict = {}
        self.restaureSettings()
        self.fetchSettings("T2")

        self.initWk = TH260Thread(self.th260.initialization)
        self.statusbar.showMessage('Initialization of the device ...')
        self.threadpool.start(self.initWk)

        self.warningBtn = QtWidgets.QPushButton()
        self.warningBtn.setText('')
        self.warningBtn.setMaximumSize(100, 100)
        self.iconOk = QtGui.QIcon()
        self.iconOk.addPixmap(QtGui.QPixmap(ICON_OK))
        self.iconWarn = QtGui.QIcon()
        self.iconWarn.addPixmap(QtGui.QPixmap(ICON_WARNING))
        self.warningBtn.setIcon(self.iconOk)
        self.warningBtn.clicked.connect(self.on_warningBtn_clicked)

        self.statusbar.addPermanentWidget(self.warningBtn)

    # ------ Slots and GUI logic ------#
    @QtCore.pyqtSlot()
    def devInit(self):
        self.countRatesTimer.start()
        self.statusbar.clearMessage()
        self.statusbar.showMessage('Device initialized, ready to use', 30000)
        self.T2applySetBtn.setEnabled(True)
        self.T2startBtn.setEnabled(True)

    @QtCore.pyqtSlot(str)
    def updateWarning(self, text):
        self.warnings = text
        if text == 'No warning':
            self.warningBtn.setIcon(self.iconOk)
        else:
            self.warningBtn.setIcon(self.iconWarn)

    @QtCore.pyqtSlot()
    def updateCountRates(self):
        """Update the display of the count rate widgets"""
        self.rateSyncValue.display(self.th260.countRates[0])
        self.rateChn1Value.display(self.th260.countRates[1])
        self.rateChn2Value.display(self.th260.countRates[2])
        self.rateTotalValue.display(self.th260.countRates[3])

    @QtCore.pyqtSlot(int)
    def updateCoincRates(self, count):
        """Update the display of the coincidence count widgets"""
        if self.sortingWorker.sortingType == "2C":
            self.rateDoubleValue.display(self.rateDoubleValue.value() + count)
        else:
            self.rateTripleValue.display(self.rateTripleValue.value() + count)

    @QtCore.pyqtSlot(str, int)
    def updateProgress(self, mode, prog):
        """
        Update the display of the acquisition progress bars

        Parameters:
        -----------
        mode : str
            'file' or 'acq'
        prog : int
            for mode = 'file' time elapsed since the acquisition starts

            for mode = 'acq' number of file recorded up to now
        """
        if mode == "file":
            self.progFileTime = prog
            progRatio = prog*100/self.th260.tacq
            self.acqProgFileBar.setValue(progRatio)
        if mode == "acq":
            self.progAcqNumber = prog
            progRatio = prog*100/self.acqNoFiles
            self.acqProgBar.setValue(progRatio)
        self.progStatus.setText('Progress: {:.1f}/{:.0f}min'
                                ' of the file no {}/{}'
                                .format(self.progFileTime/60000,
                                        self.th260.tacq/60000,
                                        self.progAcqNumber,
                                        self.acqNoFiles))

    @QtCore.pyqtSlot()
    def on_warningBtn_clicked(self):
        self.showWarning(self.warnings)

    @QtCore.pyqtSlot()
    def on_T2filenameBtn_clicked(self):
        """Open a file dialog to select a destination file"""
        self.T2filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, caption="choose a file",
                directory=self.T2defaultFileDir,
                filter="""Histogram files (*.hst);;Numpy files(*.npy);;
                          All files (*.*)""")
        self.T2filenameValue.setText(self.T2filename)

    @QtCore.pyqtSlot(int)
    def on_T2chn1Chk_stateChanged(self, state):
        """Enable/disable corresponding widgets when clicked"""
        pass
        # Remove the pass statement above and uncomment the following
        # lines when the code has been modified to handle the case when
        # only one of the two channels is used in the acquisition
#        if state == 0:   # Unchecked
#            ut.disableChildOf(self.T2chn1Frame)
#        if state == 2:  # Checked
#            ut.enableChildOf(self.T2chn1Frame)

    @QtCore.pyqtSlot(int)
    def on_T2chn2Chk_stateChanged(self, state):
        """Enable/disable corresponding widgets when clicked"""
        pass
        # Remove the pass statement above and uncomment the following
        # lines when the code has been modified to handle the case when
        # only one of the two channels is used in the acquisition
#        if state == 0:   # Unchecked
#            ut.disableChildOf(self.T2chn2Frame)
#        if state == 2:  # Checked
#            ut.enableChildOf(self.T2chn2Frame)

    @QtCore.pyqtSlot(bool)
    def on_T2modeDouble_toggled(self, checked):
        """Enable/disable the time resolution gate"""
        if checked:
            self.T2timeGateShortValue.setEnabled(False)
        else:
            self.T2timeGateShortValue.setEnabled(True)

    @QtCore.pyqtSlot()
    def on_T2saveDefaultPrmBtn_clicked(self):
        """Save the CFD settings as default"""
        self.saveSettings()

    @QtCore.pyqtSlot()
    def on_T2applySetBtn_clicked(self):
        """Fetch and apply the CFD settings"""
        self.fetchSettings("T2")
        self.printOutput(
                """Measurement settings:\n
                Sync CFDZeroCross  : {syncCFDZero}
                Sync CFDLevel      : {syncCFDLevel}
                Sync Offset        : {syncOffset}
                Chn1 CFDZeroCross  : {chn1CFDZero}
                Chn1 CFDLevel      : {chn1CFDLevel}
                Chn1 Offset        : {chn1Offset}
                Chn2 CFDZeroCross  : {chn2CFDZero}
                Chn2 CFDLevel      : {chn2CFDLevel}
                Chn2 Offset        : {chn2Offset}
                """.format(syncCFDZero=self.th260.syncCFDZeroCross,
                           syncCFDLevel=self.th260.syncCFDLevel,
                           syncOffset=self.th260.syncOffset,
                           chn1CFDZero=self.th260.inputCFDZeroCross[0],
                           chn1CFDLevel=self.th260.inputCFDLevel[0],
                           chn1Offset=self.th260.inputOffset[0],
                           chn2CFDZero=self.th260.inputCFDZeroCross[1],
                           chn2CFDLevel=self.th260.inputCFDLevel[1],
                           chn2Offset=self.th260.inputOffset[1]))
        self.th260.configureSetting()

    @QtCore.pyqtSlot()
    def on_T2startBtn_clicked(self):
        """Fetch settings for CFD and acquisition, then start measurement"""
        self.T2filename = self.T2filenameValue.text()
        try:
            self.checkExistingFilename(self.T2filename)
        except ValueError:
            return
        self.fetchSettings("T2")
        self.printOutput(
                """Measurement settings:\n
                Sync CFDZeroCross  : {syncCFDZero}
                Sync CFDLevel      : {syncCFDLevel}
                Sync Offset        : {syncOffset}
                Chn1 CFDZeroCross  : {chn1CFDZero}
                Chn1 CFDLevel      : {chn1CFDLevel}
                Chn1 Offset        : {chn1Offset}
                Chn2 CFDZeroCross  : {chn2CFDZero}
                Chn2 CFDLevel      : {chn2CFDLevel}
                Chn2 Offset        : {chn2Offset}
                """.format(syncCFDZero=self.th260.syncCFDZeroCross,
                           syncCFDLevel=self.th260.syncCFDLevel,
                           syncOffset=self.th260.syncOffset,
                           chn1CFDZero=self.th260.inputCFDZeroCross[0],
                           chn1CFDLevel=self.th260.inputCFDLevel[0],
                           chn1Offset=self.th260.inputOffset[0],
                           chn2CFDZero=self.th260.inputCFDZeroCross[1],
                           chn2CFDLevel=self.th260.inputCFDLevel[1],
                           chn2Offset=self.th260.inputOffset[1]))

        self.fetchAcqSettings("T2")
        self.printOutput(
            """Measurement settings:\n
            Acquisition time per file   : {acqTime} sec
            Number of files             : {noFiles}
            Time gate total             : {timeGate} ps
            Time gate (511 keV)         : {timeGate511} ps
            """.format(acqTime=self.th260.tacq,
                       noFiles=self.acqNoFiles,
                       timeGate=self.timeGate,
                       timeGate511=self.timeGate511
                       if self.T2modeTriple.isChecked()
                       else "None (2C mode)"))

        answer = self.showQuestion(""" Acquisition is about to start with:
                            Acquisition time per file   : {acqTime} sec
                            Number of files             : {noFiles}
                            Time gate total             : {timeGate} ps
                            Time gate (511 keV)         : {timeGate511} ps
                            """.format(acqTime=self.th260.tacq,
                                       noFiles=self.acqNoFiles,
                                       timeGate=self.timeGate,
                                       timeGate511=self.timeGate511
                                       if self.T2modeTriple.isChecked()
                                       else "None (2C mode)"))

        if answer == QtWidgets.QMessageBox.Ok:
            self.startAcquisition("T2")
            pass
        elif answer == QtWidgets.QMessageBox.Cancel:
            return

    @QtCore.pyqtSlot()
    def startAcquisition(self, mode):
        """Configure some variable of the TH260 controller and start"""
        # TODO: check param input
        self.saveAcqSettings()
        self.th260.countRates[3] = 0
        self.acqProgBar.setValue(0)
        self.acqProgFileBar.setValue(0)
        self.rateDoubleValue.display(0)
        self.rateTripleValue.display(0)
        self.progFileTime = 0
        self.progAcqNumber = 0
        if mode == "T2":
            self.th260.configureSetting()
            # sorting worker:
            self.sortingWorker.kwargs["nftot"] = self.acqNoFiles
            self.sortingWorker.kwargs["CFDset"] = self.T2settingDict
            self.sortingWorker.kwargs["acqTime"] = self.th260.tacq/60000
            self.sortingWorker.kwargs["filename"] = self.T2filename
            self.sortingWorker.kwargs["sortingType"] = "3C"\
                if self.T2modeTriple.isChecked()\
                else "2C"
            self.sortingWorker.kwargs["timeGate"] = self.timeGate
            if self.T2modeTriple.isChecked():
                self.sortingWorker.kwargs["timeRes"] = self.timeGate511
            else:
                self.sortingWorker.kwargs["timeRes"] = None

            # threads:
            self.acqThread = T2AcquisitionThread(self.th260, self.acqNoFiles)
            self.acqThread.globProgress.connect(self.updateProgress)
            self.acqThread.newMeas.connect(self.sortingWorker.newMeasurement)
            self.acqThread.fileDone.connect(self.sortingWorker.saveData)
            self.acqThread.measDone.connect(self.measEnded)

            self.sortingThread.start()
            self.countRatesTimer.stop()
            self.acqThread.start()

            self.statusbar.showMessage('Measurement running ...')
            self.progStatus = QtWidgets.QLabel('Progress: {}min/X'
                                               ' of the file no{}/N'
                                               .format(self.progFileTime,
                                                       self.progAcqNumber))
            self.statusbar.insertPermanentWidget(0, self.progStatus)
            ut.disableChildOf(self.T2acqGrp, self.T2stopBtn)
            ut.disableChildOf(self.T2settingsGrp)

    @QtCore.pyqtSlot()
    def measEnded(self):
        self.statusbar.removeWidget(self.progStatus)
        self.statusbar.showMessage("The measurement has ended normally",
                                   30000)
        ut.enableChildOf(self.T2acqGrp)
        ut.enableChildOf(self.T2settingsGrp)
        self.countRatesTimer.start()

    @QtCore.pyqtSlot()
    def on_T2stopBtn_clicked(self):
        """Stop the TTTR measurement and enable acq/settings widgets"""
        try:
            self.acqThread.requestInterruption()
        except AttributeError:
            self.showError("No thread to stop")
        else:
            self.th260.stoptttr()
            time.sleep(0.1)
            self.statusbar.removeWidget(self.progStatus)
            self.statusbar.showMessage('Last measurement stopped at {}'
                                       ' min of the file no {}'
                                       .format(self.progFileTime/60000,
                                               self.progAcqNumber+1))
        ut.enableChildOf(self.T2acqGrp)
        ut.enableChildOf(self.T2settingsGrp)
        self.countRatesTimer.start()

    @QtCore.pyqtSlot()
    def on_actionExit_triggered(self):
        self.th260.closeDevices()
        self.close()

    @QtCore.pyqtSlot()
    def on_actionDLL_version_triggered(self):
        self.showMessage("Currently installed library version: {}\n"
                         "\nPals3D has been developped using version: {}"
                         .format(self.th260.libVersion.value.decode("utf-8"),
                                 self.th260.LIB_VERSION))

    @QtCore.pyqtSlot()
    def on_actionPals3D_version_triggered(self):
        self.showMessage("Current version of Pals3D: {}\n"
                         .format(VERSION))

    @QtCore.pyqtSlot()
    def on_actionAbout_triggered(self):
        self.showMessage("Pals3D  Copyright (C) 2018-2019 "
                         "Aurélie Vancraeyenest"
                         "\nThis program comes with ABSOLUTELY NO WARRANTY."
                         "\nThis is free software, and you are welcome to "
                         "redistribute it under certain conditions. "
                         "See LICENSE file for details.")

    @QtCore.pyqtSlot()
    def on_actionPalss3D_help_triggered(self):
        webbrowser.open('http://pals3d.readthedocs.io/')

    def checkExistingFilename(self, filename):
        try:
            filebase, extension = filename.rsplit(sep=".", maxsplit=1)
        except ValueError:
            filebase = filename

        outputFileName = "".join((filebase,
                                  '_000.hst'))
        if os.path.isfile(outputFileName):
            answer = self.showQuestion("Output file {} will be overwritten!\n"
                                       "Do you want to continue?"
                                       .format(outputFileName))
            if answer == QtWidgets.QMessageBox.Cancel:
                raise ValueError()

    def fetchAcqSettings(self, mode):
        """Get the acquisition settings from the GUI widgets"""
        if mode == "T2":
            self.th260.tacq = self.T2acqTimePerFileValue.value()*60000
            self.acqNoFiles = self.T2acqNoFilesValue.value()
            self.timeGate = self.T2timeGateLongValue.value()
            if self.T2modeTriple.isChecked():
                self.timeGate511 = self.T2timeGateShortValue.value()
            else:
                self.timeGate511 = None

    def fetchSettings(self, mode):
        """Get the CFD settings for each channel from the GUI widgets"""
        if mode == "T2":
            self.th260.syncCFDLevel = self.T2syncLevelValue.value()
            self.th260.syncCFDZeroCross = self.T2syncZeroValue.value()
            self.th260.syncOffset = self.T2syncOffsetValue.value()
            self.th260.inputCFDLevel[0] = self.T2chn1LevelValue.value()
            self.th260.inputCFDLevel[1] = self.T2chn2LevelValue.value()
            self.th260.inputCFDZeroCross[0] = self.T2chn1ZeroValue.value()
            self.th260.inputCFDZeroCross[1] = self.T2chn2ZeroValue.value()
            self.th260.inputOffset[0] = self.T2chn1OffsetValue.value()
            self.th260.inputOffset[1] = self.T2chn2OffsetValue.value()
            self.T2settingDict['lev0'] = self.th260.syncCFDLevel
            self.T2settingDict['zero0'] = self.th260.syncCFDZeroCross
            self.T2settingDict['off0'] = self.th260.syncOffset
            self.T2settingDict['lev1'] = self.th260.inputCFDLevel[0]
            self.T2settingDict['zero1'] = self.th260.inputCFDZeroCross[0]
            self.T2settingDict['off1'] = self.th260.inputOffset[0]
            self.T2settingDict['lev2'] = self.th260.inputCFDLevel[1]
            self.T2settingDict['zero2'] = self.th260.inputCFDZeroCross[1]
            self.T2settingDict['off2'] = self.th260.inputOffset[1]

    def saveSettings(self):
        """Store the currents CFD settings as default values"""
        self.settings.setValue('T2chn1LevelValue',
                               self.T2chn1LevelValue.value())
        self.settings.setValue('T2chn1OffsetValue',
                               self.T2chn1OffsetValue.value())
        self.settings.setValue('T2chn1ZeroValue',
                               self.T2chn1ZeroValue.value())

        self.settings.setValue('T2chn2LevelValue',
                               self.T2chn2LevelValue.value())
        self.settings.setValue('T2chn2OffsetValue',
                               self.T2chn2OffsetValue.value())
        self.settings.setValue('T2chn2ZeroValue',
                               self.T2chn2ZeroValue.value())

        self.settings.setValue('T2syncLevelValue',
                               self.T2syncLevelValue.value())
        self.settings.setValue('T2syncOffsetValue',
                               self.T2syncOffsetValue.value())
        self.settings.setValue('T2syncZeroValue',
                               self.T2syncZeroValue.value())

    def saveAcqSettings(self):
        """Store the currents acquisition settings as default values"""
        self.settings.setValue('T2modeDouble',
                               self.T2modeDouble.isChecked())
        self.settings.setValue('T2acqTimePerFileValue',
                               self.T2acqTimePerFileValue.value())
        self.settings.setValue('T2acqNoFilesValue',
                               self.T2acqNoFilesValue.value())
        self.settings.setValue('T2timeGateLongValue',
                               self.T2timeGateLongValue.value())
        self.settings.setValue('T2timeGateShortValue',
                               self.T2timeGateShortValue.value())
        self.settings.setValue('T2filePath',
                               os.path.dirname(self.T2filename))
        self.settings.setValue('T2filename', self.T2filename)

    def restaureSettings(self):
        """Load the default values for CFD and acquisition settings"""
        self.T2chn1LevelValue.setValue(
                self.settings.value('T2chn1LevelValue', type=int))
        self.T2chn1OffsetValue.setValue(
                self.settings.value('T2chn1OffsetValue', type=int))
        self.T2chn1ZeroValue.setValue(
                self.settings.value('T2chn1ZeroValue', type=int))

        self.T2chn2LevelValue.setValue(
                self.settings.value('T2chn2LevelValue', type=int))
        self.T2chn2OffsetValue.setValue(
                self.settings.value('T2chn2OffsetValue', type=int))
        self.T2chn2ZeroValue.setValue(
                self.settings.value('T2chn2ZeroValue', type=int))

        self.T2syncLevelValue.setValue(
                self.settings.value('T2syncLevelValue', type=int))
        self.T2syncOffsetValue.setValue(
                self.settings.value('T2syncOffsetValue', type=int))
        self.T2syncZeroValue.setValue(
                self.settings.value('T2syncZeroValue', type=int))

        self.T2modeDouble.setChecked(
                self.settings.value('T2modeDouble', type=bool))

        self.T2acqTimePerFileValue.setValue(
                self.settings.value('T2acqTimePerFileValue', type=int))
        self.T2acqNoFilesValue.setValue(
                self.settings.value('T2acqNoFilesValue', type=int))

        self.T2timeGateLongValue.setValue(
                self.settings.value('T2timeGateLongValue', type=int))
        self.T2timeGateShortValue.setValue(
                self.settings.value('T2timeGateShortValue', type=int))

        self.T2filename = self.settings.value('T2filename', type=str)
        self.T2filenameValue.setText(self.T2filename)
        self.T2defaultFileDir = self.settings.value('T2filePath', type=str)

    def setupWidgetLimits(self):
        """Set the hardware limits to the corresponding widgets"""

        self.T2chn1LevelValue.setMaximum(self.th260.CFDLVLMAX)
        self.T2chn1LevelValue.setMinimum(self.th260.CFDLVLMIN)
        self.T2chn2LevelValue.setMaximum(self.th260.CFDLVLMAX)
        self.T2chn2LevelValue.setMinimum(self.th260.CFDLVLMIN)
        self.T2syncLevelValue.setMaximum(self.th260.CFDLVLMAX)
        self.T2syncLevelValue.setMinimum(self.th260.CFDLVLMIN)
        self.T2chn1OffsetValue.setMaximum(self.th260.CHANOFFSMAX)
        self.T2chn1OffsetValue.setMinimum(self.th260.CHANOFFSMIN)
        self.T2chn2OffsetValue.setMaximum(self.th260.CHANOFFSMAX)
        self.T2chn2OffsetValue.setMinimum(self.th260.CHANOFFSMIN)
        self.T2syncOffsetValue.setMaximum(self.th260.CHANOFFSMAX)
        self.T2syncOffsetValue.setMinimum(self.th260.CHANOFFSMIN)
        self.T2chn1ZeroValue.setMaximum(self.th260.CFDZCMAX)
        self.T2chn1ZeroValue.setMinimum(self.th260.CFDZCMIN)
        self.T2chn2ZeroValue.setMaximum(self.th260.CFDZCMAX)
        self.T2chn2ZeroValue.setMinimum(self.th260.CFDZCMIN)
        self.T2syncZeroValue.setMaximum(self.th260.CFDZCMAX)
        self.T2syncZeroValue.setMinimum(self.th260.CFDZCMIN)
        self.T2acqTimePerFileValue.setMaximum(self.th260.ACQTMAX/1000)  # in s
        self.T2acqTimePerFileValue.setMinimum(self.th260.ACQTMIN)  # always 1
        self.T2acqNoFilesValue.setMaximum(6000)
        self.T2acqNoFilesValue.setMinimum(0)
        self.T2timeGateLongValue.setMaximum(20000)      # in ps
        self.T2timeGateLongValue.setMinimum(0)          # in ps
        self.T2timeGateShortValue.setMaximum(20000)     # in ps
        self.T2timeGateShortValue.setMinimum(0)         # in ps

    def printOutput(self, text):
        """
        Append command outputs to the text box of the GUI

        Parameters:
        -----------
        text : 'str'
            Message to be printed in the command output widget
        """
        self.commandOutput.appendPlainText(text)

    def showMessage(self, message):
        """
        Display "message" in a "Information" message box with 'OK' button.

        Parameters:
        -----------
        message : 'str'
            Message to be printed in the command output widget
        """

        messageBox = QtWidgets.QMessageBox()
        messageBox.setText(message)
        messageBox.setWindowTitle("Info")
        messageBox.setIcon(QtWidgets.QMessageBox.Information)
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        messageBox.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        # Show the window
        messageBox.raise_()
        messageBox.exec_()

    def showError(self, message):
        """
        Display "message" in a "Critical error" message box with 'OK' button.

        Parameters:
        -----------
        message : 'str'
            Message to be printed in the command output widget
        """

        messageBox = QtWidgets.QMessageBox()
        messageBox.setText(message)
        messageBox.setWindowTitle("Error")
        messageBox.setIcon(QtWidgets.QMessageBox.Critical)
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        messageBox.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        # Show the window
        messageBox.raise_()
        messageBox.exec_()

    def showWarning(self, message):
        """
        Display "message" in a "Warning" message box with 'OK' button.

        Parameters:
        -----------
        message : 'str'
            Message to be printed in the command output widget
        """

        messageBox = QtWidgets.QMessageBox()
        messageBox.setText(message)
        messageBox.setWindowTitle("Warning")
        messageBox.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(ICON_WARNING)))
        messageBox.setIcon(QtWidgets.QMessageBox.Warning)
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        messageBox.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        # Show the window
        messageBox.raise_()
        messageBox.exec_()

    def showQuestion(self, message):
        """
        Display "message" in a "Warning question" message box with
        'OK' and 'Cancel' button

        Parameters:
        -----------
        message : 'str'
            Message to be printed in the command output widget
        """
        self.messageBox = QtWidgets.QMessageBox()
        self.messageBox.setText(message)
        self.messageBox.setWindowTitle("Question")
        self.messageBox.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(ICON_WARNING)))
        self.messageBox.setIcon(QtWidgets.QMessageBox.Warning)
        self.messageBox.setStandardButtons(QtWidgets.QMessageBox.Cancel
                                           | QtWidgets.QMessageBox.Ok)
        self.messageBox.setTextInteractionFlags(
                                            QtCore.Qt.TextSelectableByMouse)

        # Show the window
        self.messageBox.raise_()
        answer = self.messageBox.exec_()
        return answer


# ---------- Thread workers ---------- #
class TH260Thread(QtCore.QRunnable):
    """
    Generic QRunnable that takes a function and its args/kwargs
    as arguments to run it in a threadpool
    """
    def __init__(self, fn, *args, **kwargs):
        """Constructor of the TH260Thread """
        super(TH260Thread, self).__init__()
        self.fn = fn
        self.args = args
        self.kwargs = kwargs

    @QtCore.pyqtSlot()
    def run(self):
        try:
            self.fn(*self.args, **self.kwargs)
        except Exception:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
        else:
            pass


class T2AcquisitionThread(QtCore.QThread):
    """
    Write docstring here

    Supported signals:
    ------------------
    globProgress : str, int
        Emitted at the end of each single acquisition
    fileDone : int
        Emitted when the nth acquisition has ended. Sent with n as
        argument
    newMeas : int
        Emmitted while starting a new measurment with as argument the
        numero of the starting acquisition
    measDone : None
        Not in use
    """
    globProgress = QtCore.pyqtSignal(str, int)
    fileDone = QtCore.pyqtSignal(int)
    newMeas = QtCore.pyqtSignal(int)
    measDone = QtCore.pyqtSignal()

    def __init__(self,  dev, noFiles):
        super(T2AcquisitionThread, self).__init__()
        self.th260device = dev
        self.noFiles = noFiles
        self.abort = False

    def run(self):
        for nof in range(self.noFiles):
            if self.isInterruptionRequested():
                return
            self.newMeas.emit(nof)
            self.th260device.startAcquisition()
            self.fileDone.emit(nof)
            self.globProgress.emit("acq", nof+1)
        self.measDone.emit()

        self.exec_()
        self.__init__(self.th260device, self.noFiles)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec()
