# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AddEditFileDialog.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDialog, QFormLayout, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

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

        self.formLayout.setWidget(0, QFormLayout.ItemRole.LabelRole, self.bChooseFile)

        self.leFilePath = QLineEdit(AddEditFileDialog)
        self.leFilePath.setObjectName(u"leFilePath")

        self.formLayout.setWidget(0, QFormLayout.ItemRole.FieldRole, self.leFilePath)

        self.label = QLabel(AddEditFileDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.ItemRole.LabelRole, self.label)

        self.buttonPlaceholder = QVBoxLayout()
        self.buttonPlaceholder.setObjectName(u"buttonPlaceholder")

        self.formLayout.setLayout(1, QFormLayout.ItemRole.FieldRole, self.buttonPlaceholder)


        self.verticalLayout.addLayout(self.formLayout)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

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

