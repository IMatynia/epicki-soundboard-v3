# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'YoutubeDialog.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_AddYoutubeDL(object):
    def setupUi(self, AddYoutubeDL):
        if not AddYoutubeDL.objectName():
            AddYoutubeDL.setObjectName(u"AddYoutubeDL")
        AddYoutubeDL.resize(353, 264)
        self.verticalLayout_2 = QVBoxLayout(AddYoutubeDL)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.leURL = QLineEdit(AddYoutubeDL)
        self.leURL.setObjectName(u"leURL")

        self.verticalLayout.addWidget(self.leURL)

        self.leName = QLineEdit(AddYoutubeDL)
        self.leName.setObjectName(u"leName")

        self.verticalLayout.addWidget(self.leName)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lKeys = QLabel(AddYoutubeDL)
        self.lKeys.setObjectName(u"lKeys")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lKeys.sizePolicy().hasHeightForWidth())
        self.lKeys.setSizePolicy(sizePolicy)
        self.lKeys.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.lKeys)

        self.buttonPlaceholder = QVBoxLayout()
        self.buttonPlaceholder.setObjectName(u"buttonPlaceholder")

        self.horizontalLayout_2.addLayout(self.buttonPlaceholder)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.lStatus = QLabel(AddYoutubeDL)
        self.lStatus.setObjectName(u"lStatus")

        self.verticalLayout.addWidget(self.lStatus)

        self.progressBar = QProgressBar(AddYoutubeDL)
        self.progressBar.setObjectName(u"progressBar")
        self.progressBar.setValue(0)

        self.verticalLayout.addWidget(self.progressBar)

        self.leYTDLargs = QLineEdit(AddYoutubeDL)
        self.leYTDLargs.setObjectName(u"leYTDLargs")

        self.verticalLayout.addWidget(self.leYTDLargs)

        self.leFFMPEGargs = QLineEdit(AddYoutubeDL)
        self.leFFMPEGargs.setObjectName(u"leFFMPEGargs")

        self.verticalLayout.addWidget(self.leFFMPEGargs)

        self.verticalSpacer = QSpacerItem(0, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.bSave = QPushButton(AddYoutubeDL)
        self.bSave.setObjectName(u"bSave")

        self.horizontalLayout.addWidget(self.bSave)

        self.bCancel = QPushButton(AddYoutubeDL)
        self.bCancel.setObjectName(u"bCancel")

        self.horizontalLayout.addWidget(self.bCancel)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(AddYoutubeDL)

        self.bSave.setDefault(True)


        QMetaObject.connectSlotsByName(AddYoutubeDL)
    # setupUi

    def retranslateUi(self, AddYoutubeDL):
        AddYoutubeDL.setWindowTitle(QCoreApplication.translate("AddYoutubeDL", u"Add from Youtube-dl", None))
#if QT_CONFIG(tooltip)
        self.leURL.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.leURL.setPlaceholderText(QCoreApplication.translate("AddYoutubeDL", u"Media URL", None))
        self.leName.setPlaceholderText(QCoreApplication.translate("AddYoutubeDL", u"Custom name", None))
        self.lKeys.setText(QCoreApplication.translate("AddYoutubeDL", u"Key combination", None))
        self.lStatus.setText(QCoreApplication.translate("AddYoutubeDL", u"Standing by...", None))
        self.leYTDLargs.setPlaceholderText(QCoreApplication.translate("AddYoutubeDL", u"Custom YTDL arguments (except -o)", None))
        self.leFFMPEGargs.setPlaceholderText(QCoreApplication.translate("AddYoutubeDL", u"Custom FFMPEG arguments (except output format)", None))
        self.bSave.setText(QCoreApplication.translate("AddYoutubeDL", u"Save", None))
        self.bCancel.setText(QCoreApplication.translate("AddYoutubeDL", u"Cancel", None))
    # retranslateUi

