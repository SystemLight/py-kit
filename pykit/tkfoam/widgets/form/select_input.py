from tkinter import Frame, StringVar, Label, LEFT, ttk


class SelectFormItem(Frame):

    def __init__(self, master=None, cnf=None, label="", values=tuple(), **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master=master, cnf=cnf, **kw)

        self.combobox_var = None
        if len(values) > 0:
            self.combobox_var = StringVar(value=values[0])

        self.label = Label(self, width=10, text=label)
        self.label.pack(side=LEFT, padx=10)

        self.combobox = ttk.Combobox(self, width=30, textvariable=self.combobox_var, values=values, state='readonly')
        self.combobox.pack(side=LEFT)
