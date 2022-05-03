# ///////////////////////////////////////////////////////////////
#
# BY: WANDERSON M.PIMENTA
# PROJECT MADE WITH: Qt Designer and PySide6
# V: 1.0.0
#
# This project can be used freely for all uses, as long as they maintain the
# respective credits only in the Python scripts, any information in the visual
# interface (GUI) can be modified without any implication.
#
# There are limitations on Qt licenses if you want to use your products
# commercially, I recommend reading them on the official website:
# https://doc.qt.io/qtforpython/licenses.html
#
# ///////////////////////////////////////////////////////////////

# IMPORT PACKAGES AND MODULES
# ///////////////////////////////////////////////////////////////
from gui.uis.windows.main_window.functions_main_window import *
import sys
import os

# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# IMPORT SETTINGS
# ///////////////////////////////////////////////////////////////
from gui.core.json_settings import Settings

# IMPORT PY ONE DARK WINDOWS
# ///////////////////////////////////////////////////////////////
# MAIN WINDOW
from gui.uis.windows.main_window import *

# IMPORT PY ONE DARK WIDGETS
# ///////////////////////////////////////////////////////////////
from gui.widgets import *

# ADJUST QT FONT DPI FOR HIGHT SCALE AN 4K MONITOR
# ///////////////////////////////////////////////////////////////
os.environ["QT_FONT_DPI"] = "96"
# IF IS 4K MONITOR ENABLE 'os.environ["QT_SCALE_FACTOR"] = "2"'

# MAIN WINDOW
# ///////////////////////////////////////////////////////////////
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # SETUP MAIN WINDOw
        # Load widgets from "gui\uis\main_window\ui_main.py"
        # ///////////////////////////////////////////////////////////////
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)

        # LOAD SETTINGS
        # ///////////////////////////////////////////////////////////////
        settings = Settings()
        self.settings = settings.items

        # SETUP MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.hide_grips = True # Show/Hide resize grips
        SetupMainWindow.setup_gui(self)

        # SHOW MAIN WINDOW
        # ///////////////////////////////////////////////////////////////
        self.show()

    # LEFT MENU BTN IS CLICKED
    # Run function when btn is clicked
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_clicked(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # LEFT MENU
        # ///////////////////////////////////////////////////////////////
        
        # OPEN HOME PAGE
        if btn.objectName() == "btn_home":
            #Select menu
            self.ui.left_menu.select_only_one(btn.objectName())
            #Load page
            MainFunctions.set_page(self, self.ui.load_pages.page_1)
        # OPEN MARKET PAGE
        if btn.objectName() == "btn_market":
            #Select menu
            self.ui.left_menu.select_only_one(btn.objectName())
            #Load page
            MainFunctions.set_page(self, self.ui.load_pages.page_2)
        # OPEN PORTFOLIO PAGE
        if btn.objectName() == "btn_portfolio":
            #Select menu
            self.ui.left_menu.select_only_one(btn.objectName())
            #Load page
            MainFunctions.set_page(self, self.ui.load_pages.page_3)
        
        # GET TOP SETTINGS
        top_btn_settings = MainFunctions.get_title_bar_btn(self, "btn_top_settings")
        # OPEN ABOUT MENU
        if btn.objectName() == "btn_about" or btn.objectName() == "btn_close_left_column":
            #Disable selection on title bar
            top_btn_settings.set_active(False)
            #Check if left column is visible
            if not MainFunctions.left_column_is_visible(self):
                #If not, show it
                MainFunctions.toggle_left_column(self)
                #Select the about menu
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                #If it is, hide it
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    MainFunctions.toggle_left_column(self)
                #If other button is pressed, don't hide it
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(self,
                menu = self.ui.left_column.menus.menu_1,
                title = "About",
                icon_path = Functions.set_svg_icon("icon_info.svg"))
        # OPEN SETTINGS MENU
        if btn.objectName() == "btn_settings" or btn.objectName() == "btn_close_left_column":
            #Disable selection on title bar
            top_btn_settings.set_active(False)
            #Check if left column is visible
            if not MainFunctions.left_column_is_visible(self):
                #If not, show it
                MainFunctions.toggle_left_column(self)
                #Select the settings menu
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            else:
                #If it is, hide it
                if btn.objectName() == "btn_close_left_column":
                    self.ui.left_menu.deselect_all_tab()
                    MainFunctions.toggle_left_column(self)
                #If other button is pressed, don't hide it
                self.ui.left_menu.select_only_one_tab(btn.objectName())
            if btn.objectName() != "btn_close_left_column":
                MainFunctions.set_left_column_menu(self,
                menu = self.ui.left_column.menus.menu_2,
                title = "Settings",
                icon_path = Functions.set_svg_icon("icon_settings.svg"))
        
        
        # TITLE BAR MENU
        # ///////////////////////////////////////////////////////////////
        
        # SETTINGS TITLE BAR
        if btn.objectName() == "btn_top_settings":
            # Toogle Active
            if not MainFunctions.right_column_is_visible(self):
                btn.set_active(True)

                # Show / Hide
                MainFunctions.toggle_right_column(self)
            else:
                btn.set_active(False)

                # Show / Hide
                MainFunctions.toggle_right_column(self)

            # Get settings menu
            btn_settings = MainFunctions.get_left_menu_btn(self, "btn_settings")
            btn_settings.set_active_tab(False)

            # Get about menu
            btn_about = MainFunctions.get_left_menu_btn(self, "btn_about")
            btn_about.set_active_tab(False)

        # DEBUG
        print(f"Button {btn.objectName()}, clicked!")

    # LEFT MENU BTN IS RELEASED
    # Run function when btn is released
    # Check funtion by object name / btn_id
    # ///////////////////////////////////////////////////////////////
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    # RESIZE EVENT
    # ///////////////////////////////////////////////////////////////
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    # MOUSE CLICK EVENTS
    # ///////////////////////////////////////////////////////////////
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()


# SETTINGS WHEN TO START
# Set the initial class and also additional parameters of the "QApplication" class
# ///////////////////////////////////////////////////////////////
if __name__ == "__main__":
    # APPLICATION
    # ///////////////////////////////////////////////////////////////
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()

    # EXEC APP
    # ///////////////////////////////////////////////////////////////
    sys.exit(app.exec_())