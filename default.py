import os
from typing import Optional

class Magic:
    color_black = "\033[30m"
    color_red = "\033[31m"
    color_green = "\033[32m"
    color_yellow = "\033[33m"
    color_blue = "\033[34m"
    color_magenta = "\033[35m"
    color_cyan = "\033[36m"
    color_white = "\033[37m"
    color_underline = "\033[4m"
    color_bold = "\033[1m"
    color_blink = "\033[5m"
    color_highlight_black = "\033[7m"
    color_highlight_red = "\033[41m"
    color_highlight_green = "\033[42m"
    color_highlight_yellow = "\033[43m"
    color_highlight_blue = "\033[44m"
    color_highlight_magenta = "\033[45m"
    color_highlight_cyan = "\033[46m"
    color_highlight_white = "\033[47m"
    color_reset = "\033[0m"

    def print(text : str, color : str, new_line : Optional[bool] = False):
        new_line = "\n" if new_line else ""
        os.system('')
        print(new_line + color + text + Magic.color_reset)
    
    def colored(text : str, color : str):
        return color + text + Magic.color_reset


import webbrowser

class Web:
    def open(url, color, path):
        Magic.print("Open?", color, True)
        open = input("")
        if open.lower() == "yes": [webbrowser.open(path[i][url]) for i in range(len(path))]


class Error:
    def not_found():
        Magic.print("[Error 404]: Data not found", Magic.color_underline, True)
        exit()