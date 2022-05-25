#Front-end
from . functions_main_window import *
from qt_core import *
from gui.core.json_settings import Settings
from gui.core.json_themes import Themes
from gui.widgets import *
from . ui_main import *
from . functions_main_window import *
import pyqtgraph as pg

#Back-end
from portfolio import *
from markowitz import *
from markowitz2 import *

#What should the main window contain
class SetupMainWindow:
    def __init__(self):
        super().__init__()
    
    #Left menu buttons
    add_left_menus = [
        {"btn_icon" : "icon_home.svg", "btn_id" : "btn_home", "btn_text" : "Home", "btn_tooltip" : "Home page", "show_top" : True, "is_active" : True},
        {"btn_icon" : "icon_file.svg", "btn_id" : "btn_market", "btn_text" : "Market data", "btn_tooltip" : "Market data", "show_top" : True, "is_active" : False},
        {"btn_icon" : "icon_file.svg", "btn_id" : "btn_portfolio", "btn_text" : "Portfolio", "btn_tooltip" : "Portfolio", "show_top" : True, "is_active" : False},
        {"btn_icon" : "icon_info.svg", "btn_id" : "btn_about", "btn_text" : "About", "btn_tooltip" : "About", "show_top" : False, "is_active" : False}
    ]
    
    #This gets called on button click, returns the action that the button is designed for
    def setup_btns(self):
        if self.ui.title_bar.sender() != None:
            return self.ui.title_bar.sender()
        elif self.ui.left_menu.sender() != None:
            return self.ui.left_menu.sender()
        elif self.ui.left_column.sender() != None:
            return self.ui.left_column.sender()
    
    #Interaction between front- and back-end
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
        #Trigger an event when title bar menu button is clicked
        self.ui.title_bar.clicked.connect(self.btn_clicked)
        #Add the custom title bar to the GUI
        if self.settings["custom_title_bar"]:
            self.ui.title_bar.set_title(self.settings["app_name"])
        else:
            self.ui.title_bar.set_title("Welcome to Radzuptimizer")
        #Add the left column menu
        #Trigger an event when left column menu button is clicked
        self.ui.left_column.clicked.connect(self.btn_clicked)
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
        self.line_API = QLineEdit()
        self.send_API = PyPushButton(text="send", radius=8,
        color=self.themes["app_color"]["text_foreground"], bg_color=self.themes["app_color"]["dark_one"],
        bg_color_hover=self.themes["app_color"]["dark_three"], bg_color_pressed=self.themes["app_color"]["dark_four"])
        #self.text = QLabel("connected")
        #Save the API key entered by user
        def print_API():
            API_key = self.line_API.text()
            if not API_key == "":
                self.key = API_key
                print("API key loaded.")
                self.ui.load_pages.welcome_message_2.setText("You are now connected!")
            else:
                #self.text.text("error")
                print("API key cannot be empty")
                self.ui.load_pages.welcome_message_2.setText("Error. Enter your AlphaVantage API key...")
            #self.ui.load_pages.API_key_layout.addWidget(self.text)
        #Use the function on button click
        self.send_API.clicked.connect(print_API)
        #Display both the text field and the send button
        self.ui.load_pages.API_key_layout.addWidget(self.line_API)
        self.ui.load_pages.API_key_layout.addWidget(self.send_API)

        #mainpage2: Choose any ticker
        self.line_ticker = QLineEdit()
        self.add_ticker = PyPushButton(text="add", radius=8,
        color=self.themes["app_color"]["text_foreground"], bg_color=self.themes["app_color"]["dark_one"],
        bg_color_hover=self.themes["app_color"]["dark_three"], bg_color_pressed=self.themes["app_color"]["dark_four"])
        #Add the ticker to the portfolio
        def add_ticker():
            ticker = self.line_ticker.text()
            if ticker in self.stock or ticker in self.crypto:
                success = add(self, ticker)
                esg_add(self, ticker)
                if success:
                    update_table(ticker, 'add')
            else:
                print("Wrong ticker")
            return
        self.add_ticker.clicked.connect(add_ticker)

        self.ui.load_pages.ask_layout.addWidget(self.line_ticker)
        self.ui.load_pages.ask_layout.addWidget(self.add_ticker)
        #mainpage2: Table
        self.table_widget = PyTableWidget(
            radius = 8,
            color = self.themes["app_color"]["text_foreground"],
            selection_color = self.themes["app_color"]["context_color"],
            bg_color = self.themes["app_color"]["bg_two"],
            header_horizontal_color = self.themes["app_color"]["dark_two"],
            header_vertical_color = self.themes["app_color"]["bg_three"],
            bottom_line_color = self.themes["app_color"]["bg_three"],
            grid_line_color = self.themes["app_color"]["bg_one"],
            scroll_bar_bg_color = self.themes["app_color"]["bg_one"],
            scroll_bar_btn_color = self.themes["app_color"]["dark_four"],
            context_color = self.themes["app_color"]["context_color"]
        )
        #Size and column names
        self.table_widget.setColumnCount(5)
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table_widget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_widget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.column_1 = QTableWidgetItem()
        self.column_1.setTextAlignment(Qt.AlignCenter)
        self.column_1.setText("Stock")
        self.column_2 = QTableWidgetItem()
        self.column_2.setTextAlignment(Qt.AlignCenter)
        self.column_2.setText("Ticker")
        self.column_3 = QTableWidgetItem()
        self.column_3.setTextAlignment(Qt.AlignCenter)
        self.column_3.setText("Last close (USD)")
        self.column_4 = QTableWidgetItem()
        self.column_4.setTextAlignment(Qt.AlignCenter)
        self.column_4.setText("ESG grade (score)")
        self.column_5 = QTableWidgetItem()
        self.column_5.setTextAlignment(Qt.AlignCenter)
        self.column_5.setText("Optimal weight")
        self.table_widget.setHorizontalHeaderItem(0, self.column_1)
        self.table_widget.setHorizontalHeaderItem(1, self.column_2)
        self.table_widget.setHorizontalHeaderItem(2, self.column_3)
        self.table_widget.setHorizontalHeaderItem(3, self.column_4)
        self.table_widget.setHorizontalHeaderItem(4, self.column_5)
        #Add a row
        def update_table(ticker, action):
            if action == 'add':
                nrow = self.table_widget.rowCount()
                self.table_widget.insertRow(nrow)
                self.table_widget.setRowHeight(nrow, 22)
                self.table_widget.setItem(nrow, 1, QTableWidgetItem(ticker))
                self.closing = QTableWidgetItem()
                self.closing.setTextAlignment(Qt.AlignRight)
                self.esgtable = QTableWidgetItem()
                self.esgtable.setTextAlignment(Qt.AlignCenter)
                if ticker in self.crypto:
                    self.table_widget.setItem(nrow, 0, QTableWidgetItem(self.crypto[ticker]))
                    self.closing.setText(str(round(float(self.data[ticker][self.today]["4a. close (USD)"]),4)))
                elif ticker in self.stock:
                    self.table_widget.setItem(nrow, 0, QTableWidgetItem(self.stock[ticker]))
                    self.closing.setText(str(round(float(self.data[ticker][self.today]["4. close"]),4)))
                    self.esgtable.setText(self.esg[ticker]['total_grade'] + ' (' + str(self.esg[ticker]['total']) + ')',)
                self.table_widget.setItem(nrow, 2, self.closing)
                self.table_widget.setItem(nrow, 3, self.esgtable)
                return
            elif action == 'remove':
                try:
                    ticker = self.table_widget.item(self.table_widget.currentRow(),1).text()
                    remove(self, ticker)
                    print(ticker + ' removed from portfolio')
                    self.table_widget.removeRow(self.table_widget.currentRow())
                    self.table_widget.item
                except:
                    print('Nothing to remove')
                return
        self.ui.load_pages.plot_layout.addWidget(self.table_widget)
        #Remove a row
        self.delete = PyPushButton(text="delete", radius=8,
        color=self.themes["app_color"]["text_foreground"], bg_color=self.themes["app_color"]["dark_one"],
        bg_color_hover=self.themes["app_color"]["dark_three"], bg_color_pressed=self.themes["app_color"]["dark_four"])
        def remove_ticker():
            update_table(None, 'remove')
            return
        self.delete.clicked.connect(remove_ticker)
        self.ui.load_pages.ask_layout.addWidget(self.delete)

        #mainpage3: Create portfolio
        self.construct = PyPushButton(text="construct", radius=8,
        color=self.themes["app_color"]["text_foreground"], bg_color=self.themes["app_color"]["dark_one"],
        bg_color_hover=self.themes["app_color"]["dark_three"], bg_color_pressed=self.themes["app_color"]["dark_four"])

        self.optimize = PyPushButton(text="optimize", radius=8,
        color=self.themes["app_color"]["text_foreground"], bg_color=self.themes["app_color"]["dark_one"],
        bg_color_hover=self.themes["app_color"]["dark_three"], bg_color_pressed=self.themes["app_color"]["dark_four"])

        self.text_construct = QLabel("constructed")

        self.plot = pg.PlotWidget()
        scatter = pg.ScatterPlotItem()
        scatter.setSize(10)
        scatter.setBrush(255, 255, 255, 120)
        scatteropt = pg.ScatterPlotItem()
        scatteropt.setSize(14)
        scatteropt.setBrush(221, 44, 0, 240)

        #Run data_get on button push
        def construct():
            construct_pf(self)
            self.ui.load_pages.constroptimize_layout.addWidget(self.text_construct)
        self.construct.clicked.connect(construct)
        
        #Optimize and plot
        def optim():
            # markowitz(self)
            # scatter.addPoints(self.vol_arr.tolist(), self.ret_arr.tolist())
            # scatteropt.addPoints([self.max_sr_vol], [self.max_sr_ret])
            markowitz_init(self)
            scatter.addPoints(self.volatility.tolist(), self.returns.tolist())
            # self.plot(self.frontier_x, self.frontier_y)
            self.plot.addItem(scatter)
            self.plot.addItem(scatteropt)
            # for gradient-->self.sharpe_arr
        self.optimize.clicked.connect(optim)

        self.ui.load_pages.constroptimize_layout.addWidget(self.construct)
        self.ui.load_pages.constroptimize_layout.addWidget(self.optimize)
        self.ui.load_pages.markowitz_layout.addWidget(self.plot)

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
