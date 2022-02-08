from tkinter import Frame, IntVar, Label, LEFT, ttk


class NumberInputFormItem(Frame):

    def __init__(self, master=None, cnf=None, label='', **kw):
        if cnf is None:
            cnf = {}
        super().__init__(master=master, cnf=cnf, **kw)

        self.entry_var = IntVar(value=1)

        self.label = Label(self, width=10, text=label)
        self.label.pack(side=LEFT, padx=10)

        self.entry = ttk.Entry(
            self, width=20, textvariable=self.entry_var,
            validate="key", validatecommand=(self.register(NumberInputFormItem.validate_number), '%P')
        )
        self.entry.pack(side=LEFT)

    @staticmethod
    def validate_number(content):
        if content.isdigit() and int(content) > 0:
            return True
        else:
            return False
