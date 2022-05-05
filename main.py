import sys
import os

from qt_core import *

from gui.uis.windows.main_window.functions_main_window import *

from gui.core.json_settings import Settings

from gui.uis.windows.main_window import *

from gui.widgets import *

from portfolio import *

os.environ["QT_FONT_DPI"] = "96"

"""
Attributes
----------
keys : list
    Contains the IEX and the Alphavantage keys as strings for API calls.
stock : dict
    Stores all the API callable stocks with their ticker and full name.
crypto : dict
    Stores all the API callable cryptos with their ticker and full name.
data : dict
    Stores the full data that has been called through API calls in a nested dictionnary.
pfdta : DataFrame
    Stores the cleaned and trimmed data of the portfolio, ready to be optimised.
pf : dict
    Stores the name and horizon
"""

#The main window
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)
        settings = Settings()
        self.settings = settings.items
        self.hide_grips = True
        SetupMainWindow.setup_gui(self)

        self.key = "demo"
        self.stock = dict()
        self.crypto = dict()
        self.data = dict()
        boot(self)
        self.pfdta = pd.DataFrame()
        self.pf = dict()

        self.show()

    #Main window buttons clicked
    def btn_clicked(self):
        btn = SetupMainWindow.setup_btns(self)       
        #Open home page
        if btn.objectName() == "btn_home":
            #Select menu
            self.ui.left_menu.select_only_one(btn.objectName())
            #Load page
            MainFunctions.set_page(self, self.ui.load_pages.page_1)
        #Open market page
        if btn.objectName() == "btn_market":
            #Select menu
            self.ui.left_menu.select_only_one(btn.objectName())
            #Load page
            MainFunctions.set_page(self, self.ui.load_pages.page_2)
        #Open portfolio page
        if btn.objectName() == "btn_portfolio":
            #Select menu
            self.ui.left_menu.select_only_one(btn.objectName())
            #Load page
            MainFunctions.set_page(self, self.ui.load_pages.page_3)
        
        top_btn_settings = MainFunctions.get_title_bar_btn(self, "btn_top_settings")
        #Open about menu
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
        #Open settings menu
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

    #Main window buttons released
    def btn_released(self):
        # GET BT CLICKED
        btn = SetupMainWindow.setup_btns(self)

        # DEBUG
        print(f"Button {btn.objectName()}, released!")

    #Resize main window
    def resizeEvent(self, event):
        SetupMainWindow.resize_grips(self)

    #Mouse click on window
    def mousePressEvent(self, event):
        # SET DRAG POS WINDOW
        self.dragPos = event.globalPos()

#Run the program
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("icon.ico"))
    window = MainWindow()

    sys.exit(app.exec())