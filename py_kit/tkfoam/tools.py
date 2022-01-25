import ctypes
from tkinter.constants import FALSE
from typing import Union, TypeVar

from .unit import px2pt

WidgetType = TypeVar('WidgetType')


def fix_win_display(widget: WidgetType) -> WidgetType:
    """

    修复视觉模糊，加强显示清晰度

    :return:

    """
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # 告诉操作系统使用程序自身的dpi适配
    widget.tk.call('tk', 'scaling', ctypes.windll.shcore.GetScaleFactorForDevice(0) / 75)  # 设置程序缩放
    return widget


def specs(widget: WidgetType, w: int = 800, h: int = 600, x: int = None, y: int = None) -> WidgetType:
    if x is None:
        x = (widget.winfo_screenwidth() // 2) - (w // 2)

    if y is None:
        y = (widget.winfo_screenheight() // 2) - (h // 2)

    widget.geometry(f'{w}x{h}+{x}+{y}')

    return widget


def font(family: str = 'SimHei', size_px: Union[int, float] = 14, is_bold: bool = FALSE):
    return family, int(px2pt(size_px)), 'bold' if is_bold else 'normal'


default_font = font()
