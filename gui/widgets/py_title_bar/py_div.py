#Copyright (c) 2021 Wanderson M. Pimenta
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so.
# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# CUSTOM LEFT MENU
# ///////////////////////////////////////////////////////////////
class PyDiv(QWidget):
    def __init__(self, color):
        super().__init__()

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0,5,0,5)
        self.frame_line = QFrame()
        self.frame_line.setStyleSheet(f"background: {color};")
        self.frame_line.setMaximumWidth(1)
        self.frame_line.setMinimumWidth(1)
        self.layout.addWidget(self.frame_line)
        self.setMaximumWidth(20)
        self.setMinimumWidth(20)
