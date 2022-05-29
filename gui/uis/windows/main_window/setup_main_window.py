#Copyright (c) 2021 Wanderson M. Pimenta
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so.
#Modified by Raphaël Radzuweit
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

#What should the main window contain
class SetupMainWindow:
    def __init__(self):
        super().__init__()
    #Left menu buttons
    add_left_menus = [
        {"btn_icon" : "icon_home.svg", "btn_id" : "btn_home", "btn_text" : "Home", "btn_tooltip" : "Home page", "show_top" : True, "is_active" : True},
        {"btn_icon" : "icon_search.svg", "btn_id" : "btn_market", "btn_text" : "Market data", "btn_tooltip" : "Market data", "show_top" : True, "is_active" : False},
        {"btn_icon" : "icon_send.svg", "btn_id" : "btn_portfolio", "btn_text" : "Portfolio", "btn_tooltip" : "Portfolio", "show_top" : True, "is_active" : False},
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
        ##MAINPAGE##
        #MAINPAGE: Add logo#
        self.logo = QSvgWidget(Functions.set_svg_image("logo_home.svg"))
        self.ui.load_pages.logo_layout.addWidget(self.logo, Qt.AlignCenter, Qt.AlignCenter)
        #MAINPAGE: Add API keys manager#
        self.line_API = QLineEdit()
        self.send_API = PyPushButton(text="send", radius=8,
        color=self.themes["app_color"]["text_foreground"], bg_color=self.themes["app_color"]["dark_one"],
        bg_color_hover=self.themes["app_color"]["dark_three"], bg_color_pressed=self.themes["app_color"]["dark_four"])
        #Save the API key entered by user
        self.API_manage = 0 #0 = get AV API key
        def print_API(): #Method to register the API keys
            API_key = self.line_API.text() #Get the text from the LineEdit
            if not API_key == "" and self.API_manage == 0: #Is the text field not empty and are we saving the AV API key? If yes...
                self.key = API_key #Save the AV API key
                print("AV API key loaded") #Giving a sign of life to the terminal
                self.line_API.clear() #Clear the LineEdit
                self.ui.load_pages.welcome_message_2.setText("Enter your ESG Enterprise API key...") #Change the text on the app
                self.API_manage = 1 #Next key to be saved will be ESGE API key
            elif not API_key =="" and self.API_manage == 1: #If no... is the text field not empty and are we saving the ESGE API key? If yes...
                self.keyesg = API_key #Save the ESGE API key
                print("ESGE API key loaded") #Giving a sign of life to the terminal
                self.line_API.clear() #Clear the LineEdit
                self.ui.load_pages.welcome_message_2.setText("You are now connected! You can change Alpha Vantage key...") #Change the text on the app
                self.API_manage = 0 #Next key to be saved will be AV API key
            else: #If no... 
                print("API key cannot be empty") #Giving a sign of life to the terminal
                if self.API_manage == 0: #Are we saving the AV API key? If yes...
                    self.ui.load_pages.welcome_message_2.setText("Error. Enter your Alpha Vantage API key...") #Change the text on the app
                    return
                self.ui.load_pages.welcome_message_2.setText("Error. Enter your ESG Enterprise API key...") #Change the text on the app
            return
        #Use the function on button click
        self.line_API.returnPressed.connect(print_API)
        self.send_API.clicked.connect(print_API)
        #Display both the text field and the send button
        self.ui.load_pages.API_key_layout.addWidget(self.line_API)
        self.ui.load_pages.API_key_layout.addWidget(self.send_API)
        ##MAINPAGE2##
        #MAINPAGE2: Choose any ticker#
        self.line_ticker = QLineEdit()
        self.add_ticker = PyPushButton(text="add", radius=8,
        color=self.themes["app_color"]["text_foreground"], bg_color=self.themes["app_color"]["dark_one"],
        bg_color_hover=self.themes["app_color"]["dark_three"], bg_color_pressed=self.themes["app_color"]["dark_four"])
        #Add the ticker to the portfolio
        def add_ticker(): #Method to add a ticker to the portfolio
            ticker = self.line_ticker.text() #Get the text from the LineEdit
            if ticker in self.stock or ticker in self.crypto: #Is the ticker valid? If yes...
                success = add(self, ticker) #Request to add the ticker to portfolio
                esg_add(self, ticker) #Request to get ESG data
                if success: #Do we have the data and was the ticker correctly added? If yes...
                    update_table(ticker, 'add') #Update the portfolio table
                self.line_ticker.clear() #Clear the LineEdit
            else: #If no...
                print("Wrong ticker") #Giving a sign of life to the terminal
                self.line_ticker.clear() #Clear the LineEdit
            return
        self.line_ticker.returnPressed.connect(add_ticker)
        self.add_ticker.clicked.connect(add_ticker)
        self.ui.load_pages.ask_layout.addWidget(self.line_ticker)
        self.ui.load_pages.ask_layout.addWidget(self.add_ticker)
        #MAINPAGE2: Table#
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
        def update_table(ticker, action, place = None): #Method to modify the table content
            if action == 'add': #Does the user want to add a row? If yes...
                nrow = self.table_widget.rowCount() #Count the number of rows
                self.table_widget.insertRow(nrow) #Insert a row at the end of the table
                self.table_widget.setRowHeight(nrow, 22) #Set the row's height
                self.table_widget.setItem(nrow, 1, QTableWidgetItem(ticker)) #In the second column, insert the ticker name
                self.closing = QTableWidgetItem() #Instantiate the closing quote
                self.closing.setTextAlignment(Qt.AlignRight) #Align it right
                self.esgtable = QTableWidgetItem() #Instantiate the ESG value
                self.esgtable.setTextAlignment(Qt.AlignCenter) #Align it center
                if ticker in self.crypto: #Is the ticker a crypto? If yes...
                    self.table_widget.setItem(nrow, 0, QTableWidgetItem(self.crypto[ticker])) #In the first column, insert the name of the crypto
                    self.closing.setText(str(round(float(self.data[ticker][self.today]["4a. close (USD)"]),4))) #Set the closing quote value
                elif ticker in self.stock: #If no... is the ticker a stock? If yes...
                    self.table_widget.setItem(nrow, 0, QTableWidgetItem(self.stock[ticker])) #In the first column, insert the name of the stock
                    self.closing.setText(str(round(float(self.data[ticker][self.today]["4. close"]),4))) #Set the closing quote value
                    self.esgtable.setText(self.esg[ticker]['total_grade'] + ' (' + str(self.esg[ticker]['total']) + ')',) #Set the ESG value
                self.table_widget.setItem(nrow, 2, self.closing) #In the third column, insert the closing quote
                self.table_widget.setItem(nrow, 3, self.esgtable) #In the fourth column, insert the ESG value
                return
            elif action == 'remove': #If no... does the user want to remove a row? If yes...
                try: #Try the following, if there is an impossibility, jumps to the except block
                    ticker = self.table_widget.item(self.table_widget.currentRow(),1).text() #Get the ticker name from the second column of the selected row
                    remove(self, ticker) #Remove said ticker from portfolio
                    print(ticker + ' removed from portfolio')  #Giving a sign of life to the terminal
                    self.table_widget.removeRow(self.table_widget.currentRow()) #Remove the row from the table
                except: #If something went wrong in the try block, most likely no row was selected
                    print('Nothing to remove') #Giving a sign of life to the terminal
                return
            elif action == 'optw': #If no... is there a request from the optimizer to add the optimal weight? If yes...
                self.optw = QTableWidgetItem() #Instantiate the optimal weight
                self.optw.setTextAlignment(Qt.AlignCenter) #Align it center
                self.optw.setText(str(round(self.weight[place], 3))) #Set the optimal weight value
                self.table_widget.setItem(place, 4, self.optw) #In the fifth column, insert the optimal weight value
                return
            return
        self.ui.load_pages.plot_layout.addWidget(self.table_widget)
        #Remove a row
        self.delete = PyPushButton(text="delete", radius=8,
        color=self.themes["app_color"]["text_foreground"], bg_color=self.themes["app_color"]["dark_one"],
        bg_color_hover=self.themes["app_color"]["dark_three"], bg_color_pressed=self.themes["app_color"]["dark_four"])
        def remove_ticker(): #Method to remove a ticker from portfolio
            update_table(None, 'remove') #Ask to remove the ticker
            return
        self.shortcut = QShortcut(QKeySequence("del"), self)
        self.shortcut.activated.connect(remove_ticker)
        self.delete.clicked.connect(remove_ticker)
        self.ui.load_pages.ask_layout.addWidget(self.delete)
        ##MAINPAGE3##
        #MAINPAGE3: Create portfolio
        self.construct = PyPushButton(text="construct", radius=8,
        color=self.themes["app_color"]["text_foreground"], bg_color=self.themes["app_color"]["dark_one"],
        bg_color_hover=self.themes["app_color"]["dark_three"], bg_color_pressed=self.themes["app_color"]["dark_four"])

        self.optimize = PyPushButton(text="optimize", radius=8,
        color=self.themes["app_color"]["text_foreground"], bg_color=self.themes["app_color"]["dark_one"],
        bg_color_hover=self.themes["app_color"]["dark_three"], bg_color_pressed=self.themes["app_color"]["dark_four"])
        self.text_construct = QLabel("constructed")
        self.plot = pg.PlotWidget()
        scatter = pg.ScatterPlotItem(hoverable = True)
        scatter.setSize(6)
        scatteropt = pg.ScatterPlotItem(hoverable = True)
        scatteropt.setSize(14)
        scatteropt.setBrush(221, 44, 0, 240)
        plot = pg.PlotCurveItem()
        #Run data_get on button push
        def construct(): #Method to construct the portfolio
            construct_pf(self) #Ask to construct the portfolio
            self.ui.load_pages.constroptimize_layout.addWidget(self.text_construct) #Change the text on the app
        self.construct.clicked.connect(construct)
        #Optimize and plot
        def optim(): #Method to optimize and plot the result
            markowitz_init(self) #Ask to optimize the portfolio
            scatteropt.clear() #Clear the variable from any previous work
            scatter.clear() #Clear the variable from any previous work
            plot.clear() #Clear the variable from any previous work
            scatteropt.addPoints([self.optim2[0]], [self.optim2[1]]) #Add the efficient portfolio from non-linear optimization. Remove the '2's to get the one from Monte-Carlo
            scat_df = pd.DataFrame() #Instantiate a DataFrame
            for i in ['volatility', 'returns', 'sharpe_ratios']: #For each variable of interest
                scat_df[i] = eval('self.' + i + '.tolist()') #Add a column to the DataFrame
            scat_df = scat_df.sort_values(by = 'sharpe_ratios') #Sort by Sharpe ratios
            brush = ['#fdcf52', '#f5b95c', '#e3a646', '#f7a96a', '#d56b28', '#ee6432', '#c85b2d', '#b82b1f', '#a83c32', '#7f2c20'] #Set up the color mapping (yes, by hand ahah)
            rep = np.append(np.repeat(len(scat_df)//len(brush), 9), np.array(len(scat_df)//len(brush) + len(scat_df)%len(brush))) #For each 10 colors we give an equal amount of points
            for i in range(len(rep)): #For each 10 colors
                scatter.addPoints(list(scat_df['volatility'][i*rep[0]:(i*rep[0]+rep[i])]), list(scat_df['returns'][i*rep[0]:(i*rep[0]+rep[i])]), brush = brush[i], pen = brush[i]) #Add the set of points with the corresponding colors
            plot.setData(self.volatility2, self.returns2, pen = pg.mkPen('r', width=4)) #Plot the efficient frontier from non-linear optimization
            self.plot.addItem(scatter) #Load on graph
            self.plot.addItem(scatteropt) #Load on graph
            self.plot.addItem(plot) #Load on graph
            a = 0 #Instantiate a temp variable to zero (a bit sketchy I know but it works)
            for i in self.pf[self.horizondyn]["stock"] + self.pf[self.horizondyn]["crypto"]: #For each ticker in the portfolio
                update_table(i, 'optw', a) #Add the corresponding weight to the table
                a += 1 #Next row
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
