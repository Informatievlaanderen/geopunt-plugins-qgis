# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_geopunt4QgisGIPOD.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_gipodDlg(object):
    def setupUi(self, gipodDlg):
        gipodDlg.setObjectName(_fromUtf8("gipodDlg"))
        gipodDlg.resize(517, 350)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(gipodDlg.sizePolicy().hasHeightForWidth())
        gipodDlg.setSizePolicy(sizePolicy)
        gipodDlg.setMinimumSize(QtCore.QSize(0, 350))
        gipodDlg.setMaximumSize(QtCore.QSize(16777215, 370))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geopunt4Qgis/images/geopuntGIPODsmall.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        gipodDlg.setWindowIcon(icon)
        gipodDlg.setLayoutDirection(QtCore.Qt.LeftToRight)
        gipodDlg.setAutoFillBackground(False)
        gipodDlg.setSizeGripEnabled(False)
        gipodDlg.setModal(False)
        self.verticalLayout = QtGui.QVBoxLayout(gipodDlg)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.typeBox = QtGui.QGroupBox(gipodDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.typeBox.sizePolicy().hasHeightForWidth())
        self.typeBox.setSizePolicy(sizePolicy)
        self.typeBox.setObjectName(_fromUtf8("typeBox"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.typeBox)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.workassignmentRadio = QtGui.QRadioButton(self.typeBox)
        self.workassignmentRadio.setChecked(True)
        self.workassignmentRadio.setObjectName(_fromUtf8("workassignmentRadio"))
        self.horizontalLayout.addWidget(self.workassignmentRadio)
        self.manifestationRadio = QtGui.QRadioButton(self.typeBox)
        self.manifestationRadio.setObjectName(_fromUtf8("manifestationRadio"))
        self.horizontalLayout.addWidget(self.manifestationRadio)
        self.verticalLayout.addWidget(self.typeBox)
        self.queryWgt = QtGui.QWidget(gipodDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.queryWgt.sizePolicy().hasHeightForWidth())
        self.queryWgt.setSizePolicy(sizePolicy)
        self.queryWgt.setObjectName(_fromUtf8("queryWgt"))
        self.gridLayout = QtGui.QGridLayout(self.queryWgt)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.startEdit = QtGui.QDateEdit(self.queryWgt)
        self.startEdit.setMinimumSize(QtCore.QSize(100, 0))
        self.startEdit.setDate(QtCore.QDate(2013, 1, 1))
        self.startEdit.setCalendarPopup(True)
        self.startEdit.setObjectName(_fromUtf8("startEdit"))
        self.gridLayout.addWidget(self.startEdit, 6, 1, 1, 1)
        self.endEdit = QtGui.QDateEdit(self.queryWgt)
        self.endEdit.setMinimumSize(QtCore.QSize(100, 0))
        self.endEdit.setDate(QtCore.QDate(2014, 1, 1))
        self.endEdit.setCalendarPopup(True)
        self.endEdit.setObjectName(_fromUtf8("endEdit"))
        self.gridLayout.addWidget(self.endEdit, 7, 1, 1, 1)
        self.startdatumLbl = QtGui.QLabel(self.queryWgt)
        self.startdatumLbl.setObjectName(_fromUtf8("startdatumLbl"))
        self.gridLayout.addWidget(self.startdatumLbl, 6, 0, 1, 1)
        self.einddatumLbl = QtGui.QLabel(self.queryWgt)
        self.einddatumLbl.setObjectName(_fromUtf8("einddatumLbl"))
        self.gridLayout.addWidget(self.einddatumLbl, 7, 0, 1, 1)
        self.stadLbl = QtGui.QLabel(self.queryWgt)
        self.stadLbl.setObjectName(_fromUtf8("stadLbl"))
        self.gridLayout.addWidget(self.stadLbl, 2, 0, 1, 1)
        self.extendChk = QtGui.QCheckBox(self.queryWgt)
        self.extendChk.setObjectName(_fromUtf8("extendChk"))
        self.gridLayout.addWidget(self.extendChk, 8, 0, 1, 2)
        self.cityCbx = QtGui.QComboBox(self.queryWgt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cityCbx.sizePolicy().hasHeightForWidth())
        self.cityCbx.setSizePolicy(sizePolicy)
        self.cityCbx.setMinimumSize(QtCore.QSize(100, 0))
        self.cityCbx.setEditable(False)
        self.cityCbx.setObjectName(_fromUtf8("cityCbx"))
        self.gridLayout.addWidget(self.cityCbx, 2, 1, 1, 1)
        self.manifestationlbl = QtGui.QLabel(self.queryWgt)
        self.manifestationlbl.setEnabled(False)
        self.manifestationlbl.setObjectName(_fromUtf8("manifestationlbl"))
        self.gridLayout.addWidget(self.manifestationlbl, 5, 0, 1, 1)
        self.eventCbx = QtGui.QComboBox(self.queryWgt)
        self.eventCbx.setEnabled(False)
        self.eventCbx.setEditable(False)
        self.eventCbx.setObjectName(_fromUtf8("eventCbx"))
        self.gridLayout.addWidget(self.eventCbx, 5, 1, 1, 1)
        self.provinceCbx = QtGui.QComboBox(self.queryWgt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.provinceCbx.sizePolicy().hasHeightForWidth())
        self.provinceCbx.setSizePolicy(sizePolicy)
        self.provinceCbx.setMinimumSize(QtCore.QSize(100, 0))
        self.provinceCbx.setEditable(False)
        self.provinceCbx.setObjectName(_fromUtf8("provinceCbx"))
        self.gridLayout.addWidget(self.provinceCbx, 1, 1, 1, 1)
        self.provncieLbl = QtGui.QLabel(self.queryWgt)
        self.provncieLbl.setObjectName(_fromUtf8("provncieLbl"))
        self.gridLayout.addWidget(self.provncieLbl, 1, 0, 1, 1)
        self.eigenaarLbl = QtGui.QLabel(self.queryWgt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.eigenaarLbl.sizePolicy().hasHeightForWidth())
        self.eigenaarLbl.setSizePolicy(sizePolicy)
        self.eigenaarLbl.setObjectName(_fromUtf8("eigenaarLbl"))
        self.gridLayout.addWidget(self.eigenaarLbl, 3, 0, 1, 1)
        self.ownerCbx = QtGui.QComboBox(self.queryWgt)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ownerCbx.sizePolicy().hasHeightForWidth())
        self.ownerCbx.setSizePolicy(sizePolicy)
        self.ownerCbx.setMinimumSize(QtCore.QSize(100, 0))
        self.ownerCbx.setEditable(False)
        self.ownerCbx.setObjectName(_fromUtf8("ownerCbx"))
        self.gridLayout.addWidget(self.ownerCbx, 3, 1, 1, 1)
        self.verticalLayout.addWidget(self.queryWgt)
        self.outputWgt = QtGui.QWidget(gipodDlg)
        self.outputWgt.setObjectName(_fromUtf8("outputWgt"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout(self.outputWgt)
        self.horizontalLayout_2.setContentsMargins(-1, 1, -1, 1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.laagNaamLbl = QtGui.QLabel(self.outputWgt)
        self.laagNaamLbl.setObjectName(_fromUtf8("laagNaamLbl"))
        self.horizontalLayout_2.addWidget(self.laagNaamLbl)
        self.lyrName = QtGui.QLineEdit(self.outputWgt)
        self.lyrName.setEnabled(True)
        self.lyrName.setText(_fromUtf8("GIPOD"))
        self.lyrName.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.lyrName.setPlaceholderText(_fromUtf8(""))
        self.lyrName.setObjectName(_fromUtf8("lyrName"))
        self.horizontalLayout_2.addWidget(self.lyrName)
        self.verticalLayout.addWidget(self.outputWgt)
        self.mgsBox = QtGui.QLabel(gipodDlg)
        self.mgsBox.setFrameShape(QtGui.QFrame.NoFrame)
        self.mgsBox.setFrameShadow(QtGui.QFrame.Plain)
        self.mgsBox.setText(_fromUtf8(""))
        self.mgsBox.setObjectName(_fromUtf8("mgsBox"))
        self.verticalLayout.addWidget(self.mgsBox)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(gipodDlg)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonBox.sizePolicy().hasHeightForWidth())
        self.buttonBox.setSizePolicy(sizePolicy)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Help)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.horizontalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi(gipodDlg)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), gipodDlg.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), gipodDlg.reject)
        QtCore.QObject.connect(self.manifestationRadio, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.eventCbx.setEnabled)
        QtCore.QObject.connect(self.manifestationRadio, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.manifestationlbl.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(gipodDlg)

    def retranslateUi(self, gipodDlg):
        gipodDlg.setWindowTitle(_translate("gipodDlg", "Bevraag GIPOD", None))
        self.typeBox.setTitle(_translate("gipodDlg", "Type", None))
        self.workassignmentRadio.setText(_translate("gipodDlg", "Werkopdracht", None))
        self.manifestationRadio.setText(_translate("gipodDlg", "Manifestatie", None))
        self.startEdit.setDisplayFormat(_translate("gipodDlg", "dd/MM/yyyy", None))
        self.endEdit.setDisplayFormat(_translate("gipodDlg", "dd/MM/yyyy", None))
        self.startdatumLbl.setText(_translate("gipodDlg", "Startdatum:", None))
        self.einddatumLbl.setText(_translate("gipodDlg", "Einddatum:", None))
        self.stadLbl.setText(_translate("gipodDlg", "Stad of gemeente:", None))
        self.extendChk.setText(_translate("gipodDlg", "Beperk zoekresultaten tot huidig zoomniveau", None))
        self.manifestationlbl.setText(_translate("gipodDlg", "Type manifestatie:", None))
        self.provncieLbl.setText(_translate("gipodDlg", "Provincie:", None))
        self.eigenaarLbl.setText(_translate("gipodDlg", "Eigenaar: ", None))
        self.laagNaamLbl.setText(_translate("gipodDlg", "Laagnaam:", None))

import resources_rc
