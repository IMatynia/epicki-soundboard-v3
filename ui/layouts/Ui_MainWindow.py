# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(636, 529)
        font = QFont()
        font.setFamily(u"Ubuntu")
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName(u"actionSave")
        self.actionReload = QAction(MainWindow)
        self.actionReload.setObjectName(u"actionReload")
        self.actionEdit_settings = QAction(MainWindow)
        self.actionEdit_settings.setObjectName(u"actionEdit_settings")
        self.actionOpen_settings_directory = QAction(MainWindow)
        self.actionOpen_settings_directory.setObjectName(u"actionOpen_settings_directory")
        self.actionOpen_tts_manager = QAction(MainWindow)
        self.actionOpen_tts_manager.setObjectName(u"actionOpen_tts_manager")
        self.actionPlay_current_file = QAction(MainWindow)
        self.actionPlay_current_file.setObjectName(u"actionPlay_current_file")
        self.action_Move_to_page = QAction(MainWindow)
        self.action_Move_to_page.setObjectName(u"action_Move_to_page")
        self.actionRemove_with_missing_files = QAction(MainWindow)
        self.actionRemove_with_missing_files.setObjectName(u"actionRemove_with_missing_files")
        self.actionPurge_unused_files_in_customs_folder = QAction(MainWindow)
        self.actionPurge_unused_files_in_customs_folder.setObjectName(u"actionPurge_unused_files_in_customs_folder")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.tvHotkeys = QTableWidget(self.centralwidget)
        if (self.tvHotkeys.columnCount() < 2):
            self.tvHotkeys.setColumnCount(2)
        __qtablewidgetitem = QTableWidgetItem()
        self.tvHotkeys.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tvHotkeys.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        self.tvHotkeys.setObjectName(u"tvHotkeys")
        self.tvHotkeys.setFont(font)
        self.tvHotkeys.setAcceptDrops(True)
        self.tvHotkeys.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tvHotkeys.setAlternatingRowColors(True)
        self.tvHotkeys.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tvHotkeys.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tvHotkeys.setSortingEnabled(True)
        self.tvHotkeys.horizontalHeader().setCascadingSectionResizes(True)
        self.tvHotkeys.horizontalHeader().setHighlightSections(False)
        self.tvHotkeys.horizontalHeader().setStretchLastSection(True)
        self.tvHotkeys.verticalHeader().setVisible(False)
        self.tvHotkeys.verticalHeader().setCascadingSectionResizes(False)
        self.tvHotkeys.verticalHeader().setMinimumSectionSize(20)
        self.tvHotkeys.verticalHeader().setDefaultSectionSize(22)
        self.tvHotkeys.verticalHeader().setHighlightSections(False)
        self.tvHotkeys.verticalHeader().setProperty("showSortIndicator", False)
        self.tvHotkeys.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.tvHotkeys)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cbSource = QComboBox(self.centralwidget)
        self.cbSource.addItem("")
        self.cbSource.addItem("")
        self.cbSource.addItem("")
        self.cbSource.addItem("")
        self.cbSource.setObjectName(u"cbSource")
        sizePolicy = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbSource.sizePolicy().hasHeightForWidth())
        self.cbSource.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.cbSource)

        self.bEdit = QPushButton(self.centralwidget)
        self.bEdit.setObjectName(u"bEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.bEdit.sizePolicy().hasHeightForWidth())
        self.bEdit.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.bEdit)

        self.bRemove = QPushButton(self.centralwidget)
        self.bRemove.setObjectName(u"bRemove")
        sizePolicy1.setHeightForWidth(self.bRemove.sizePolicy().hasHeightForWidth())
        self.bRemove.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.bRemove)

        self.bPlay = QPushButton(self.centralwidget)
        self.bPlay.setObjectName(u"bPlay")
        sizePolicy1.setHeightForWidth(self.bPlay.sizePolicy().hasHeightForWidth())
        self.bPlay.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.bPlay)

        self.bStop = QPushButton(self.centralwidget)
        self.bStop.setObjectName(u"bStop")
        sizePolicy1.setHeightForWidth(self.bStop.sizePolicy().hasHeightForWidth())
        self.bStop.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.bStop)

        self.bPrevPage = QPushButton(self.centralwidget)
        self.bPrevPage.setObjectName(u"bPrevPage")
        sizePolicy1.setHeightForWidth(self.bPrevPage.sizePolicy().hasHeightForWidth())
        self.bPrevPage.setSizePolicy(sizePolicy1)
        self.bPrevPage.setMinimumSize(QSize(30, 0))
        self.bPrevPage.setMaximumSize(QSize(30, 16777215))
        self.bPrevPage.setBaseSize(QSize(0, 0))

        self.horizontalLayout.addWidget(self.bPrevPage)

        self.lbPage = QLabel(self.centralwidget)
        self.lbPage.setObjectName(u"lbPage")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.lbPage.sizePolicy().hasHeightForWidth())
        self.lbPage.setSizePolicy(sizePolicy2)
        self.lbPage.setMinimumSize(QSize(30, 0))
        self.lbPage.setAlignment(Qt.AlignCenter)

        self.horizontalLayout.addWidget(self.lbPage)

        self.bNextPage = QPushButton(self.centralwidget)
        self.bNextPage.setObjectName(u"bNextPage")
        sizePolicy1.setHeightForWidth(self.bNextPage.sizePolicy().hasHeightForWidth())
        self.bNextPage.setSizePolicy(sizePolicy1)
        self.bNextPage.setMinimumSize(QSize(30, 0))
        self.bNextPage.setMaximumSize(QSize(30, 16777215))

        self.horizontalLayout.addWidget(self.bNextPage)


        self.verticalLayout.addLayout(self.horizontalLayout)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 636, 24))
        self.menuData = QMenu(self.menubar)
        self.menuData.setObjectName(u"menuData")
        self.menuText_to_speech = QMenu(self.menubar)
        self.menuText_to_speech.setObjectName(u"menuText_to_speech")
        self.menuMisc = QMenu(self.menubar)
        self.menuMisc.setObjectName(u"menuMisc")
        self.menuINFO = QMenu(self.menubar)
        self.menuINFO.setObjectName(u"menuINFO")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuData.menuAction())
        self.menubar.addAction(self.menuText_to_speech.menuAction())
        self.menubar.addAction(self.menuMisc.menuAction())
        self.menubar.addAction(self.menuINFO.menuAction())
        self.menuData.addAction(self.actionSave)
        self.menuData.addAction(self.actionReload)
        self.menuData.addSeparator()
        self.menuData.addAction(self.actionEdit_settings)
        self.menuText_to_speech.addAction(self.actionOpen_tts_manager)
        self.menuText_to_speech.addAction(self.actionPlay_current_file)
        self.menuMisc.addAction(self.action_Move_to_page)
        self.menuMisc.addAction(self.actionRemove_with_missing_files)
        self.menuMisc.addAction(self.actionPurge_unused_files_in_customs_folder)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Epicki Soundboard V3", None))
        self.actionSave.setText(QCoreApplication.translate("MainWindow", u"&Save settings", None))
        self.actionReload.setText(QCoreApplication.translate("MainWindow", u"&Reload settings", None))
        self.actionEdit_settings.setText(QCoreApplication.translate("MainWindow", u"&Edit settings", None))
        self.actionOpen_settings_directory.setText(QCoreApplication.translate("MainWindow", u"&Open settings directory", None))
        self.actionOpen_tts_manager.setText(QCoreApplication.translate("MainWindow", u"&Open tts manager", None))
        self.actionPlay_current_file.setText(QCoreApplication.translate("MainWindow", u"&Play current file", None))
        self.action_Move_to_page.setText(QCoreApplication.translate("MainWindow", u"&Move to page", None))
        self.actionRemove_with_missing_files.setText(QCoreApplication.translate("MainWindow", u"&Remove with missing files", None))
        self.actionPurge_unused_files_in_customs_folder.setText(QCoreApplication.translate("MainWindow", u"&Purge unused files in customs folder", None))
        ___qtablewidgetitem = self.tvHotkeys.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Hotkey", None));
        ___qtablewidgetitem1 = self.tvHotkeys.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"File", None));
        self.cbSource.setItemText(0, QCoreApplication.translate("MainWindow", u"Add from...", None))
        self.cbSource.setItemText(1, QCoreApplication.translate("MainWindow", u"Audio file", None))
        self.cbSource.setItemText(2, QCoreApplication.translate("MainWindow", u"Youtube-dl", None))
        self.cbSource.setItemText(3, QCoreApplication.translate("MainWindow", u"Current TTS", None))

        self.cbSource.setCurrentText(QCoreApplication.translate("MainWindow", u"Add from...", None))
        self.bEdit.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.bRemove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.bPlay.setText(QCoreApplication.translate("MainWindow", u"Play", None))
        self.bStop.setText(QCoreApplication.translate("MainWindow", u"Stop all", None))
        self.bPrevPage.setText(QCoreApplication.translate("MainWindow", u"<<", None))
        self.lbPage.setText(QCoreApplication.translate("MainWindow", u"1", None))
        self.bNextPage.setText(QCoreApplication.translate("MainWindow", u">>", None))
        self.menuData.setTitle(QCoreApplication.translate("MainWindow", u"&Data", None))
        self.menuText_to_speech.setTitle(QCoreApplication.translate("MainWindow", u"&Text-to-speech", None))
        self.menuMisc.setTitle(QCoreApplication.translate("MainWindow", u"&Misc", None))
        self.menuINFO.setTitle(QCoreApplication.translate("MainWindow", u"INFO", None))
    # retranslateUi

