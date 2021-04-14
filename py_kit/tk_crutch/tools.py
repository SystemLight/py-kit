from tkinter.constants import FALSE
from typing import Union

from ..unit import px2pt


def specs(component, w: int = 800, h: int = 600, x: int = None, y: int = None):
    if x is None:
        x = (component.winfo_screenwidth() // 2) - (w // 2)

    if y is None:
        y = (component.winfo_screenheight() // 2) - (h // 2)

    component.geometry(f"{w}x{h}+{x}+{y}")


def font(family: str = "SimHei", size_px: Union[int, float] = 14, is_bold: bool = FALSE):
    return family, int(px2pt(size_px)), "bold" if is_bold else "normal"
