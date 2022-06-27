# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AddEditFileDialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_AddEditFileDialog(object):
    def setupUi(self, AddEditFileDialog):
        if not AddEditFileDialog.objectName():
            AddEditFileDialog.setObjectName(u"AddEditFileDialog")
        AddEditFileDialog.resize(360, 129)
        self.verticalLayout = QVBoxLayout(AddEditFileDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.bChooseFile = QPushButton(AddEditFileDialog)
        self.bChooseFile.setObjectName(u"bChooseFile")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.bChooseFile)

        self.leFilePath = QLineEdit(AddEditFileDialog)
        self.leFilePath.setObjectName(u"leFilePath")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.leFilePath)

        self.label = QLabel(AddEditFileDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label)

        self.buttonPlaceholder = QVBoxLayout()
        self.buttonPlaceholder.setObjectName(u"buttonPlaceholder")

        self.formLayout.setLayout(1, QFormLayout.FieldRole, self.buttonPlaceholder)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.bSave = QPushButton(AddEditFileDialog)
        self.bSave.setObjectName(u"bSave")

        self.horizontalLayout.addWidget(self.bSave)

        self.bCancel = QPushButton(AddEditFileDialog)
        self.bCancel.setObjectName(u"bCancel")

        self.horizontalLayout.addWidget(self.bCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(AddEditFileDialog)

        self.bSave.setDefault(True)


        QMetaObject.connectSlotsByName(AddEditFileDialog)
    # setupUi

    def retranslateUi(self, AddEditFileDialog):
        AddEditFileDialog.setWindowTitle(QCoreApplication.translate("AddEditFileDialog", u"Add or edit hotkey", None))
        self.bChooseFile.setText(QCoreApplication.translate("AddEditFileDialog", u"Select file", None))
#if QT_CONFIG(tooltip)
        self.leFilePath.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.leFilePath.setPlaceholderText(QCoreApplication.translate("AddEditFileDialog", u"Path to file", None))
        self.label.setText(QCoreApplication.translate("AddEditFileDialog", u"Key combination:", None))
        self.bSave.setText(QCoreApplication.translate("AddEditFileDialog", u"Save", None))
        self.bCancel.setText(QCoreApplication.translate("AddEditFileDialog", u"Cancel", None))
    # retranslateUi

