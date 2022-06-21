# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'EditRemoveFileHK.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_dialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(319, 124)
        self.verticalLayout = QVBoxLayout(dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.lineEdit = QLineEdit(dialog)
        self.lineEdit.setObjectName(u"lineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.lineEdit)

        self.pushButton = QPushButton(dialog)
        self.pushButton.setObjectName(u"pushButton")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.pushButton)

        self.label_2 = QLabel(dialog)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.label_2)

        self.pushButton_2 = QPushButton(dialog)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.pushButton_2)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)

        QMetaObject.connectSlotsByName(dialog)
    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Add or edit hotkey", None))
        self.pushButton.setText(QCoreApplication.translate("dialog", u"Set keys", None))
        self.label_2.setText(QCoreApplication.translate("dialog", u"Awaiting input", None))
        self.pushButton_2.setText(QCoreApplication.translate("dialog", u"Select file", None))
    # retranslateUi

