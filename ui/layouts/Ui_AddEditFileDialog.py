# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AddEditFileDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QMetaObject,
)
from PySide6.QtWidgets import (
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QVBoxLayout,
)


class Ui_AddEditFileDialog(object):
    def setupUi(self, AddEditFileDialog):
        if not AddEditFileDialog.objectName():
            AddEditFileDialog.setObjectName("AddEditFileDialog")
        AddEditFileDialog.resize(360, 129)
        self.verticalLayout = QVBoxLayout(AddEditFileDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.formLayout.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.bChooseFile = QPushButton(AddEditFileDialog)
        self.bChooseFile.setObjectName("bChooseFile")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.bChooseFile)

        self.leFilePath = QLineEdit(AddEditFileDialog)
        self.leFilePath.setObjectName("leFilePath")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.leFilePath)

        self.label = QLabel(AddEditFileDialog)
        self.label.setObjectName("label")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label)

        self.buttonPlaceholder = QVBoxLayout()
        self.buttonPlaceholder.setObjectName("buttonPlaceholder")

        self.formLayout.setLayout(
            1, QFormLayout.ItemRole.FieldRole, self.buttonPlaceholder
        )

        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.bSave = QPushButton(AddEditFileDialog)
        self.bSave.setObjectName("bSave")

        self.horizontalLayout.addWidget(self.bSave)

        self.bCancel = QPushButton(AddEditFileDialog)
        self.bCancel.setObjectName("bCancel")

        self.horizontalLayout.addWidget(self.bCancel)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(AddEditFileDialog)

        self.bSave.setDefault(True)

        QMetaObject.connectSlotsByName(AddEditFileDialog)

    # setupUi

    def retranslateUi(self, AddEditFileDialog):
        AddEditFileDialog.setWindowTitle(
            QCoreApplication.translate("AddEditFileDialog", "Add or edit hotkey", None)
        )
        self.bChooseFile.setText(
            QCoreApplication.translate("AddEditFileDialog", "Select file", None)
        )
        # if QT_CONFIG(tooltip)
        self.leFilePath.setToolTip("")
        # endif // QT_CONFIG(tooltip)
        self.leFilePath.setPlaceholderText(
            QCoreApplication.translate("AddEditFileDialog", "Path to file", None)
        )
        self.label.setText(
            QCoreApplication.translate("AddEditFileDialog", "Key combination:", None)
        )
        self.bSave.setText(
            QCoreApplication.translate("AddEditFileDialog", "Save", None)
        )
        self.bCancel.setText(
            QCoreApplication.translate("AddEditFileDialog", "Cancel", None)
        )

    # retranslateUi
