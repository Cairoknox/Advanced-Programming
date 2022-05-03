from gui.widgets.py_table_widget.py_table_widget import PyTableWidget
from . functions_main_window import *
import sys
import os
from qt_core import *
from gui.core.json_settings import Settings
from gui.core.json_themes import Themes
from gui.widgets import *

from . ui_main import *
from . functions_main_window import *

#What should the main window contain.
class SetupMainWindow:
    def __init__(self):
        super().__init__()
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)
    
    #Left menu buttons
    add_left_menus = [
        {"btn_icon" : "icon_home.svg", "btn_id" : "btn_home", "btn_text" : "Home", "btn_tooltip" : "Home page", "show_top" : True, "is_active" : True},
        {"btn_icon" : "icon_file.svg", "btn_id" : "btn_market", "btn_text" : "Market data", "btn_tooltip" : "Market data", "show_top" : True, "is_active" : False},
        {"btn_icon" : "icon_file.svg", "btn_id" : "btn_portfolio", "btn_text" : "Portfolio", "btn_tooltip" : "Portfolio", "show_top" : True, "is_active" : False},
        {"btn_icon" : "icon_info.svg", "btn_id" : "btn_about", "btn_text" : "About", "btn_tooltip" : "About", "show_top" : False, "is_active" : False},
        {"btn_icon" : "icon_settings.svg", "btn_id" : "btn_settings", "btn_text" : "Settings", "btn_tooltip" : "Settings", "show_top" : False, "is_active" : False}
    ]
    #Title bar menu buttons
    add_title_bar_menus = [
        {"btn_icon" : "icon_search.svg", "btn_id" : "btn_search", "btn_tooltip" : "Search", "is_active" : False},
        {"btn_icon" : "icon_settings.svg", "btn_id" : "btn_top_settings", "btn_tooltip" : "Top settings", "is_active" : False}
    ]

    #This gets called on button click, returns the action that the button is designed for
    def setup_btns(self):
        if self.ui.title_bar.sender() != None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() != None:
            return self.ui.left_menu.sender()
        elif self.ui.left_column.sender() != None:
            return self.ui.left_column.sender()
    
    #Customized settings of the GUI
    def setup_gui(self):
        self.setWindowTitle(self.settings["app_name"])
        #For a more modern look, we remove the OS frame
        if self.settings["custom_title_bar"]:
            self.setWindowFlag(Qt.FramelessWindowHint)
            self.setAttribute(Qt.WA_TranslucentBackground)
        #We want to be able to move the frame
        if self.settings["custom_title_bar"]:
            self.left_grip = PyGrips(self, "left", self.hide_grips)
            self.right_grip = PyGrips(self, "right", self.hide_grips)
            self.top_grip = PyGrips(self, "top", self.hide_grips)
            self.bottom_grip = PyGrips(self, "bottom", self.hide_grips)
            self.top_left_grip = PyGrips(self, "top_left", self.hide_grips)
            self.top_right_grip = PyGrips(self, "top_right", self.hide_grips)
            self.bottom_left_grip = PyGrips(self, "bottom_left", self.hide_grips)
            self.bottom_right_grip = PyGrips(self, "bottom_right", self.hide_grips)
        #Add the left menu
        self.ui.left_menu.add_menus(SetupMainWindow.add_left_menus)
        #Trigger an event when left menu button is clicked
        self.ui.left_menu.clicked.connect(self.btn_clicked)
        self.ui.left_menu.released.connect(self.btn_released)
        #Add title bar menu
        self.ui.title_bar.add_menus(SetupMainWindow.add_title_bar_menus)
        #Trigger an event when title bar menu button is clicked
        self.ui.title_bar.clicked.connect(self.btn_clicked)
        self.ui.title_bar.released.connect(self.btn_released)
        #Add the custom title bar to the GUI
        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("Welcome to Radzuptimizer")
        #Add the left column menu
        #Trigger an event when left column menu button is clicked
        self.ui.left_column.clicked.connect(self.btn_clicked)
        self.ui.left_column.released.connect(self.btn_released)
        #Page on start of application
        MainFunctions.set_page(self, self.ui.load_pages.page_1)
        #Load settings and themes
        settings = Settings()
        self.settings = settings.items
        themes = Themes()
        self.themes = themes.items
        
        #mainpage: Add logo
        self.logo = QSvgWidget(Functions.set_svg_image("logo_home.svg"))
        self.ui.load_pages.logo_layout.addWidget(self.logo, Qt.AlignCenter, Qt.AlignCenter)
        
        #mainpage: Add API key manager
        self.line_edit = QLineEdit()
        self.button = QPushButton("send", self)
        self.text = QLabel("connected")
        #Save the API key entered by user
        def print_API():
            API_key = self.line_edit.text()
            print(API_key)
            self.ui.load_pages.API_valid_layout.addWidget(self.text)
        #Use the function on button click
        self.button.clicked.connect(print_API)
        #Display both the text field and the send button
        self.ui.load_pages.API_key_layout.addWidget(self.line_edit, Qt.AlignCenter, Qt.AlignCenter)
        self.ui.load_pages.send_layout.addWidget(self.button, Qt.AlignCenter, Qt.AlignCenter)

    #Resize the grips when window is resized
    def resize_grips(self):
        if self.settings["custom_title_bar"]:
            self.left_grip.setGeometry(5, 10, 10, self.height())
            self.right_grip.setGeometry(self.width() - 15, 10, 10, self.height())
            self.top_grip.setGeometry(5, 5, self.width() - 10, 10)
            self.bottom_grip.setGeometry(5, self.height() - 15, self.width() - 10, 10)
            self.top_right_grip.setGeometry(self.width() - 20, 5, 15, 15)
            self.bottom_left_grip.setGeometry(5, self.height() - 20, 15, 15)
            self.bottom_right_grip.setGeometry(self.width() - 20, self.height() - 20, 15, 15)