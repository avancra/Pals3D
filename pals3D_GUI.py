# -*- coding: utf-8 -*-
"""
Data acquisition GUI for TimeHarp260 P
for use with positron annihilation lifetime spectroscpoy

(c) Aurelie Vancraeyenest 2018
"""

import sys
import traceback
import os.path

from PyQt5 import QtWidgets, QtCore

import toolbox.utils as ut
import acqGUI
import th260controller
import th260sorter

# put here visual ressources


class MainWindow(QtWidgets.QMainWindow, acqGUI.Ui_MainWindow):

    """
        Main instance for the GUI of the hv controller panel

    TO be completed

    """

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.settings = QtCore.QSettings('Aalto-Antimatter', 'Pals3D')

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
        self.th260.WARNING.connect(self.showWarning)
        self.th260.PROGRESS.connect(self.updateProgress)
        self.th260.DATA.connect(self.sortingWorker.sortBuffer,
                                type=QtCore.Qt.QueuedConnection)
        self.th260.ACQ_ENDED.connect(self.sortingWorker.processLastEvents,
                                     type=QtCore.Qt.QueuedConnection)
        self.th260.DEVINIT.connect(self.countRatesTimer.start)
        self.th260.UPDATECountRate.connect(self.updateCountRates)
#        self.th260.ERROR.connect()

        self.sortingWorker.NEW_OUTPUT.connect(self.printOutput)

        self.th260.searchDevices()
        self.setupWidgetLimits()

        self.restaureSettings()
        self.fetchSettings("T2")

        self.initWk = TH260Thread(self.th260.initialization)
        self.threadpool.start(self.initWk)

    # ------ Slots and GUI logic ------#
    @QtCore.pyqtSlot()
    def updateCountRates(self):
        self.rateSyncValue.display(self.th260.countRates[0])
        self.rateChn1Value.display(self.th260.countRates[1])
        self.rateChn2Value.display(self.th260.countRates[2])
        self.rateTotalValue.display(self.th260.countRates[3])

    @QtCore.pyqtSlot(int)
    def updateCoincRates(self, count):
        if self.sortingWorker.sortingType == "2C":
            self.rateDoubleValue.display(self.rateDoubleValue.value() + count)
        else:
            self.rateTripleValue.display(self.rateTripleValue.value() + count)

    @QtCore.pyqtSlot()
    def on_T2filenameBtn_clicked(self):
        self.T2filename, _ = QtWidgets.QFileDialog.getSaveFileName(
                self, caption="choose a file",
                directory=self.T2defaultFileDir,
                filter="PTU files (*.ptu);;All files (*.*)")
        self.T2filenameValue.setText(self.T2filename)

    @QtCore.pyqtSlot(int)
    def on_T2chn1Chk_stateChanged(self, state):
        if state == 0:   # Unchecked
            ut.disableChildOf(self.T2chn1Frame)
        if state == 2:  # Checked
            ut.enableChildOf(self.T2chn1Frame)

    @QtCore.pyqtSlot(int)
    def on_T2chn2Chk_stateChanged(self, state):
        if state == 0:   # Unchecked
            ut.disableChildOf(self.T2chn2Frame)
        if state == 2:  # Checked
            ut.enableChildOf(self.T2chn2Frame)

    @QtCore.pyqtSlot(bool)
    def on_T2modeDouble_toggled(self, checked):
        if checked:
            self.T2timeGateShortValue.setEnabled(False)
        else:
            self.T2timeGateShortValue.setEnabled(True)

    @QtCore.pyqtSlot()
    def on_T2saveDefaultPrmBtn_clicked(self):
        self.saveSettings()

    @QtCore.pyqtSlot()
    def on_T2applySetBtn_clicked(self):
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
        self.T2filename = self.T2filenameValue.text()
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

        # TODO: add the filename in the question
        rep = self.showQuestion(""" Acquisition is about to start with:
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

        if rep == QtWidgets.QMessageBox.Ok:
            self.startAcquisition("T2")
            pass
        elif rep == QtWidgets.QMessageBox.Cancel:
            return

    @QtCore.pyqtSlot()
    def startAcquisition(self, mode):
        # TODO: check param input
        self.saveAcqSettings()
        self.th260.countRates[3] = 0
        self.acqProgBar.setValue(0)
        self.acqProgFileBar.setValue(0)
        self.rateDoubleValue.display(0)
        self.rateTripleValue.display(0)
        if mode == "T2":
            self.th260.configureSetting()
            # sorting worker:
            self.sortingWorker.kwargs["filename"] = self.T2filename
            self.sortingWorker.kwargs["sortingType"] = "3C"\
                if self.T2modeTriple.isChecked()\
                else "2C"
            self.sortingWorker.kwargs["timeGate"] = self.timeGate
            if self.T2modeTriple.isChecked():
                self.sortingWorker.kwargs["timeRes"] = self.timeGate511
            else:
                self.sortingWorker.kwargs["timeRes"] = None
            if self.T2doHistChk.isChecked():
                self.sortingWorker.kwargs["doHist"] = True
            else:
                self.sortingWorker.kwargs["doHist"] = False

            # threads:
            self.acqThread = T2AcquisitionThread(self.th260, self.acqNoFiles)
            self.acqThread.globProgress.connect(self.updateProgress)
            self.acqThread.newMeas.connect(self.sortingWorker.newMeasurement)
            self.acqThread.fileDone.connect(self.sortingWorker.saveData)

            self.sortingThread.start()
            self.countRatesTimer.stop()
            self.acqThread.start()

            ut.disableChildOf(self.T2acqGrp, self.T2stopBtn)
            ut.disableChildOf(self.T2settingsGrp)

    @QtCore.pyqtSlot(str, int)
    def updateProgress(self, mode, prog):
        pass
        if mode == "file":
            progRatio = prog*100/self.th260.tacq
            self.acqProgFileBar.setValue(progRatio)
        if mode == "acq":
            progRatio = prog*100/self.acqNoFiles
            self.acqProgBar.setValue(progRatio)

    @QtCore.pyqtSlot()
    def on_T2stopBtn_clicked(self):
        ut.enableChildOf(self.T2acqGrp)
        ut.enableChildOf(self.T2settingsGrp)

        self.countRatesTimer.stop()
        self.th260.stoptttr()
        self.countRatesTimer.start()


    def fetchAcqSettings(self, mode):
        """
        """
        if mode == "T2":
            # TODO : change back to *60000
            self.th260.tacq = self.T2acqTimePerFileValue.value()*1000  # *60000
            self.acqNoFiles = self.T2acqNoFilesValue.value()
            self.timeGate = self.T2timeGateLongValue.value()
            if self.T2modeTriple.isChecked():
                self.timeGate511 = self.T2timeGateShortValue.value()
            else:
                self.timeGate511 = None

    def fetchSettings(self, mode):
        """
        """

        if mode is "T2":
            self.th260.syncCFDLevel = self.T2syncLevelValue.value()
            self.th260.syncCFDZeroCross = self.T2syncZeroValue.value()
            self.th260.syncOffset = self.T2syncOffsetValue.value()
            self.th260.inputCFDLevel[0] = self.T2chn1LevelValue.value()
            self.th260.inputCFDLevel[1] = self.T2chn2LevelValue.value()
            self.th260.inputCFDZeroCross[0] = self.T2chn1ZeroValue.value()
            self.th260.inputCFDZeroCross[1] = self.T2chn2ZeroValue.value()
            self.th260.inputOffset[0] = self.T2chn1OffsetValue.value()
            self.th260.inputOffset[1] = self.T2chn2OffsetValue.value()

        return False, None

    def saveSettings(self):
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
        self.settings.setValue('T2doHist',
                               self.T2doHistChk.isChecked())

    def restaureSettings(self):

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
        self.T2doHistChk.setChecked(
                self.settings.value('T2doHist', type=bool))

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
        """ Set the hardware limits to the corresponding widgets
        """
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
        self.T2acqTimePerFileValue.setMinimum(self.th260.ACQTMIN/1000)  # in s
        self.T2acqNoFilesValue.setMaximum(6000)
        self.T2acqNoFilesValue.setMinimum(0)
        self.T2timeGateLongValue.setMaximum(20000)      # in ps
        self.T2timeGateLongValue.setMinimum(0)          # in ps
        self.T2timeGateShortValue.setMaximum(20000)     # in ps
        self.T2timeGateShortValue.setMinimum(0)         # in ps

    def printOutput(self, text):
        """
            Append command outputs to the text box of the GUI

            parameters:
            ----
                s: 'str' -- emitted via threadpool threads
        """
        self.commandOutput.appendPlainText(text)

    def showError(self, message):
        """
            Display "message" in a "Critical error" message box
            with 'OK' button.

        """

        # Create a QMessagebox
        messageBox = QtWidgets.QMessageBox()

        messageBox.setText(message)
        messageBox.setWindowTitle("Error")
#        messageBox.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/grid.png")))
        messageBox.setIcon(QtWidgets.QMessageBox.Critical)
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        messageBox.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        # Show the window
        messageBox.raise_()
        messageBox.exec_()

    def showWarning(self, message):

        # Create a QMessagebox
        messageBox = QtWidgets.QMessageBox()

        messageBox.setText(message)
        messageBox.setWindowTitle("Warning")
#        messageBox.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/grid.png")))
        messageBox.setIcon(QtWidgets.QMessageBox.Warning)
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        messageBox.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        # Show the window
        messageBox.raise_()
        messageBox.exec_()

    def showQuestion(self, message):
        self.messageBox = QtWidgets.QMessageBox()
        self.messageBox.setText(message)
        self.messageBox.setWindowTitle("Question")
#        messageBox.setWindowIcon(QtGui.QIcon(QtGui.QPixmap(":/icons/grid.png")))
        self.messageBox.setIcon(QtWidgets.QMessageBox.Warning)
        self.messageBox.setStandardButtons(QtWidgets.QMessageBox.Cancel
                                           | QtWidgets.QMessageBox.Ok)
        self.messageBox.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        # Show the window
        self.messageBox.raise_()
        answer = self.messageBox.exec_()
        return answer


# ---------- Thread workers ---------- #
class TH260Thread(QtCore.QRunnable):
    def __init__(self, fn, *args, **kwargs):
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
        ----
            globProgress: 'str', 'int'
                Emitted at the end of each single acquisition
    """
    globProgress = QtCore.pyqtSignal(str, int)
    fileDone = QtCore.pyqtSignal(int)
    newMeas = QtCore.pyqtSignal(int)
    measDone = QtCore.pyqtSignal()

    def __init__(self,  dev, noFiles):
        super(T2AcquisitionThread, self).__init__()
        self.th260device = dev
        self.noFiles = noFiles

    def run(self):

        for nof in range(self.noFiles):
            self.newMeas.emit(nof)
            self.th260device.startAcquisition()
            self.fileDone.emit(nof)
            self.globProgress.emit("acq", nof+1)
        self.exec_()
        self.__init__(self.th260device, self.noFiles)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    form = MainWindow()
    form.show()
    app.exec()
