# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_pages.ui'
##
## Created by: Qt User Interface Compiler version 6.3.0
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
from PySide6.QtWidgets import (QApplication, QFrame, QGridLayout, QHBoxLayout,
    QLabel, QSizePolicy, QStackedWidget, QVBoxLayout,
    QWidget)

class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(1078, 827)
        font = QFont()
        font.setPointSize(14)
        font.setUnderline(False)
        font.setKerning(False)
        MainPages.setFont(font)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(0, 0, 0, 0)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.pages.setStyleSheet(u"font-size: 14pt;background: rgb(60, 68, 84);")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        font1 = QFont()
        font1.setFamilies([u"MS Shell Dlg 2"])
        font1.setPointSize(14)
        self.page_1.setFont(font1)
        self.page_1.setStyleSheet(u"")
        self.page_1_layout = QVBoxLayout(self.page_1)
        self.page_1_layout.setSpacing(0)
        self.page_1_layout.setObjectName(u"page_1_layout")
        self.page_1_layout.setContentsMargins(0, 0, 0, 0)
        self.main_frame = QFrame(self.page_1)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setFont(font1)
        self.main_frame.setStyleSheet(u"font-size: 14pt;background: transparent;")
        self.main_frame.setFrameShape(QFrame.NoFrame)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.gridLayout = QGridLayout(self.main_frame)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.logo_frame = QFrame(self.main_frame)
        self.logo_frame.setObjectName(u"logo_frame")
        self.logo_frame.setMaximumSize(QSize(300, 240))
        self.logo_frame.setFrameShape(QFrame.NoFrame)
        self.logo_frame.setFrameShadow(QFrame.Raised)
        self.logo_layout = QVBoxLayout(self.logo_frame)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setObjectName(u"logo_layout")
        self.logo_layout.setContentsMargins(0, 0, 0, 0)
        self.welcome_message = QLabel(self.logo_frame)
        self.welcome_message.setObjectName(u"welcome_message")
        self.welcome_message.setMaximumSize(QSize(16777215, 40))
        font2 = QFont()
        font2.setFamilies([u"MS Shell Dlg 2"])
        font2.setPointSize(16)
        self.welcome_message.setFont(font2)
        self.welcome_message.setStyleSheet(u"font-size: 16pt")
        self.welcome_message.setAlignment(Qt.AlignCenter)

        self.logo_layout.addWidget(self.welcome_message)


        self.gridLayout.addWidget(self.logo_frame, 1, 1, 1, 1)

        self.API_frame = QFrame(self.main_frame)
        self.API_frame.setObjectName(u"API_frame")
        self.API_frame.setMinimumSize(QSize(0, 40))
        self.API_frame.setFont(font1)
        self.API_frame.setFrameShape(QFrame.NoFrame)
        self.API_frame.setFrameShadow(QFrame.Raised)
        self.API_layout = QHBoxLayout(self.API_frame)
        self.API_layout.setSpacing(0)
        self.API_layout.setObjectName(u"API_layout")
        self.API_layout.setContentsMargins(0, 0, 0, 0)
        self.API_key_frame = QFrame(self.API_frame)
        self.API_key_frame.setObjectName(u"API_key_frame")
        self.API_key_frame.setMinimumSize(QSize(0, 20))
        self.API_key_frame.setMaximumSize(QSize(400, 120))
        self.API_key_frame.setFrameShape(QFrame.NoFrame)
        self.API_key_frame.setFrameShadow(QFrame.Raised)
        self.API_key_layout = QHBoxLayout(self.API_key_frame)
        self.API_key_layout.setSpacing(0)
        self.API_key_layout.setObjectName(u"API_key_layout")
        self.API_key_layout.setContentsMargins(0, 0, 0, 0)

        self.API_layout.addWidget(self.API_key_frame)


        self.gridLayout.addWidget(self.API_frame, 4, 0, 1, 3)

        self.frame = QFrame(self.main_frame)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.NoFrame)
        self.frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.frame)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.welcome_message_2 = QLabel(self.frame)
        self.welcome_message_2.setObjectName(u"welcome_message_2")
        self.welcome_message_2.setEnabled(True)
        self.welcome_message_2.setFont(font1)
        self.welcome_message_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.welcome_message_2)


        self.gridLayout.addWidget(self.frame, 2, 0, 1, 3)


        self.page_1_layout.addWidget(self.main_frame)

        self.pages.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setStyleSheet(u"")
        self.page_2_layout = QVBoxLayout(self.page_2)
        self.page_2_layout.setSpacing(0)
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_layout.setContentsMargins(0, 0, 0, 0)
        self.main_frame_2 = QFrame(self.page_2)
        self.main_frame_2.setObjectName(u"main_frame_2")
        self.main_frame_2.setStyleSheet(u"font-size: 14pt;background: transparent;")
        self.main_frame_2.setFrameShape(QFrame.NoFrame)
        self.main_frame_2.setFrameShadow(QFrame.Raised)
        self.gridLayout_2 = QGridLayout(self.main_frame_2)
        self.gridLayout_2.setSpacing(0)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.plot_frame = QFrame(self.main_frame_2)
        self.plot_frame.setObjectName(u"plot_frame")
        self.plot_frame.setMinimumSize(QSize(400, 200))
        self.plot_frame.setFrameShape(QFrame.NoFrame)
        self.plot_frame.setFrameShadow(QFrame.Raised)
        self.plot_layout = QVBoxLayout(self.plot_frame)
        self.plot_layout.setSpacing(0)
        self.plot_layout.setObjectName(u"plot_layout")
        self.plot_layout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_2.addWidget(self.plot_frame, 2, 1, 1, 1)

        self.ask_frame = QFrame(self.main_frame_2)
        self.ask_frame.setObjectName(u"ask_frame")
        self.ask_frame.setMinimumSize(QSize(300, 120))
        self.ask_frame.setMaximumSize(QSize(450, 240))
        self.ask_frame.setFrameShape(QFrame.NoFrame)
        self.ask_frame.setFrameShadow(QFrame.Raised)
        self.ask_layout = QHBoxLayout(self.ask_frame)
        self.ask_layout.setSpacing(0)
        self.ask_layout.setObjectName(u"ask_layout")
        self.ask_layout.setContentsMargins(0, 0, 0, 0)

        self.gridLayout_2.addWidget(self.ask_frame, 3, 1, 1, 1, Qt.AlignHCenter|Qt.AlignVCenter)


        self.page_2_layout.addWidget(self.main_frame_2)

        self.pages.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setStyleSheet(u"")
        self.page_3_layout = QVBoxLayout(self.page_3)
        self.page_3_layout.setSpacing(0)
        self.page_3_layout.setObjectName(u"page_3_layout")
        self.page_3_layout.setContentsMargins(0, 0, 0, 0)
        self.main_frame_3 = QFrame(self.page_3)
        self.main_frame_3.setObjectName(u"main_frame_3")
        self.main_frame_3.setStyleSheet(u"font-size: 14pt;background: transparent;")
        self.main_frame_3.setFrameShape(QFrame.NoFrame)
        self.main_frame_3.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.main_frame_3)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 0)
        self.markowitz_frame = QFrame(self.main_frame_3)
        self.markowitz_frame.setObjectName(u"markowitz_frame")
        self.markowitz_frame.setFrameShape(QFrame.NoFrame)
        self.markowitz_frame.setFrameShadow(QFrame.Raised)
        self.markowitz_layout = QVBoxLayout(self.markowitz_frame)
        self.markowitz_layout.setSpacing(0)
        self.markowitz_layout.setObjectName(u"markowitz_layout")
        self.markowitz_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.markowitz_frame)

        self.constroptimize_frame = QFrame(self.main_frame_3)
        self.constroptimize_frame.setObjectName(u"constroptimize_frame")
        self.constroptimize_frame.setMaximumSize(QSize(300, 240))
        self.constroptimize_frame.setFrameShape(QFrame.NoFrame)
        self.constroptimize_frame.setFrameShadow(QFrame.Raised)
        self.constroptimize_layout = QHBoxLayout(self.constroptimize_frame)
        self.constroptimize_layout.setSpacing(0)
        self.constroptimize_layout.setObjectName(u"constroptimize_layout")
        self.constroptimize_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout_2.addWidget(self.constroptimize_frame, 0, Qt.AlignHCenter|Qt.AlignVCenter)


        self.page_3_layout.addWidget(self.main_frame_3)

        self.pages.addWidget(self.page_3)

        self.main_pages_layout.addWidget(self.pages)


        self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(2)


        QMetaObject.connectSlotsByName(MainPages)
    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        self.welcome_message.setText(QCoreApplication.translate("MainPages", u"Welcome to the Radzuptimizer", None))
        self.welcome_message_2.setText(QCoreApplication.translate("MainPages", u"Enter your AlphaVantage API key...", None))
    # retranslateUi

