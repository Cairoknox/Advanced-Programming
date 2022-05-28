#Copyright (c) 2021 Wanderson M. Pimenta
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so.
# IMPORT QT CORE
# ///////////////////////////////////////////////////////////////
from qt_core import *

# STYLE
# ///////////////////////////////////////////////////////////////
style = '''
QPushButton {{
	border: none;
    padding-left: 10px;
    padding-right: 5px;
    color: {_color};
	border-radius: {_radius};	
	background-color: {_bg_color};
}}
QPushButton:hover {{
	background-color: {_bg_color_hover};
}}
QPushButton:pressed {{	
	background-color: {_bg_color_pressed};
}}
'''

# PY PUSH BUTTON
# ///////////////////////////////////////////////////////////////
class PyPushButton(QPushButton):
    def __init__(
        self, 
        text,
        radius,
        color,
        bg_color,
        bg_color_hover,
        bg_color_pressed,
        parent = None,
    ):
        super().__init__()

        # SET PARAMETRES
        self.setText(text)
        if parent != None:
            self.setParent(parent)
        self.setCursor(Qt.PointingHandCursor)

        # SET STYLESHEET
        custom_style = style.format(
            _color = color,
            _radius = radius,
            _bg_color = bg_color,
            _bg_color_hover = bg_color_hover,
            _bg_color_pressed = bg_color_pressed
        )
        self.setStyleSheet(custom_style)

        