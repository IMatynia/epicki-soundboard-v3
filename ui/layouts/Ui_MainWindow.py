# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'MainWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QComboBox, QHBoxLayout,
    QHeaderView, QMainWindow, QMenu, QMenuBar,
    QPushButton, QSizePolicy, QSpinBox, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(636, 529)
        font = QFont()
        font.setFamilies([u"Ubuntu"])
        font.setBold(False)
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
        self.actionYoutube_dl_arguments = QAction(MainWindow)
        self.actionYoutube_dl_arguments.setObjectName(u"actionYoutube_dl_arguments")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayout = QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.cbSource = QComboBox(self.centralwidget)
        self.cbSource.addItem("")
        self.cbSource.addItem("")
        self.cbSource.addItem("")
        self.cbSource.addItem("")
        self.cbSource.setObjectName(u"cbSource")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cbSource.sizePolicy().hasHeightForWidth())
        self.cbSource.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.cbSource)

        self.bEdit = QPushButton(self.centralwidget)
        self.bEdit.setObjectName(u"bEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
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

        self.bStop = QPushButton(self.centralwidget)
        self.bStop.setObjectName(u"bStop")
        sizePolicy1.setHeightForWidth(self.bStop.sizePolicy().hasHeightForWidth())
        self.bStop.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.bStop)

        self.bPlay = QPushButton(self.centralwidget)
        self.bPlay.setObjectName(u"bPlay")
        sizePolicy1.setHeightForWidth(self.bPlay.sizePolicy().hasHeightForWidth())
        self.bPlay.setSizePolicy(sizePolicy1)
        font1 = QFont()
        font1.setFamilies([u"Ubuntu"])
        font1.setPointSize(9)
        font1.setBold(False)
        self.bPlay.setFont(font1)
        self.bPlay.setFlat(False)

        self.horizontalLayout.addWidget(self.bPlay)

        self.lbPage = QSpinBox(self.centralwidget)
        self.lbPage.setObjectName(u"lbPage")
        self.lbPage.setMinimum(1)
        self.lbPage.setMaximum(999)
        self.lbPage.setValue(1)

        self.horizontalLayout.addWidget(self.lbPage)


        self.verticalLayout.addLayout(self.horizontalLayout)

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
        self.tvHotkeys.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.tvHotkeys.setAlternatingRowColors(True)
        self.tvHotkeys.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tvHotkeys.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tvHotkeys.setSortingEnabled(True)
        self.tvHotkeys.horizontalHeader().setCascadingSectionResizes(True)
        self.tvHotkeys.horizontalHeader().setHighlightSections(False)
        self.tvHotkeys.horizontalHeader().setStretchLastSection(True)
        self.tvHotkeys.verticalHeader().setVisible(False)
        self.tvHotkeys.verticalHeader().setCascadingSectionResizes(False)
        self.tvHotkeys.verticalHeader().setMinimumSectionSize(20)
        self.tvHotkeys.verticalHeader().setDefaultSectionSize(22)
        self.tvHotkeys.verticalHeader().setHighlightSections(False)
        self.tvHotkeys.verticalHeader().setProperty(u"showSortIndicator", False)
        self.tvHotkeys.verticalHeader().setStretchLastSection(False)

        self.verticalLayout.addWidget(self.tvHotkeys)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 636, 33))
        self.menuData = QMenu(self.menubar)
        self.menuData.setObjectName(u"menuData")
        self.menuText_to_speech = QMenu(self.menubar)
        self.menuText_to_speech.setObjectName(u"menuText_to_speech")
        self.menuMisc = QMenu(self.menubar)
        self.menuMisc.setObjectName(u"menuMisc")
        self.menuINFO = QMenu(self.menubar)
        self.menuINFO.setObjectName(u"menuINFO")
        MainWindow.setMenuBar(self.menubar)

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
        self.actionYoutube_dl_arguments.setText(QCoreApplication.translate("MainWindow", u"&Custom FFMPEG arguments", None))
        self.cbSource.setItemText(0, QCoreApplication.translate("MainWindow", u"Add from...", None))
        self.cbSource.setItemText(1, QCoreApplication.translate("MainWindow", u"Audio file", None))
        self.cbSource.setItemText(2, QCoreApplication.translate("MainWindow", u"Youtube-dl", None))
        self.cbSource.setItemText(3, QCoreApplication.translate("MainWindow", u"Current TTS", None))

        self.cbSource.setCurrentText(QCoreApplication.translate("MainWindow", u"Add from...", None))
        self.bEdit.setText(QCoreApplication.translate("MainWindow", u"Edit", None))
        self.bRemove.setText(QCoreApplication.translate("MainWindow", u"Remove", None))
        self.bStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
#if QT_CONFIG(tooltip)
        self.bPlay.setToolTip(QCoreApplication.translate("MainWindow", u"Play selected", None))
#endif // QT_CONFIG(tooltip)
        self.bPlay.setText(QCoreApplication.translate("MainWindow", u"Play", None))
#if QT_CONFIG(tooltip)
        self.lbPage.setToolTip(QCoreApplication.translate("MainWindow", u"Page number", None))
#endif // QT_CONFIG(tooltip)
        ___qtablewidgetitem = self.tvHotkeys.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"Hotkey", None));
        ___qtablewidgetitem1 = self.tvHotkeys.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"File", None));
        self.menuData.setTitle(QCoreApplication.translate("MainWindow", u"&Data", None))
        self.menuText_to_speech.setTitle(QCoreApplication.translate("MainWindow", u"&Text-to-speech", None))
        self.menuMisc.setTitle(QCoreApplication.translate("MainWindow", u"&Misc", None))
        self.menuINFO.setTitle(QCoreApplication.translate("MainWindow", u"INFO", None))
    # retranslateUi

