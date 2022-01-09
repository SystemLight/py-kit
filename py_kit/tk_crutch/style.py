from tkinter.constants import *

from .theme import ThemeColor, Cursor
from .tools import font

default_font = font()

# 向左漂浮样式
float_left_pack_cnf = {
    'anchor': NW,
    'side': LEFT
}

# 向左漂浮水平方向有间距
float_left_px10_pack_cnf = float_left_pack_cnf.copy()
float_left_px10_pack_cnf['padx'] = 10

# 确认按钮样式
primary_button_cnf = {
    'padx': 15,
    'pady': 6,
    'cursor': Cursor.POINTER,
    'borderwidth': 0,
    'font': default_font,
    'fg': ThemeColor.white,
    'bg': ThemeColor.primary,
    'activebackground': ThemeColor.active_primary,
    'activeforeground': ThemeColor.white
}

# 危险按钮样式
danger_button_cnf = {
    'padx': 15,
    'pady': 6,
    'cursor': Cursor.POINTER,
    'borderwidth': 0,
    'font': default_font,
    'fg': ThemeColor.white,
    'bg': ThemeColor.danger,
    'activebackground': ThemeColor.active_danger,
    'activeforeground': ThemeColor.white
}
