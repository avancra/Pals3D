# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'acqGUI.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(717, 783)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.T2settingsGrp = QtWidgets.QGroupBox(self.centralwidget)
        self.T2settingsGrp.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.T2settingsGrp.setFlat(False)
        self.T2settingsGrp.setObjectName("T2settingsGrp")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.T2settingsGrp)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_9 = QtWidgets.QLabel(self.T2settingsGrp)
        self.label_9.setObjectName("label_9")
        self.gridLayout_2.addWidget(self.label_9, 0, 0, 1, 1)
        self.T2chn1Chk = QtWidgets.QCheckBox(self.T2settingsGrp)
        self.T2chn1Chk.setChecked(True)
        self.T2chn1Chk.setObjectName("T2chn1Chk")
        self.gridLayout_2.addWidget(self.T2chn1Chk, 0, 1, 1, 1)
        self.T2chn2Chk = QtWidgets.QCheckBox(self.T2settingsGrp)
        self.T2chn2Chk.setChecked(True)
        self.T2chn2Chk.setObjectName("T2chn2Chk")
        self.gridLayout_2.addWidget(self.T2chn2Chk, 0, 2, 1, 1)
        self.T2syncFrame = QtWidgets.QFrame(self.T2settingsGrp)
        self.T2syncFrame.setObjectName("T2syncFrame")
        self.T2syncLayout_3 = QtWidgets.QFormLayout(self.T2syncFrame)
        self.T2syncLayout_3.setObjectName("T2syncLayout_3")
        self.T2syncZeroLabel = QtWidgets.QLabel(self.T2syncFrame)
        self.T2syncZeroLabel.setObjectName("T2syncZeroLabel")
        self.T2syncLayout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.T2syncZeroLabel)
        self.T2syncLevelLabel = QtWidgets.QLabel(self.T2syncFrame)
        self.T2syncLevelLabel.setObjectName("T2syncLevelLabel")
        self.T2syncLayout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.T2syncLevelLabel)
        self.T2syncOffsetLabel = QtWidgets.QLabel(self.T2syncFrame)
        self.T2syncOffsetLabel.setObjectName("T2syncOffsetLabel")
        self.T2syncLayout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.T2syncOffsetLabel)
        self.T2syncOffsetValue = QtWidgets.QSpinBox(self.T2syncFrame)
        self.T2syncOffsetValue.setMinimum(-99999)
        self.T2syncOffsetValue.setMaximum(99999)
        self.T2syncOffsetValue.setObjectName("T2syncOffsetValue")
        self.T2syncLayout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.T2syncOffsetValue)
        self.T2syncZeroValue_3 = QtWidgets.QSpinBox(self.T2syncFrame)
        self.T2syncZeroValue_3.setMinimum(-40)
        self.T2syncZeroValue_3.setMaximum(0)
        self.T2syncZeroValue_3.setObjectName("T2syncZeroValue_3")
        self.T2syncLayout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.T2syncZeroValue_3)
        self.T2syncLevelValue = QtWidgets.QSpinBox(self.T2syncFrame)
        self.T2syncLevelValue.setMinimum(-1200)
        self.T2syncLevelValue.setMaximum(0)
        self.T2syncLevelValue.setObjectName("T2syncLevelValue")
        self.T2syncLayout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.T2syncLevelValue)
        self.gridLayout_2.addWidget(self.T2syncFrame, 1, 0, 1, 1)
        self.T2chn1Frame = QtWidgets.QFrame(self.T2settingsGrp)
        self.T2chn1Frame.setObjectName("T2chn1Frame")
        self.T2chn1Layout_3 = QtWidgets.QFormLayout(self.T2chn1Frame)
        self.T2chn1Layout_3.setObjectName("T2chn1Layout_3")
        self.T2chn1ZeroLabel = QtWidgets.QLabel(self.T2chn1Frame)
        self.T2chn1ZeroLabel.setObjectName("T2chn1ZeroLabel")
        self.T2chn1Layout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.T2chn1ZeroLabel)
        self.T2chn1ZeroValue = QtWidgets.QSpinBox(self.T2chn1Frame)
        self.T2chn1ZeroValue.setMinimum(-40)
        self.T2chn1ZeroValue.setMaximum(0)
        self.T2chn1ZeroValue.setObjectName("T2chn1ZeroValue")
        self.T2chn1Layout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.T2chn1ZeroValue)
        self.T2chn1LevelLabel = QtWidgets.QLabel(self.T2chn1Frame)
        self.T2chn1LevelLabel.setObjectName("T2chn1LevelLabel")
        self.T2chn1Layout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.T2chn1LevelLabel)
        self.T2chn1LevelValue = QtWidgets.QSpinBox(self.T2chn1Frame)
        self.T2chn1LevelValue.setMinimum(-1200)
        self.T2chn1LevelValue.setMaximum(0)
        self.T2chn1LevelValue.setObjectName("T2chn1LevelValue")
        self.T2chn1Layout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.T2chn1LevelValue)
        self.label = QtWidgets.QLabel(self.T2chn1Frame)
        self.label.setObjectName("label")
        self.T2chn1Layout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label)
        self.T2chn1OffsetValue = QtWidgets.QSpinBox(self.T2chn1Frame)
        self.T2chn1OffsetValue.setMinimum(-99999)
        self.T2chn1OffsetValue.setMaximum(99999)
        self.T2chn1OffsetValue.setObjectName("T2chn1OffsetValue")
        self.T2chn1Layout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.T2chn1OffsetValue)
        self.gridLayout_2.addWidget(self.T2chn1Frame, 1, 1, 1, 1)
        self.T2chn2Frame = QtWidgets.QFrame(self.T2settingsGrp)
        self.T2chn2Frame.setObjectName("T2chn2Frame")
        self.T2chn2Layout_3 = QtWidgets.QFormLayout(self.T2chn2Frame)
        self.T2chn2Layout_3.setObjectName("T2chn2Layout_3")
        self.T2chn2ZeroLabel = QtWidgets.QLabel(self.T2chn2Frame)
        self.T2chn2ZeroLabel.setObjectName("T2chn2ZeroLabel")
        self.T2chn2Layout_3.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.T2chn2ZeroLabel)
        self.T2chn2LevelLabel = QtWidgets.QLabel(self.T2chn2Frame)
        self.T2chn2LevelLabel.setObjectName("T2chn2LevelLabel")
        self.T2chn2Layout_3.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.T2chn2LevelLabel)
        self.T2chn2OffsetLabel = QtWidgets.QLabel(self.T2chn2Frame)
        self.T2chn2OffsetLabel.setObjectName("T2chn2OffsetLabel")
        self.T2chn2Layout_3.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.T2chn2OffsetLabel)
        self.T2chn2OffsetValue = QtWidgets.QSpinBox(self.T2chn2Frame)
        self.T2chn2OffsetValue.setMinimum(-99999)
        self.T2chn2OffsetValue.setMaximum(99999)
        self.T2chn2OffsetValue.setObjectName("T2chn2OffsetValue")
        self.T2chn2Layout_3.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.T2chn2OffsetValue)
        self.T2chn2ZeroValue = QtWidgets.QSpinBox(self.T2chn2Frame)
        self.T2chn2ZeroValue.setMinimum(-40)
        self.T2chn2ZeroValue.setMaximum(0)
        self.T2chn2ZeroValue.setObjectName("T2chn2ZeroValue")
        self.T2chn2Layout_3.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.T2chn2ZeroValue)
        self.T2chn2LevelValue = QtWidgets.QSpinBox(self.T2chn2Frame)
        self.T2chn2LevelValue.setMinimum(-1200)
        self.T2chn2LevelValue.setMaximum(0)
        self.T2chn2LevelValue.setObjectName("T2chn2LevelValue")
        self.T2chn2Layout_3.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.T2chn2LevelValue)
        self.gridLayout_2.addWidget(self.T2chn2Frame, 1, 2, 1, 1)
        self.T2saveDefaultPrmBtn = QtWidgets.QPushButton(self.T2settingsGrp)
        self.T2saveDefaultPrmBtn.setObjectName("T2saveDefaultPrmBtn")
        self.gridLayout_2.addWidget(self.T2saveDefaultPrmBtn, 2, 0, 1, 2)
        self.T2applySetBtn = QtWidgets.QPushButton(self.T2settingsGrp)
        self.T2applySetBtn.setObjectName("T2applySetBtn")
        self.gridLayout_2.addWidget(self.T2applySetBtn, 2, 2, 1, 1)
        self.verticalLayout.addWidget(self.T2settingsGrp)
        self.T2acqGrp = QtWidgets.QGroupBox(self.centralwidget)
        self.T2acqGrp.setObjectName("T2acqGrp")
        self.gridLayout_10 = QtWidgets.QGridLayout(self.T2acqGrp)
        self.gridLayout_10.setObjectName("gridLayout_10")
        self.label_17 = QtWidgets.QLabel(self.T2acqGrp)
        self.label_17.setObjectName("label_17")
        self.gridLayout_10.addWidget(self.label_17, 2, 1, 1, 1)
        self.formLayout_9 = QtWidgets.QFormLayout()
        self.formLayout_9.setObjectName("formLayout_9")
        self.T2acqTimePerFileLabel = QtWidgets.QLabel(self.T2acqGrp)
        self.T2acqTimePerFileLabel.setObjectName("T2acqTimePerFileLabel")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.T2acqTimePerFileLabel)
        self.T2acqTimePerFileValue = QtWidgets.QSpinBox(self.T2acqGrp)
        self.T2acqTimePerFileValue.setMaximum(6000)
        self.T2acqTimePerFileValue.setObjectName("T2acqTimePerFileValue")
        self.formLayout_9.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.T2acqTimePerFileValue)
        self.T2acqNoFilesLabel = QtWidgets.QLabel(self.T2acqGrp)
        self.T2acqNoFilesLabel.setObjectName("T2acqNoFilesLabel")
        self.formLayout_9.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.T2acqNoFilesLabel)
        self.T2acqNoFilesValue = QtWidgets.QSpinBox(self.T2acqGrp)
        self.T2acqNoFilesValue.setMaximum(6000)
        self.T2acqNoFilesValue.setObjectName("T2acqNoFilesValue")
        self.formLayout_9.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.T2acqNoFilesValue)
        self.gridLayout_10.addLayout(self.formLayout_9, 3, 0, 2, 1)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.T2modeTriple = QtWidgets.QRadioButton(self.T2acqGrp)
        self.T2modeTriple.setChecked(True)
        self.T2modeTriple.setObjectName("T2modeTriple")
        self.horizontalLayout_7.addWidget(self.T2modeTriple)
        self.T2modeDouble = QtWidgets.QRadioButton(self.T2acqGrp)
        self.T2modeDouble.setChecked(False)
        self.T2modeDouble.setObjectName("T2modeDouble")
        self.horizontalLayout_7.addWidget(self.T2modeDouble)
        self.gridLayout_10.addLayout(self.horizontalLayout_7, 0, 0, 1, 2)
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.T2filenameLabel = QtWidgets.QLabel(self.T2acqGrp)
        self.T2filenameLabel.setObjectName("T2filenameLabel")
        self.horizontalLayout_8.addWidget(self.T2filenameLabel)
        self.T2filenameBtn = QtWidgets.QPushButton(self.T2acqGrp)
        self.T2filenameBtn.setObjectName("T2filenameBtn")
        self.horizontalLayout_8.addWidget(self.T2filenameBtn)
        self.T2filenameValue = QtWidgets.QLineEdit(self.T2acqGrp)
        self.T2filenameValue.setClearButtonEnabled(True)
        self.T2filenameValue.setObjectName("T2filenameValue")
        self.horizontalLayout_8.addWidget(self.T2filenameValue)
        self.gridLayout_10.addLayout(self.horizontalLayout_8, 6, 0, 1, 3)
        self.formLayout_10 = QtWidgets.QFormLayout()
        self.formLayout_10.setObjectName("formLayout_10")
        self.T2timeGateLongLabel = QtWidgets.QLabel(self.T2acqGrp)
        self.T2timeGateLongLabel.setObjectName("T2timeGateLongLabel")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.T2timeGateLongLabel)
        self.T2timeGateShortLabel = QtWidgets.QLabel(self.T2acqGrp)
        self.T2timeGateShortLabel.setObjectName("T2timeGateShortLabel")
        self.formLayout_10.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.T2timeGateShortLabel)
        self.T2timeGateLongValue = QtWidgets.QSpinBox(self.T2acqGrp)
        self.T2timeGateLongValue.setMaximum(20000)
        self.T2timeGateLongValue.setObjectName("T2timeGateLongValue")
        self.formLayout_10.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.T2timeGateLongValue)
        self.T2timeGateShortValue = QtWidgets.QSpinBox(self.T2acqGrp)
        self.T2timeGateShortValue.setMaximum(20000)
        self.T2timeGateShortValue.setObjectName("T2timeGateShortValue")
        self.formLayout_10.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.T2timeGateShortValue)
        self.gridLayout_10.addLayout(self.formLayout_10, 3, 1, 2, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.T2startBtn = QtWidgets.QPushButton(self.T2acqGrp)
        self.T2startBtn.setMinimumSize(QtCore.QSize(197, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.T2startBtn.setFont(font)
        self.T2startBtn.setObjectName("T2startBtn")
        self.horizontalLayout_9.addWidget(self.T2startBtn)
        self.T2stopBtn = QtWidgets.QPushButton(self.T2acqGrp)
        self.T2stopBtn.setMinimumSize(QtCore.QSize(196, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.T2stopBtn.setFont(font)
        self.T2stopBtn.setObjectName("T2stopBtn")
        self.horizontalLayout_9.addWidget(self.T2stopBtn)
        self.gridLayout_10.addLayout(self.horizontalLayout_9, 7, 1, 1, 2)
        self.line = QtWidgets.QFrame(self.T2acqGrp)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout_10.addWidget(self.line, 1, 0, 1, 3)
        self.label_12 = QtWidgets.QLabel(self.T2acqGrp)
        self.label_12.setObjectName("label_12")
        self.gridLayout_10.addWidget(self.label_12, 2, 0, 1, 1)
        self.T2doHistChk = QtWidgets.QCheckBox(self.T2acqGrp)
        self.T2doHistChk.setObjectName("T2doHistChk")
        self.gridLayout_10.addWidget(self.T2doHistChk, 5, 0, 1, 1)
        self.line.raise_()
        self.label_12.raise_()
        self.T2doHistChk.raise_()
        self.label_17.raise_()
        self.verticalLayout.addWidget(self.T2acqGrp)
        self.progGrp = QtWidgets.QGroupBox(self.centralwidget)
        self.progGrp.setObjectName("progGrp")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.progGrp)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.splitter = QtWidgets.QSplitter(self.progGrp)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.layoutWidget = QtWidgets.QWidget(self.splitter)
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_4.addWidget(self.label_2)
        self.commandOutput = QtWidgets.QPlainTextEdit(self.layoutWidget)
        self.commandOutput.setMinimumSize(QtCore.QSize(321, 179))
        self.commandOutput.setReadOnly(True)
        self.commandOutput.setPlainText("")
        self.commandOutput.setObjectName("commandOutput")
        self.verticalLayout_4.addWidget(self.commandOutput)
        self.layoutWidget1 = QtWidgets.QWidget(self.splitter)
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_3.addWidget(self.label_3)
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.acqProgLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.acqProgLabel.setObjectName("acqProgLabel")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.acqProgLabel)
        self.acqProgBar = QtWidgets.QProgressBar(self.layoutWidget1)
        self.acqProgBar.setProperty("value", 0)
        self.acqProgBar.setObjectName("acqProgBar")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.acqProgBar)
        self.acqProgFileLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.acqProgFileLabel.setObjectName("acqProgFileLabel")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.acqProgFileLabel)
        self.acqProgFileBar = QtWidgets.QProgressBar(self.layoutWidget1)
        self.acqProgFileBar.setProperty("value", 0)
        self.acqProgFileBar.setObjectName("acqProgFileBar")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.acqProgFileBar)
        self.verticalLayout_3.addLayout(self.formLayout)
        self.label_34 = QtWidgets.QLabel(self.layoutWidget1)
        self.label_34.setObjectName("label_34")
        self.verticalLayout_3.addWidget(self.label_34)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.rateSyncLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.rateSyncLabel.setObjectName("rateSyncLabel")
        self.gridLayout.addWidget(self.rateSyncLabel, 0, 0, 1, 1)
        self.rateChn1Label = QtWidgets.QLabel(self.layoutWidget1)
        self.rateChn1Label.setObjectName("rateChn1Label")
        self.gridLayout.addWidget(self.rateChn1Label, 0, 1, 1, 1)
        self.rateChn2Label = QtWidgets.QLabel(self.layoutWidget1)
        self.rateChn2Label.setObjectName("rateChn2Label")
        self.gridLayout.addWidget(self.rateChn2Label, 0, 2, 1, 1)
        self.rateSyncValue = QtWidgets.QLCDNumber(self.layoutWidget1)
        self.rateSyncValue.setFrameShadow(QtWidgets.QFrame.Plain)
        self.rateSyncValue.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.rateSyncValue.setObjectName("rateSyncValue")
        self.gridLayout.addWidget(self.rateSyncValue, 1, 0, 1, 1)
        self.rateChn1Value = QtWidgets.QLCDNumber(self.layoutWidget1)
        self.rateChn1Value.setFrameShadow(QtWidgets.QFrame.Plain)
        self.rateChn1Value.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.rateChn1Value.setObjectName("rateChn1Value")
        self.gridLayout.addWidget(self.rateChn1Value, 1, 1, 1, 1)
        self.rateChn2Value = QtWidgets.QLCDNumber(self.layoutWidget1)
        self.rateChn2Value.setFrameShadow(QtWidgets.QFrame.Plain)
        self.rateChn2Value.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.rateChn2Value.setObjectName("rateChn2Value")
        self.gridLayout.addWidget(self.rateChn2Value, 1, 2, 1, 1)
        self.rateDoubleLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.rateDoubleLabel.setObjectName("rateDoubleLabel")
        self.gridLayout.addWidget(self.rateDoubleLabel, 2, 0, 1, 1)
        self.rateTripleLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.rateTripleLabel.setObjectName("rateTripleLabel")
        self.gridLayout.addWidget(self.rateTripleLabel, 2, 1, 1, 1)
        self.rateTotalLabel = QtWidgets.QLabel(self.layoutWidget1)
        self.rateTotalLabel.setObjectName("rateTotalLabel")
        self.gridLayout.addWidget(self.rateTotalLabel, 2, 2, 1, 1)
        self.rateDoubleValue = QtWidgets.QLCDNumber(self.layoutWidget1)
        self.rateDoubleValue.setFrameShadow(QtWidgets.QFrame.Plain)
        self.rateDoubleValue.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.rateDoubleValue.setObjectName("rateDoubleValue")
        self.gridLayout.addWidget(self.rateDoubleValue, 3, 0, 1, 1)
        self.rateTripleValue = QtWidgets.QLCDNumber(self.layoutWidget1)
        self.rateTripleValue.setFrameShadow(QtWidgets.QFrame.Plain)
        self.rateTripleValue.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.rateTripleValue.setObjectName("rateTripleValue")
        self.gridLayout.addWidget(self.rateTripleValue, 3, 1, 1, 1)
        self.rateTotalValue = QtWidgets.QLCDNumber(self.layoutWidget1)
        self.rateTotalValue.setFrameShadow(QtWidgets.QFrame.Plain)
        self.rateTotalValue.setDigitCount(12)
        self.rateTotalValue.setSegmentStyle(QtWidgets.QLCDNumber.Flat)
        self.rateTotalValue.setObjectName("rateTotalValue")
        self.gridLayout.addWidget(self.rateTotalValue, 3, 2, 1, 1)
        self.verticalLayout_3.addLayout(self.gridLayout)
        self.gridLayout_3.addWidget(self.splitter, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.progGrp)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 717, 20))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.T2settingsGrp.setTitle(_translate("MainWindow", "Settings"))
        self.label_9.setText(_translate("MainWindow", "Sync / channel 0 (1274 keV)"))
        self.T2chn1Chk.setText(_translate("MainWindow", "Channel 1 (511 keV)"))
        self.T2chn2Chk.setText(_translate("MainWindow", "Channel 2 (511 keV)"))
        self.T2syncZeroLabel.setText(_translate("MainWindow", "CFD zero cross (mV)"))
        self.T2syncLevelLabel.setText(_translate("MainWindow", "CFD level (mV)"))
        self.T2syncOffsetLabel.setText(_translate("MainWindow", "Chn offset (ps)"))
        self.T2chn1ZeroLabel.setText(_translate("MainWindow", "CFD zero cross (mV)"))
        self.T2chn1LevelLabel.setText(_translate("MainWindow", "CFD level (mV)"))
        self.label.setText(_translate("MainWindow", "Chn offset (ps)"))
        self.T2chn2ZeroLabel.setText(_translate("MainWindow", "CFD zero cross (mV)"))
        self.T2chn2LevelLabel.setText(_translate("MainWindow", "CFD level (mV)"))
        self.T2chn2OffsetLabel.setText(_translate("MainWindow", "Chn offset (ps)"))
        self.T2saveDefaultPrmBtn.setText(_translate("MainWindow", "Save current parameters as default"))
        self.T2applySetBtn.setText(_translate("MainWindow", "Apply settings"))
        self.T2acqGrp.setTitle(_translate("MainWindow", "Acquisition"))
        self.label_17.setText(_translate("MainWindow", "Gating parameters"))
        self.T2acqTimePerFileLabel.setText(_translate("MainWindow", "Acq time per file (min)"))
        self.T2acqNoFilesLabel.setText(_translate("MainWindow", "Total number of files"))
        self.T2modeTriple.setText(_translate("MainWindow", "Triple coincidence"))
        self.T2modeDouble.setText(_translate("MainWindow", "Double coincidence"))
        self.T2filenameLabel.setText(_translate("MainWindow", "Output file name"))
        self.T2filenameBtn.setText(_translate("MainWindow", "Pick a file"))
        self.T2timeGateLongLabel.setText(_translate("MainWindow", "time gate long (ps)"))
        self.T2timeGateShortLabel.setText(_translate("MainWindow", "time gate 511 (ps)"))
        self.T2startBtn.setText(_translate("MainWindow", "Start"))
        self.T2stopBtn.setText(_translate("MainWindow", "Stop"))
        self.label_12.setText(_translate("MainWindow", "Acquisition parameters"))
        self.T2doHistChk.setText(_translate("MainWindow", "Do histrogramming"))
        self.progGrp.setTitle(_translate("MainWindow", "Progress and control"))
        self.label_2.setText(_translate("MainWindow", "Commnand output"))
        self.commandOutput.setPlaceholderText(_translate("MainWindow", "Command output"))
        self.label_3.setText(_translate("MainWindow", "Acquisition progress"))
        self.acqProgLabel.setText(_translate("MainWindow", "Current acquisition"))
        self.acqProgFileLabel.setText(_translate("MainWindow", "Current file"))
        self.label_34.setText(_translate("MainWindow", "Counting rates (cnts/sec):"))
        self.rateSyncLabel.setText(_translate("MainWindow", "Sync/chn 0"))
        self.rateChn1Label.setText(_translate("MainWindow", "channel 1"))
        self.rateChn2Label.setText(_translate("MainWindow", "channel 2"))
        self.rateDoubleLabel.setText(_translate("MainWindow", "Double coinc"))
        self.rateTripleLabel.setText(_translate("MainWindow", "Triple coinc"))
        self.rateTotalLabel.setText(_translate("MainWindow", "Total"))

