# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AddTTSDialog.ui'
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

class Ui_AddFromTTS(object):
    def setupUi(self, AddFromTTS):
        if not AddFromTTS.objectName():
            AddFromTTS.setObjectName(u"AddFromTTS")
        AddFromTTS.resize(360, 129)
        self.verticalLayout = QVBoxLayout(AddFromTTS)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.leName = QLineEdit(AddFromTTS)
        self.leName.setObjectName(u"leName")

        self.verticalLayout.addWidget(self.leName)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.lKeys = QLabel(AddFromTTS)
        self.lKeys.setObjectName(u"lKeys")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
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

        self.verticalSpacer = QSpacerItem(20, 11, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setSizeConstraint(QLayout.SetMinimumSize)
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.bSave = QPushButton(AddFromTTS)
        self.bSave.setObjectName(u"bSave")

        self.horizontalLayout.addWidget(self.bSave)

        self.bCancel = QPushButton(AddFromTTS)
        self.bCancel.setObjectName(u"bCancel")

        self.horizontalLayout.addWidget(self.bCancel)


        self.verticalLayout.addLayout(self.horizontalLayout)


        self.retranslateUi(AddFromTTS)

        self.bSave.setDefault(True)


        QMetaObject.connectSlotsByName(AddFromTTS)
    # setupUi

    def retranslateUi(self, AddFromTTS):
        AddFromTTS.setWindowTitle(QCoreApplication.translate("AddFromTTS", u"Add from TTS", None))
#if QT_CONFIG(tooltip)
        self.leName.setToolTip("")
#endif // QT_CONFIG(tooltip)
        self.leName.setPlaceholderText(QCoreApplication.translate("AddFromTTS", u"Custom name", None))
        self.lKeys.setText(QCoreApplication.translate("AddFromTTS", u"Key combination", None))
        self.bSave.setText(QCoreApplication.translate("AddFromTTS", u"Save", None))
        self.bCancel.setText(QCoreApplication.translate("AddFromTTS", u"Cancel", None))
    # retranslateUi

