'''
self.horizon : str
        (optional) Indicates the max date of the portfolio. Default is 1st May 2019.
'''

#Front-end
import sys
import os
from qt_core import *
from gui.uis.windows.main_window.functions_main_window import *
from gui.core.json_settings import Settings
from gui.uis.windows.main_window import *
from gui.widgets import *
os.environ["QT_FONT_DPI"] = "96"

#Back-end
from portfolio import *

#The main window
class MainWindow(QMainWindow):
    def __init__(self):
        #Back-end
        self.key = "demo"
        self.keyesg = "5c92ad213380a777c20a6c7f523ca436"
        self.horizon = '2020-03-02'
        self.horizondyn = '2020-03-02'
        self.stock = dict()
        self.crypto = dict()
        self.data = dict()
        self.esg = dict()
        self.today = requests.get("https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo").json()["Meta Data"]["3. Last Refreshed"][0:10]
        self.pfdta = pd.DataFrame()
        self.pf = dict()
        boot(self)
        
        #Front-end
        super().__init__()
        self.ui = UI_MainWindow()
        self.ui.setup_ui(self)
        settings = Settings()
        self.settings = settings.items
        self.hide_grips = True
        SetupMainWindow.setup_gui(self)

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
        #Open about menu
        if btn.objectName() == "btn_about" or btn.objectName() == "btn_close_left_column":
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
            # Get about menu
            btn_about = MainFunctions.get_left_menu_btn(self, "btn_about")
            btn_about.set_active_tab(False)

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