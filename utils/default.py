from typing import Optional
import webbrowser
import os


class _magic:
	def __init__(self):
		self.color_black = "\033[30m"
		self.color_red = "\033[31m"
		self.color_green = "\033[32m"
		self.color_yellow = "\033[33m"
		self.color_blue = "\033[34m"
		self.color_magenta = "\033[35m"
		self.color_cyan = "\033[36m"
		self.color_white = "\033[37m"
		self.color_underline = "\033[4m"
		self.color_bold = "\033[1m"
		self.color_blink = "\033[5m"
		self.color_highlight_black = "\033[7m"
		self.color_highlight_red = "\033[41m"
		self.color_highlight_green = "\033[42m"
		self.color_highlight_yellow = "\033[43m"
		self.color_highlight_blue = "\033[44m"
		self.color_highlight_magenta = "\033[45m"
		self.color_highlight_cyan = "\033[46m"
		self.color_highlight_white = "\033[47m"
		self.color_reset = "\033[0m"


	def colorize(self, text: str, color: str) -> str:
		""" Colorizes the text with the given color """
		return color + text + Magic.color_reset

	def print(self, text: str, color: str, new_line : Optional[bool] = False):
		""" Colorizes and prints the text """
		os.system('')
		new_line = "\n" if (new_line) else ""
		print(new_line + self.colorize(text, color))

Magic = _magic()


class _web:
	def __init__(self): pass


	def open(self, url: str, color: str, path: str):
		""" Opens the url in a browser window """
		if input(Magic.colorize("Open? [y/n]: ", color)).lower() == "y": [webbrowser.open(path[i][url]) for i in range(len(path))]

Web = _web()


class _error:
	def __init__(self): pass


	def NotFound(self):
		""" Raises a 404 error and quits the program """
		Magic.print("[Error 404]: Data not found", Magic.color_underline, True)
		exit()

Error = _error()