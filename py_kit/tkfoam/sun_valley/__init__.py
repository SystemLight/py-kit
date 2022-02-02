import os
from typing import TypeVar, Literal

WidgetType = TypeVar('WidgetType')


def set_theme(widget: WidgetType, theme: Literal['light', 'dark'] = 'light') -> WidgetType:
    widget.tk.call('source', os.path.join(os.path.dirname(__file__), 'sun-valley.tcl'))
    widget.tk.call('set_theme', theme)
    return widget
