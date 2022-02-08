from tkinter import Frame, StringVar, Label, LEFT, ttk


class TextInputFormItem(Frame):

    def __init__(self, master=None, cnf=None, label='', **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master=master, cnf=cnf, **kw)

        self.entry_var = StringVar()

        self.label = Label(self, width=10, text=label)
        self.label.pack(side=LEFT, padx=10)

        self.entry = ttk.Entry(self, width=20, textvariable=self.entry_var)
        self.entry.pack(side=LEFT)
