import tkinter as tk
from tkinter import ttk

from .basic_component import BasicWindow
from .provider import *


class AppWindow(BasicWindow):

    def __init__(self, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

        self._is_set_specs = False

    def set_specs(self, w: int = 800, h: int = 600, x: int = None, y: int = None):
        super().set_specs(w, h, x, y)
        self._is_set_specs = True

    def mainloop(self, n=0, is_set_specs=True):
        if is_set_specs is True and not self._is_set_specs:
            self.set_specs()

        super().mainloop(n)

    start = run = mainloop

    def Label(self, provider: LabelCnfProvider):
        """

        构建Label组件

        :param provider:
        :return:

        """
        return tk.Label(self, provider.build())

    def Button(self, provider: ButtonCnfProvider):
        """

        构建Button组件

        :param provider:
        :return:

        """
        return tk.Button(self, provider.build())

    def RadioButton(self, provider: RadioButtonCnfProvider):
        """

        构建单选组件

        :param provider:
        :return:

        """
        return tk.Radiobutton(self, provider.build())

    def CheckButton(self, provider: CheckButtonCnfProvider):
        """

        构建多选框组件

        :param provider:
        :return:

        """
        return tk.Checkbutton(self, provider.build())

    def Entry(self, provider: EntryCnfProvider):
        """

        构建文本输入框组件

        :param provider:
        :return:

        """
        return tk.Entry(self, provider.build())

    def Frame(self, provider: FrameCnfProvider):
        """

        构建组件盒子容器

        :param provider:
        :return:

        """
        return tk.Frame(self, provider.build())

    def LabelFrame(self, provider: LabelFrameCnfProvider):
        """

        构建组件内联盒子容器

        :param provider:
        :return:

        """
        return tk.LabelFrame(self, provider.build())

    def Separator(self, provider: SeparatorCnfProvider):
        """

        构建分割线组件

        :param provider:
        :return:

        """
        return ttk.Separator(self, **provider.build())
