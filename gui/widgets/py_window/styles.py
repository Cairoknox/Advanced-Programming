#Copyright (c) 2021 Wanderson M. Pimenta
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so.

class Styles(object):
    bg_style = """
    #pod_bg_app {{
        background-color: {_bg_color};
        border-radius: {_border_radius};
        border: {_border_size}px solid {_border_color};
    }}
    QFrame {{ 
        color: {_text_color};
        font: {_text_font};
    }}
    """