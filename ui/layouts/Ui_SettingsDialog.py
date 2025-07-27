# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'SettingsDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QDialog,
    QFormLayout, QGridLayout, QHBoxLayout, QLabel,
    QPushButton, QSizePolicy, QSpacerItem, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        if not SettingsDialog.objectName():
            SettingsDialog.setObjectName(u"SettingsDialog")
        SettingsDialog.resize(340, 267)
        self.verticalLayout = QVBoxLayout(SettingsDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(SettingsDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.cbDeviceSelector = QComboBox(SettingsDialog)
        self.cbDeviceSelector.setObjectName(u"cbDeviceSelector")

        self.verticalLayout.addWidget(self.cbDeviceSelector)

        self.cPlayOnMain = QCheckBox(SettingsDialog)
        self.cPlayOnMain.setObjectName(u"cPlayOnMain")

        self.verticalLayout.addWidget(self.cPlayOnMain)

        self.cPlaySingle = QCheckBox(SettingsDialog)
        self.cPlaySingle.setObjectName(u"cPlaySingle")

        self.verticalLayout.addWidget(self.cPlaySingle)

        self.glHotkeys = QGridLayout()
        self.glHotkeys.setObjectName(u"glHotkeys")

        self.verticalLayout.addLayout(self.glHotkeys)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.label_6 = QLabel(SettingsDialog)
        self.label_6.setObjectName(u"label_6")

        self.horizontalLayout.addWidget(self.label_6)

        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.lWindowPos = QLabel(SettingsDialog)
        self.lWindowPos.setObjectName(u"lWindowPos")

        self.horizontalLayout.addWidget(self.lWindowPos)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.sbVerticalWin = QSpinBox(SettingsDialog)
        self.sbVerticalWin.setObjectName(u"sbVerticalWin")
        self.sbVerticalWin.setMaximum(10000)

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.LabelRole, self.sbVerticalWin)

        self.label_7 = QLabel(SettingsDialog)
        self.label_7.setObjectName(u"label_7")

        self.formLayout_2.setWidget(0, QFormLayout.ItemRole.FieldRole, self.label_7)

        self.sbHorizontalWin = QSpinBox(SettingsDialog)
        self.sbHorizontalWin.setObjectName(u"sbHorizontalWin")
        self.sbHorizontalWin.setMaximum(10000)

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.LabelRole, self.sbHorizontalWin)

        self.label_8 = QLabel(SettingsDialog)
        self.label_8.setObjectName(u"label_8")

        self.formLayout_2.setWidget(1, QFormLayout.ItemRole.FieldRole, self.label_8)


        self.verticalLayout.addLayout(self.formLayout_2)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout_2.addItem(self.horizontalSpacer_2)

        self.bSave = QPushButton(SettingsDialog)
        self.bSave.setObjectName(u"bSave")

        self.horizontalLayout_2.addWidget(self.bSave)

        self.bCancel = QPushButton(SettingsDialog)
        self.bCancel.setObjectName(u"bCancel")

        self.horizontalLayout_2.addWidget(self.bCancel)


        self.verticalLayout.addLayout(self.horizontalLayout_2)


        self.retranslateUi(SettingsDialog)

        self.bSave.setDefault(True)


        QMetaObject.connectSlotsByName(SettingsDialog)
    # setupUi

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(QCoreApplication.translate("SettingsDialog", u"Change settings", None))
        self.label.setText(QCoreApplication.translate("SettingsDialog", u"Additional device", None))
        self.cPlayOnMain.setText(QCoreApplication.translate("SettingsDialog", u"Play on main device too", None))
        self.cPlaySingle.setText(QCoreApplication.translate("SettingsDialog", u"Play only one sound at once", None))
        self.label_6.setText(QCoreApplication.translate("SettingsDialog", u"Current window position:", None))
        self.lWindowPos.setText(QCoreApplication.translate("SettingsDialog", u"[POSITION]", None))
        self.label_7.setText(QCoreApplication.translate("SettingsDialog", u"Vertical window pos", None))
        self.label_8.setText(QCoreApplication.translate("SettingsDialog", u"Horizontal window pos", None))
        self.bSave.setText(QCoreApplication.translate("SettingsDialog", u"Save", None))
        self.bCancel.setText(QCoreApplication.translate("SettingsDialog", u"Cancel", None))
    # retranslateUi

