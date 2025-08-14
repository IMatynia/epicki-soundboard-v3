# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'YoutubeDialog.ui'
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
from PySide6.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QPushButton, QSizePolicy,
    QSpacerItem, QVBoxLayout, QWidget)

class Ui_AddYoutubeDL(object):
    def setupUi(self, AddYoutubeDL):
        if not AddYoutubeDL.objectName():
            AddYoutubeDL.setObjectName(u"AddYoutubeDL")
        AddYoutubeDL.resize(398, 214)
        self.verticalLayout_2 = QVBoxLayout(AddYoutubeDL)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(AddYoutubeDL)
        self.label.setObjectName(u"label")
        self.label.setScaledContents(False)
        self.label.setWordWrap(True)

        self.verticalLayout.addWidget(self.label)

        self.verticalSpacer = QSpacerItem(0, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

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
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lKeys.sizePolicy().hasHeightForWidth())
        self.lKeys.setSizePolicy(sizePolicy)
        self.lKeys.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_2.addWidget(self.lKeys)

        self.buttonPlaceholder = QVBoxLayout()
        self.buttonPlaceholder.setObjectName(u"buttonPlaceholder")

        self.horizontalLayout_2.addLayout(self.buttonPlaceholder)


        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.lStatus = QLabel(AddYoutubeDL)
        self.lStatus.setObjectName(u"lStatus")

        self.verticalLayout.addWidget(self.lStatus)


        self.verticalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SizeConstraint.SetMinimumSize)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.bActionButton = QPushButton(AddYoutubeDL)
        self.bActionButton.setObjectName(u"bActionButton")

        self.horizontalLayout.addWidget(self.bActionButton)

        self.bCancel = QPushButton(AddYoutubeDL)
        self.bCancel.setObjectName(u"bCancel")

        self.horizontalLayout.addWidget(self.bCancel)


        self.verticalLayout_2.addLayout(self.horizontalLayout)


        self.retranslateUi(AddYoutubeDL)

        QMetaObject.connectSlotsByName(AddYoutubeDL)
    # setupUi

    def retranslateUi(self, AddYoutubeDL):
        AddYoutubeDL.setWindowTitle(QCoreApplication.translate("AddYoutubeDL", u"Add from Youtube-dl", None))
        self.label.setText(QCoreApplication.translate("AddYoutubeDL", u"Download media via youtube-dl or its forks. The default behaviour tries to download the media as audio only in the prefered file format. Parameters can be configured via the config file.", None))
#if QT_CONFIG(tooltip)
        self.leURL.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.leURL.setPlaceholderText(QCoreApplication.translate("AddYoutubeDL", u"Media URL", None))
        self.leName.setPlaceholderText(QCoreApplication.translate("AddYoutubeDL", u"Custom name", None))
        self.lKeys.setText(QCoreApplication.translate("AddYoutubeDL", u"Key combination", None))
        self.lStatus.setText(QCoreApplication.translate("AddYoutubeDL", u"Standing by...", None))
        self.bActionButton.setText(QCoreApplication.translate("AddYoutubeDL", u"Download", None))
        self.bCancel.setText(QCoreApplication.translate("AddYoutubeDL", u"Cancel", None))
    # retranslateUi

