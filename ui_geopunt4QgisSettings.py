# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_geopunt4QgisSettings.ui'
#
# Created: Fri Dec 27 11:52:43 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_settingsDlg(object):
    def setupUi(self, settingsDlg):
        settingsDlg.setObjectName(_fromUtf8("settingsDlg"))
        settingsDlg.resize(441, 343)
        self.verticalLayout = QtGui.QVBoxLayout(settingsDlg)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.settingsTab = QtGui.QToolBox(settingsDlg)
        self.settingsTab.setObjectName(_fromUtf8("settingsTab"))
        self.adresTab = QtGui.QWidget()
        self.adresTab.setGeometry(QtCore.QRect(0, 0, 423, 213))
        self.adresTab.setObjectName(_fromUtf8("adresTab"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.adresTab)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.add2mapBox_1 = QtGui.QGroupBox(self.adresTab)
        self.add2mapBox_1.setObjectName(_fromUtf8("add2mapBox_1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.add2mapBox_1)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.adresSavetoFileChk = QtGui.QRadioButton(self.add2mapBox_1)
        self.adresSavetoFileChk.setObjectName(_fromUtf8("adresSavetoFileChk"))
        self.verticalLayout_2.addWidget(self.adresSavetoFileChk)
        self.adresSaveMemoryChk = QtGui.QRadioButton(self.add2mapBox_1)
        self.adresSaveMemoryChk.setChecked(True)
        self.adresSaveMemoryChk.setObjectName(_fromUtf8("adresSaveMemoryChk"))
        self.verticalLayout_2.addWidget(self.adresSaveMemoryChk)
        self.label_1 = QtGui.QLabel(self.add2mapBox_1)
        self.label_1.setObjectName(_fromUtf8("label_1"))
        self.verticalLayout_2.addWidget(self.label_1)
        self.adresLayerTxt = QtGui.QLineEdit(self.add2mapBox_1)
        self.adresLayerTxt.setObjectName(_fromUtf8("adresLayerTxt"))
        self.verticalLayout_2.addWidget(self.adresLayerTxt)
        self.verticalLayout_3.addWidget(self.add2mapBox_1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_3.addItem(spacerItem)
        self.settingsTab.addItem(self.adresTab, _fromUtf8(""))
        self.reverseTab = QtGui.QWidget()
        self.reverseTab.setGeometry(QtCore.QRect(0, 0, 423, 213))
        self.reverseTab.setObjectName(_fromUtf8("reverseTab"))
        self.verticalLayout_5 = QtGui.QVBoxLayout(self.reverseTab)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.add2mapBox_2 = QtGui.QGroupBox(self.reverseTab)
        self.add2mapBox_2.setObjectName(_fromUtf8("add2mapBox_2"))
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.add2mapBox_2)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.reverseSavetoFileChk = QtGui.QRadioButton(self.add2mapBox_2)
        self.reverseSavetoFileChk.setObjectName(_fromUtf8("reverseSavetoFileChk"))
        self.verticalLayout_4.addWidget(self.reverseSavetoFileChk)
        self.reverseSaveMemoryChk = QtGui.QRadioButton(self.add2mapBox_2)
        self.reverseSaveMemoryChk.setChecked(True)
        self.reverseSaveMemoryChk.setObjectName(_fromUtf8("reverseSaveMemoryChk"))
        self.verticalLayout_4.addWidget(self.reverseSaveMemoryChk)
        self.label_2 = QtGui.QLabel(self.add2mapBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_4.addWidget(self.label_2)
        self.reverseLayerTxt = QtGui.QLineEdit(self.add2mapBox_2)
        self.reverseLayerTxt.setObjectName(_fromUtf8("reverseLayerTxt"))
        self.verticalLayout_4.addWidget(self.reverseLayerTxt)
        self.verticalLayout_5.addWidget(self.add2mapBox_2)
        spacerItem1 = QtGui.QSpacerItem(20, 75, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.settingsTab.addItem(self.reverseTab, _fromUtf8(""))
        self.poiTab = QtGui.QWidget()
        self.poiTab.setGeometry(QtCore.QRect(0, 0, 423, 213))
        self.poiTab.setObjectName(_fromUtf8("poiTab"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.poiTab)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.add2mapBox_3 = QtGui.QGroupBox(self.poiTab)
        self.add2mapBox_3.setObjectName(_fromUtf8("add2mapBox_3"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.add2mapBox_3)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.poiSavetoFileChk = QtGui.QRadioButton(self.add2mapBox_3)
        self.poiSavetoFileChk.setObjectName(_fromUtf8("poiSavetoFileChk"))
        self.verticalLayout_6.addWidget(self.poiSavetoFileChk)
        self.poiSaveMemoryChk = QtGui.QRadioButton(self.add2mapBox_3)
        self.poiSaveMemoryChk.setChecked(True)
        self.poiSaveMemoryChk.setObjectName(_fromUtf8("poiSaveMemoryChk"))
        self.verticalLayout_6.addWidget(self.poiSaveMemoryChk)
        self.label_3 = QtGui.QLabel(self.add2mapBox_3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_6.addWidget(self.label_3)
        self.poiLayerTxt = QtGui.QLineEdit(self.add2mapBox_3)
        self.poiLayerTxt.setObjectName(_fromUtf8("poiLayerTxt"))
        self.verticalLayout_6.addWidget(self.poiLayerTxt)
        self.verticalLayout_7.addWidget(self.add2mapBox_3)
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_7.addItem(spacerItem2)
        self.settingsTab.addItem(self.poiTab, _fromUtf8(""))
        self.verticalLayout.addWidget(self.settingsTab)
        self.buttonBox = QtGui.QDialogButtonBox(settingsDlg)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(settingsDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), settingsDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), settingsDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(settingsDlg)

    def retranslateUi(self, settingsDlg):
        settingsDlg.setWindowTitle(QtGui.QApplication.translate("settingsDlg", "Instellingen", None, QtGui.QApplication.UnicodeUTF8))
        self.add2mapBox_1.setTitle(QtGui.QApplication.translate("settingsDlg", "Toevoegen punten aan de kaart", None, QtGui.QApplication.UnicodeUTF8))
        self.adresSavetoFileChk.setText(QtGui.QApplication.translate("settingsDlg", "Opslaan naar bestand ", None, QtGui.QApplication.UnicodeUTF8))
        self.adresSaveMemoryChk.setText(QtGui.QApplication.translate("settingsDlg", "Opslaan naar tijdelijke laag", None, QtGui.QApplication.UnicodeUTF8))
        self.label_1.setText(QtGui.QApplication.translate("settingsDlg", "Naam  van de laag met adrespunten:", None, QtGui.QApplication.UnicodeUTF8))
        self.settingsTab.setItemText(self.settingsTab.indexOf(self.adresTab), QtGui.QApplication.translate("settingsDlg", "Zoek naar adres", None, QtGui.QApplication.UnicodeUTF8))
        self.add2mapBox_2.setTitle(QtGui.QApplication.translate("settingsDlg", "Toevoegen punten aan de kaart", None, QtGui.QApplication.UnicodeUTF8))
        self.reverseSavetoFileChk.setText(QtGui.QApplication.translate("settingsDlg", "Opslaan naar bestand ", None, QtGui.QApplication.UnicodeUTF8))
        self.reverseSaveMemoryChk.setText(QtGui.QApplication.translate("settingsDlg", "Opslaan naar tijdelijke laag", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("settingsDlg", "Naam  van de laag met adrespunten:", None, QtGui.QApplication.UnicodeUTF8))
        self.settingsTab.setItemText(self.settingsTab.indexOf(self.reverseTab), QtGui.QApplication.translate("settingsDlg", "Prikken van een adres", None, QtGui.QApplication.UnicodeUTF8))
        self.add2mapBox_3.setTitle(QtGui.QApplication.translate("settingsDlg", "Toevoegen punten aan de kaart", None, QtGui.QApplication.UnicodeUTF8))
        self.poiSavetoFileChk.setText(QtGui.QApplication.translate("settingsDlg", "Opslaan naar bestand ", None, QtGui.QApplication.UnicodeUTF8))
        self.poiSaveMemoryChk.setText(QtGui.QApplication.translate("settingsDlg", "Opslaan naar tijdelijke laag", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("settingsDlg", "Naam  van de laag met adrespunten:", None, QtGui.QApplication.UnicodeUTF8))
        self.settingsTab.setItemText(self.settingsTab.indexOf(self.poiTab), QtGui.QApplication.translate("settingsDlg", "Zoeken naar plaatsen", None, QtGui.QApplication.UnicodeUTF8))

