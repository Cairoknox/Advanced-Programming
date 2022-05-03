# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main_pagesPCtOwL.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from qt_core import *

class Ui_MainPages(object):
    def setupUi(self, MainPages):
        if not MainPages.objectName():
            MainPages.setObjectName(u"MainPages")
        MainPages.resize(833, 611)
        self.main_pages_layout = QVBoxLayout(MainPages)
        self.main_pages_layout.setSpacing(0)
        self.main_pages_layout.setObjectName(u"main_pages_layout")
        self.main_pages_layout.setContentsMargins(5, 5, 5, 5)
        self.pages = QStackedWidget(MainPages)
        self.pages.setObjectName(u"pages")
        self.pages.setStyleSheet(u"font-size: 14pt;background: lightblue;")
        self.page_1 = QWidget()
        self.page_1.setObjectName(u"page_1")
        font = QFont()
        font.setFamily(u"MS Shell Dlg 2")
        font.setPointSize(14)
        self.page_1.setFont(font)
        self.page_1.setStyleSheet(u"")
        self.page_1_layout = QVBoxLayout(self.page_1)
        self.page_1_layout.setSpacing(5)
        self.page_1_layout.setObjectName(u"page_1_layout")
        self.page_1_layout.setContentsMargins(5, 5, 5, 5)
        self.main_frame = QFrame(self.page_1)
        self.main_frame.setObjectName(u"main_frame")
        self.main_frame.setFont(font)
        self.main_frame.setStyleSheet(u"font-size: 14pt;background: white;")
        self.main_frame.setFrameShape(QFrame.NoFrame)
        self.main_frame.setFrameShadow(QFrame.Raised)
        self.verticalLayout = QVBoxLayout(self.main_frame)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.logo_frame = QFrame(self.main_frame)
        self.logo_frame.setObjectName(u"logo_frame")
        self.logo_frame.setFrameShape(QFrame.NoFrame)
        self.logo_frame.setFrameShadow(QFrame.Raised)
        self.logo_layout = QVBoxLayout(self.logo_frame)
        self.logo_layout.setSpacing(0)
        self.logo_layout.setObjectName(u"logo_layout")
        self.logo_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.logo_frame)

        self.welcome_message = QLabel(self.main_frame)
        self.welcome_message.setObjectName(u"welcome_message")
        font1 = QFont()
        font1.setFamily(u"MS Shell Dlg 2")
        font1.setPointSize(14)
        font1.setBold(False)
        self.welcome_message.setFont(font1)
        self.welcome_message.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.welcome_message)

        self.welcome_message_2 = QLabel(self.main_frame)
        self.welcome_message_2.setObjectName(u"welcome_message_2")
        self.welcome_message_2.setEnabled(True)
        self.welcome_message_2.setFont(font1)
        self.welcome_message_2.setAlignment(Qt.AlignCenter)

        self.verticalLayout.addWidget(self.welcome_message_2)

        self.API_frame = QFrame(self.main_frame)
        self.API_frame.setObjectName(u"API_frame")
        self.API_frame.setMinimumSize(QSize(0, 40))
        self.API_frame.setFont(font)
        self.API_frame.setFrameShape(QFrame.NoFrame)
        self.API_frame.setFrameShadow(QFrame.Raised)
        self.API_layout = QHBoxLayout(self.API_frame)
        self.API_layout.setSpacing(0)
        self.API_layout.setObjectName(u"API_layout")
        self.API_layout.setContentsMargins(0, 0, 6, 0)
        self.API_key_frame = QFrame(self.API_frame)
        self.API_key_frame.setObjectName(u"API_key_frame")
        self.API_key_frame.setFrameShape(QFrame.NoFrame)
        self.API_key_frame.setFrameShadow(QFrame.Raised)
        self.API_key_layout = QVBoxLayout(self.API_key_frame)
        self.API_key_layout.setSpacing(0)
        self.API_key_layout.setObjectName(u"API_key_layout")
        self.API_key_layout.setContentsMargins(0, 0, 0, 0)

        self.API_layout.addWidget(self.API_key_frame)

        self.API_valid_frame = QFrame(self.API_frame)
        self.API_valid_frame.setObjectName(u"API_valid_frame")
        self.API_valid_frame.setFrameShape(QFrame.NoFrame)
        self.API_valid_frame.setFrameShadow(QFrame.Raised)
        self.API_valid_layout = QVBoxLayout(self.API_valid_frame)
        self.API_valid_layout.setSpacing(0)
        self.API_valid_layout.setObjectName(u"API_valid_layout")
        self.API_valid_layout.setContentsMargins(0, 0, 0, 0)

        self.API_layout.addWidget(self.API_valid_frame)


        self.verticalLayout.addWidget(self.API_frame)

        self.send_frame = QFrame(self.main_frame)
        self.send_frame.setObjectName(u"send_frame")
        self.send_frame.setMinimumSize(QSize(0, 20))
        self.send_frame.setFrameShape(QFrame.NoFrame)
        self.send_frame.setFrameShadow(QFrame.Raised)
        self.send_layout = QVBoxLayout(self.send_frame)
        self.send_layout.setSpacing(0)
        self.send_layout.setObjectName(u"send_layout")
        self.send_layout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.addWidget(self.send_frame)


        self.page_1_layout.addWidget(self.main_frame)

        self.pages.addWidget(self.page_1)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.page_2.setStyleSheet(u"font-size: 14pt;background: orange;")
        self.page_2_layout = QVBoxLayout(self.page_2)
        self.page_2_layout.setSpacing(5)
        self.page_2_layout.setObjectName(u"page_2_layout")
        self.page_2_layout.setContentsMargins(5, 5, 5, 5)
        self.pages.addWidget(self.page_2)
        self.page_3 = QWidget()
        self.page_3.setObjectName(u"page_3")
        self.page_3.setStyleSheet(u"QFrame {\n"
"	font-size: 16pt;\n"
"}")
        self.page_3_layout = QVBoxLayout(self.page_3)
        self.page_3_layout.setObjectName(u"page_3_layout")
        self.pages.addWidget(self.page_3)

        self.main_pages_layout.addWidget(self.pages)


        self.retranslateUi(MainPages)

        self.pages.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainPages)
    # setupUi

    def retranslateUi(self, MainPages):
        MainPages.setWindowTitle(QCoreApplication.translate("MainPages", u"Form", None))
        self.welcome_message.setText(QCoreApplication.translate("MainPages", u"Welcome to the Radzuptimizer", None))
        self.welcome_message_2.setText(QCoreApplication.translate("MainPages", u"Enter your AlphaVantage API key...", None))
    # retranslateUi

