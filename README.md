# Coursework: Advanced programming - A portfolio optimizer
## Welcome word
Welcome to the Radzuptimizer. It is, for now, a simple portfolio optimizer that was developed in the context of an advanced programming course at the University of Lausanne.

The GUI runs on PySide6 and the theme and widgets were developed by Wanderson M. Pimenta. All credits towards his work should be properly set up, I am terribly sorry if there is any mistake on that side.

## A dive into future developments
Right now, the next step for the application would be a switch to Python 3.9. It is more adequate for using Pyside6, and has more functionalities to exploit CPython -- I will talk later why it is important for further development. In any case, the project in its current state sits in a public repository on GitHub, github.com/Cairoknox/Advanced-Programming.

A big maintenance issue will be the access to both the Alpha Vantage API, and the ESG Enterprise API in the long-term. That said, a switch to the Swissquote API is currently considered as soon as I have the access. However, that would completely prevent users who do not have access to it to use the application. In my defense, I want to precise that this application is made for my private use in the first place and has absolutely no commercial nor philanthropic goal. This would lead us eventually to the version 2 of the application.

In version 2, many updates are already planned. First, once I get access to the Swissquote API, I want to make use of all the additional data they provide on businesses. Namely, I want to be able to plot historical time series, display information on the balance sheet, or for example provide links to the financial and impact reports. Also, I want to be able to draw typical patterns on these historical time series, like pitchforks, Gann fans or squares, and Fibonnaci retracements, arcs, fans, or time zones. Of course, this would also come with the possibility to plot candles.

Next, I think it would be nice to be able to include government bonds, cash (and foreign currencies), commodities, and futures. This would offer a complete palette of investment possibilities.

Then, I want to implement other portfolio optimization strategies. Namely, beyond mean variance optimization, I think of conditional VaR, risk parity, information ratio, Kelly criterion, tracking error, Sortino ratio, omega ratio, and maximum drawdown. I also want to be able to optimize based on other variables such as impact grades. At the same time, I want to be able to set minimum or maximum weight for each assets and to be able to set the starting and ending date. That would be the perfect time to think about implementation in CPython, and parallelization of the processes of the different algorithms. Technically, this last step of implementation is not a big deal as data is already prepared to be used as 2D arrays for basic matrix operations. This is really convenient.

That said, we can talk about the elephant in the room, cryptocurrencies. I did not talk much about them although they do not really fit that kind of portfolio allocation strategies due to their high volatility, very high correlation, and questionable returns. Eventually, I believe that by setting proper minimum and maximum weights on cryptocurrencies, they can have a coherent place in the portfolio allocation problem. Also, it would be nice to have some ESG data on them. As you may know, proof-of-work currencies are not energy efficient at all compared to proof-of-stake currencies. This may be one of the measures used to proxy ESG data.

At the end of this series of update, I would consider the product as viable. To conclude version 2 of the application, I would probably offer a GUI job. I would also start being concerned by the efficiency issues of the code. In its current structure, once the Swissquote API is implemented, the application can easily include all the aforementioned updates with very little Python coding. However, to move onward with version 3, I think that, instead of using just-in-time compiler or CPython, a big optimization module grouping all optimization methods could be written in C++ to help efficiency -- that said, everything could also be written in C++. Also, that would be the time for some Spring cleaning of the code, making it clearer, and thinking of alternatives to some structural choice I made early on.

Version 3 of the application enters a completely new and exciting realm. I am already thinking of developing forecasting tools with multiple models, out-of-sample performance measures, and so on. It should also include macroeconomics models and variables. In addition, the user will also have the ability to place orders with the app. Moreover, the user will be able to set up a bot for automatic orders at configurable thresholds.

## How to run the program
Developed on Windows but should run on Linux and macOS. Open and run the main.py file with Python 3.8.2 to start the program. It requires the installation of numpy, scipy, pandas, numba, PySide6, and pyqtgraph.

## Credits
The following files are modified from the original work of Wanderson M. Pimenta.

1. gui/uis/windows/main_window/setup_main_window.py (extensively modified)
2. main.py (slightly modified)
3. functions_main_window.py (slightly modified)
4. settings.json(barely modified)

The following files are the fruit of my own work.

1. portfolio.py
2. markowitz.py
3. main_pages.py
4. ui_left_column.py
5. crypto.json
6. esg.json
7. stock.json

## License
This work is subject to a MIT License. See the corresponding LICENSE file for more information on what you can do with it.

## Badges
[![Windows](https://svgshare.com/i/ZhY.svg)](https://svgshare.com/i/ZhY.svg)
[![forthebadge made-with-python](http://ForTheBadge.com/images/badges/made-with-python.svg)](https://www.python.org/)
[![GitHub release](https://img.shields.io/github/release/Naereen/StrapDown.js.svg)](https://github.com/Cairoknox/Advanced-Programming/releases/)
[![GitHub commits](https://badgen.net/github/commits/Naereen/Strapdown.js)](https://github.com/Cairoknox/Advanced-Programming/commit/)
[![GitHub license](https://badgen.net/github/license/Naereen/Strapdown.js)](https://github.com/Cairoknox/Advanced-Programming/blob/main/LICENSE)
