import ctypes
import tkinter as tk


class BasicWindow(tk.Tk):

    def __init__(self, screenName=None, baseName=None, className='Tk', useTk=1, sync=0, use=None):
        super().__init__(screenName, baseName, className, useTk, sync, use)

    def set_specs(self, w: int = 800, h: int = 600, x: int = None, y: int = None):
        if x is None:
            x = (self.winfo_screenwidth() // 2) - (w // 2)

        if y is None:
            y = (self.winfo_screenheight() // 2) - (h // 2)

        self.geometry(f'{w}x{h}+{x}+{y}')

    def fix_win_display(self):
        """

        修复视觉模糊，加强显示清晰度

        :return:

        """
        ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 告诉操作系统使用程序自身的dpi适配
        self.tk.call('tk', 'scaling', ctypes.windll.shcore.GetScaleFactorForDevice(0) / 75)  # 设置程序缩放
