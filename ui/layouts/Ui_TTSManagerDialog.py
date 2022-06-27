# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TTSManagerDialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_TTSManagerDialog(object):
    def setupUi(self, TTSManagerDialog):
        if not TTSManagerDialog.objectName():
            TTSManagerDialog.setObjectName(u"TTSManagerDialog")
        TTSManagerDialog.resize(500, 330)
        self.verticalLayout = QVBoxLayout(TTSManagerDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(TTSManagerDialog)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.cbLanguage = QComboBox(TTSManagerDialog)
        self.cbLanguage.setObjectName(u"cbLanguage")
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbLanguage.sizePolicy().hasHeightForWidth())
        self.cbLanguage.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.cbLanguage)

        self.label_2 = QLabel(TTSManagerDialog)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout.addWidget(self.label_2)

        self.teText = QTextEdit(TTSManagerDialog)
        self.teText.setObjectName(u"teText")

        self.verticalLayout.addWidget(self.teText)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.bTranslate = QPushButton(TTSManagerDialog)
        self.bTranslate.setObjectName(u"bTranslate")

        self.horizontalLayout.addWidget(self.bTranslate)

        self.bGenerate = QPushButton(TTSManagerDialog)
        self.bGenerate.setObjectName(u"bGenerate")

        self.horizontalLayout.addWidget(self.bGenerate)

        self.bCancel = QPushButton(TTSManagerDialog)
        self.bCancel.setObjectName(u"bCancel")

        self.horizontalLayout.addWidget(self.bCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(TTSManagerDialog)

        self.bGenerate.setDefault(True)


        QMetaObject.connectSlotsByName(TTSManagerDialog)
    # setupUi

    def retranslateUi(self, TTSManagerDialog):
        TTSManagerDialog.setWindowTitle(QCoreApplication.translate("TTSManagerDialog", u"TTS Manager", None))
        self.label.setText(QCoreApplication.translate("TTSManagerDialog", u"Language", None))
        self.label_2.setText(QCoreApplication.translate("TTSManagerDialog", u"Text, that will be changed to speech", None))
        self.teText.setPlaceholderText(QCoreApplication.translate("TTSManagerDialog", u"Lorem ipsum dolor sit amet", None))
#if QT_CONFIG(statustip)
        self.bTranslate.setStatusTip(QCoreApplication.translate("TTSManagerDialog", u"Translates the english text into desired language", None))
#endif // QT_CONFIG(statustip)
        self.bTranslate.setText(QCoreApplication.translate("TTSManagerDialog", u"Translate from EN", None))
        self.bGenerate.setText(QCoreApplication.translate("TTSManagerDialog", u"Generate", None))
        self.bCancel.setText(QCoreApplication.translate("TTSManagerDialog", u"Cancel", None))
    # retranslateUi

