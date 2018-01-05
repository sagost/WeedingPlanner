# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'weeding_parameter.ui'
#
# Created: Wed Apr 20 13:14:29 2016
#      by: PyQt4 UI code generator 4.10.4
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

class Ui_WeedingParameter(object):
    def setupUi(self, WeedingParameter):
        WeedingParameter.setObjectName(_fromUtf8("WeedingParameter"))
        WeedingParameter.resize(564, 308)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(WeedingParameter.sizePolicy().hasHeightForWidth())
        WeedingParameter.setSizePolicy(sizePolicy)
        self.formLayout_3 = QtGui.QFormLayout(WeedingParameter)
        self.formLayout_3.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.formLayout_3.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_3.setObjectName(_fromUtf8("formLayout_3"))
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.formLayout_3.setItem(1, QtGui.QFormLayout.LabelRole, spacerItem)
        self.groupBox = QtGui.QGroupBox(WeedingParameter)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox.setMaximum(1000.99)
        self.doubleSpinBox.setSingleStep(0.5)
        self.doubleSpinBox.setProperty("value", 0.5)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.horizontalLayout_2.addWidget(self.doubleSpinBox)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_2.setMaximum(1000.99)
        self.doubleSpinBox_2.setSingleStep(0.5)
        self.doubleSpinBox_2.setProperty("value", 0.5)
        self.doubleSpinBox_2.setObjectName(_fromUtf8("doubleSpinBox_2"))
        self.horizontalLayout.addWidget(self.doubleSpinBox_2)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_5.addWidget(self.label_2)
        self.doubleSpinBox_4 = QtGui.QDoubleSpinBox(self.groupBox)
        self.doubleSpinBox_4.setObjectName(_fromUtf8("doubleSpinBox_4"))
        self.horizontalLayout_5.addWidget(self.doubleSpinBox_4)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.formLayout_3.setWidget(2, QtGui.QFormLayout.LabelRole, self.groupBox)
        self.buttonBox = QtGui.QDialogButtonBox(WeedingParameter)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayout_3.setWidget(3, QtGui.QFormLayout.LabelRole, self.buttonBox)
        self.groupBox_2 = QtGui.QGroupBox(WeedingParameter)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.formLayout_2 = QtGui.QFormLayout(self.groupBox_2)
        self.formLayout_2.setObjectName(_fromUtf8("formLayout_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_4.addWidget(self.label)
        self.spinBox = QtGui.QSpinBox(self.groupBox_2)
        self.spinBox.setMinimum(1)
        self.spinBox.setObjectName(_fromUtf8("spinBox"))
        self.horizontalLayout_4.addWidget(self.spinBox)
        self.formLayout_2.setLayout(0, QtGui.QFormLayout.LabelRole, self.horizontalLayout_4)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout_3.addWidget(self.label_10)
        self.comboBox_3 = QtGui.QComboBox(self.groupBox_2)
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.horizontalLayout_3.addWidget(self.comboBox_3)
        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_3.addWidget(self.label_9)
        self.doubleSpinBox_3 = QtGui.QDoubleSpinBox(self.groupBox_2)
        self.doubleSpinBox_3.setMinimum(-1000000.0)
        self.doubleSpinBox_3.setMaximum(10000000.0)
        self.doubleSpinBox_3.setProperty("value", 1.0)
        self.doubleSpinBox_3.setObjectName(_fromUtf8("doubleSpinBox_3"))
        self.horizontalLayout_3.addWidget(self.doubleSpinBox_3)
        self.formLayout_2.setLayout(1, QtGui.QFormLayout.LabelRole, self.horizontalLayout_3)
        self.formLayout_3.setWidget(0, QtGui.QFormLayout.LabelRole, self.groupBox_2)

        self.retranslateUi(WeedingParameter)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), WeedingParameter.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), WeedingParameter.reject)
        QtCore.QMetaObject.connectSlotsByName(WeedingParameter)

    def retranslateUi(self, WeedingParameter):
        WeedingParameter.setWindowTitle(_translate("WeedingParameter", "Dialog", None))
        self.groupBox.setTitle(_translate("WeedingParameter", "Define weeding area minimum dimension: ", None))
        self.label_3.setText(_translate("WeedingParameter", "Vertical dimension in m. ", None))
        self.label_4.setText(_translate("WeedingParameter", "Horizontal dimension in m. ", None))
        self.label_2.setText(_translate("WeedingParameter", "Minimum distance between weeding areas in m. ", None))
        self.groupBox_2.setTitle(_translate("WeedingParameter", "Select NDVI Band Classification rule:", None))
        self.label.setText(_translate("WeedingParameter", "Select Band:", None))
        self.label_10.setText(_translate("WeedingParameter", "\"Band Value\" ", None))
        self.comboBox_3.setItemText(0, _translate("WeedingParameter", ">=", None))
        self.comboBox_3.setItemText(1, _translate("WeedingParameter", "<=", None))
        self.comboBox_3.setItemText(2, _translate("WeedingParameter", "=", None))
        self.comboBox_3.setItemText(3, _translate("WeedingParameter", ">", None))
        self.comboBox_3.setItemText(4, _translate("WeedingParameter", "<", None))
        self.label_9.setText(_translate("WeedingParameter", "    Then:", None))

