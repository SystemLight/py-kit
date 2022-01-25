import imghdr
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

from ..button import PrimaryButton


class ChooseImage(Frame):

    def __init__(self, master=None, cnf=None, **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master=master, cnf=cnf, **kw)

        self.entry_var = StringVar()

        self.entry = Entry(self, width=30, textvariable=self.entry_var)
        self.entry.pack(side=LEFT, ipady=5)

        self.button = PrimaryButton(self, text="选择文件", border=1, cursor='hand2', command=self.choose_file)
        self.button.pack(side=LEFT, ipady=2)

    def choose_file(self):
        result_path = askopenfilename()
        try:
            if imghdr.what(result_path):
                self.entry_var.set(result_path)
            else:
                messagebox.showerror('错误', '非图片文件')
        except FileNotFoundError:
            ...


class ChooseImageFormItem(Frame):

    def __init__(self, master=None, cnf=None, label='', **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master=master, cnf=cnf, **kw)

        self.label = Label(self, width=10, text=label)
        self.label.pack(side=LEFT, padx=10)

        self.choose_image = ChooseImage(self)
        self.choose_image.pack(side=LEFT)
