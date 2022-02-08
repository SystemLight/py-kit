from tkinter import Button

from ..constants import ThemeColor, Cursor
from ..utils import default_font


class PrimaryButton(Button):

    def __init__(self, master=None, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        self['padx'] = 15
        self['pady'] = 6
        self['cursor'] = Cursor.POINTER
        self['font'] = default_font
        self['borderwidth'] = 0
        self['fg'] = ThemeColor.white
        self['bg'] = ThemeColor.primary
        self['activebackground'] = ThemeColor.active_primary
        self['activeforeground'] = ThemeColor.white


class DangerButton(Button):

    def __init__(self, master=None, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master, cnf, **kw)

        self['padx'] = 15
        self['pady'] = 6
        self['cursor'] = Cursor.POINTER
        self['font'] = default_font
        self['borderwidth'] = 0
        self['fg'] = ThemeColor.white
        self['bg'] = ThemeColor.danger
        self['activebackground'] = ThemeColor.active_danger
        self['activeforeground'] = ThemeColor.white
