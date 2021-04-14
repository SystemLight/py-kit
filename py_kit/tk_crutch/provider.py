from tkinter import PhotoImage
from tkinter.constants import *
from typing import Union

from .theme import ThemeColor, Cursor
from ..unit import px2pt


class BasicCnfProvider:

    def __init__(self, **kwargs):
        # 其它更多参数
        self._kwargs = kwargs

    def build(self):
        local_content = self.__dict__
        out_put_dic = {}
        for k in local_content:
            if k == "_kwargs":
                continue
            out_put_dic[k] = local_content[k]
        out_put_dic.update(local_content["_kwargs"])
        return out_put_dic


class WidgetCnfProvider(BasicCnfProvider):

    def __init__(self, **kwargs):
        BasicCnfProvider.__init__(self, **kwargs)

        # 前景色
        self.fg = self.foreground = None

        # 背景色
        self.bg = self.background = None

        # 当功能组件获取焦点时背景颜色
        self.highlightbackground = None

        # 当功能组件获取焦点时文字颜色
        self.highlightcolor = None

        # 组件宽度
        self.width = None

        # 组件高度
        self.height = None

        # 文本到多少宽度换行，单位是像素
        self.wraplength = None

        # 文字字体
        self.font = None

        # 存在多行文本时最后一行的对齐方式
        self.justify = CENTER

        """

        内置位图：
            error
            hourglass
            info
            questhead
            question
            warning
            gray12
            gray25
            gray50
            gray75

        """
        self.bitmap = None

        # 位图与文字共存时，文字位置
        self.compound = None

        # 控制标签的外框样式
        self.relief = None

        # 水平边距
        self.padx = None

        # 垂直边距
        self.pady = None

        # 设置 PhotoImage 图片对象
        self.image = None

        # 设置光标形状
        self.cursor = None

        # 边框大小
        self.bd = self.borderwidth = None

        # 组件状态
        self.state = NORMAL

    def set_font(self, family: str = "SimHei", size: Union[int, float] = 12, is_bold: bool = FALSE):
        self.font = (family, size, "bold" if is_bold else "normal")
        return self

    def set_img(self, image_path: str):
        """

        支持图片格式 PGM, PPM, GIF, PNG
        更多格式使用PIL处理

        :param image_path:
        :return:

        """
        self.image = PhotoImage(file=image_path)
        return self


class CommandCnfProvider:

    def __init__(self):
        # 激活回调函数
        self.command = None

    def register_command(self, func):
        self.command = func


class LabelCnfProvider(WidgetCnfProvider):

    def __init__(self, **kwargs):
        WidgetCnfProvider.__init__(self, **kwargs)

        # 组件在盒子中内容位置
        self.anchor = CENTER

        # 是否存在下划线，定义在第几个字母下添加
        self.underline = -1

        # Label标签文字内容
        self.text = ""

        # 文本变量
        self.textvariable = None


class ButtonCnfProvider(WidgetCnfProvider, CommandCnfProvider):

    def __init__(self, **kwargs):
        WidgetCnfProvider.__init__(self, **kwargs)

        # 组件在盒子中内容位置
        self.anchor = CENTER

        # 是否存在下划线
        self.underline = -1

        # 获取焦点时凸出显示厚度
        self.highlightthickness = None

        # 激活按钮时前景和背景颜色
        self.activebackground = None
        self.activeforeground = None

        self.disabledforeground = None


class RadioButtonCnfProvider(WidgetCnfProvider, CommandCnfProvider):

    def __init__(self, **kwargs):
        WidgetCnfProvider.__init__(self, **kwargs)

        # 鼠标光标在选项按钮上时的背景颜色
        self.activebackground = None

        # 鼠标光标在选项按钮上时的前景颜色
        self.activeforeground = None

        # 当选项按钮被选取时的图像
        self.selectcolor = None

        # 当选项按钮被选取时的颜色
        self.selectimage = None

        # 当此值为0时，用盒子取代选项按钮
        self.indicatoron = None

        # 文本变量
        self.textvariable = None

        # 选项按钮的值
        self.value = None

        # 设置或取得目前选取的单选按钮，tk变量对象
        self.variable = None


class CheckButtonCnfProvider(WidgetCnfProvider, CommandCnfProvider):

    def __init__(self, **kwargs):
        WidgetCnfProvider.__init__(self, **kwargs)

        # 鼠标光标在选项按钮上时的背景颜色
        self.activebackground = None

        # 鼠标光标在选项按钮上时的前景颜色
        self.activeforeground = None

        # 禁用时颜色
        self.disabledforeground = None

        # 当选项按钮被选取时的图像
        self.selectcolor = None

        # 当选项按钮被选取时的颜色
        self.selectimage = None

        # 当此值为0时，用盒子取代选项按钮
        self.indicatoron = None

        # 文本变量
        self.textvariable = None

        # 设置或取得目前选取的单选按钮，tk变量对象
        self.variable = None

        # 设置默认未选中复选框是0
        self.offvalue = None

        # 设置默认未选中复选框是1
        self.onvalue = None


class EntryCnfProvider(WidgetCnfProvider):

    def __init__(self, **kwargs):
        WidgetCnfProvider.__init__(self, **kwargs)

        # 选取的字符串是否自动到剪贴板中
        self.exportselection = FALSE

        # 显示输入字符串
        self.show = None

        # 被选取字符串的背景颜色
        self.selectbackground = None

        # 被选取字符串的前景颜色
        self.selectfroeground = None

        # 选取字符串时的边界宽度
        self.selectborderwidth = 1

        # 在x轴使用滚动条
        self.xscrollcommand = FALSE

        # 文本变量
        self.textvariable = None


class FrameCnfProvider(WidgetCnfProvider):

    def __init__(self, **kwargs):
        WidgetCnfProvider.__init__(self, **kwargs)

        del self.justify
        del self.state


class LabelFrameCnfProvider(WidgetCnfProvider):

    def __init__(self, **kwargs):
        WidgetCnfProvider.__init__(self, **kwargs)

        del self.justify
        del self.state

        # 盒子文本内容
        self.text = None

        # 盒子文本锚点
        self.labelAnchor = None


class TkcButtonCnfProvider(ButtonCnfProvider):

    def __init__(self, **kwargs):
        ButtonCnfProvider.__init__(self, **kwargs)

        self.set_font(size=int(px2pt(14)))
        self.text = "按 钮"
        self.fg = ThemeColor.white
        self.bg = ThemeColor.primary
        self.padx = 15
        self.pady = 6
        self.cursor = Cursor.POINTER
        self.borderwidth = 0
        self.activebackground = ThemeColor.active_primary
        self.activeforeground = ThemeColor.white


class TTKWidgetCnfProvider(BasicCnfProvider):

    def __init__(self, **kwargs):
        BasicCnfProvider.__init__(self, **kwargs)


class SeparatorCnfProvider(TTKWidgetCnfProvider):

    def __init__(self, **kwargs):
        TTKWidgetCnfProvider.__init__(self, **kwargs)

        # 定义方向
        self.orient = HORIZONTAL


class PackCnfProvider(BasicCnfProvider):

    def __init__(
            self,
            before=None,
            after=None,
            anchor=NW,
            expand=FALSE,
            fill=NONE,
            side=TOP,
            ipadx=None,
            ipady=None,
            padx=(0, 0),
            pady=(0, 0),
            **kwargs
    ):
        BasicCnfProvider.__init__(self, **kwargs)

        # 在指定的组件前面进行pack
        self.before = before

        # 在指定的组件后面进行pack
        self.after = after

        # 组件在盒子中内容位置
        self.anchor = anchor

        # 若没有启用组件expand空间，则只包含组件独占空间
        self.expand = expand

        # 填充空间方式
        self.fill = fill

        # 空间位置，理解为CSS中float浮动属性
        self.side = side

        # 内部padding值
        self.ipadx = ipadx
        self.ipady = ipady

        # 外部边距值
        self.padx = padx
        self.pady = pady

    @property
    def float(self):
        return self.side

    @float.setter
    def float(self, value):
        self.side = value

    def pack(self, component):
        component.pack(self.build())
        return component


class GridCnfProvider(BasicCnfProvider):

    def __init__(self, **kwargs):
        BasicCnfProvider.__init__(self, **kwargs)

        # 行序号
        self.row = None

        # 列序号
        self.column = None

        # 行跨单元格
        self.rowspan = None

        # 列跨单元格
        self.columnspan = None

        # 类似anchor
        self.sticky = None

        # 外部边距值
        self.padx = [0, 0]
        self.pady = [0, 0]

    def grid(self, component):
        component.grid(self.build())
        return component


class PlaceCnfProvider(BasicCnfProvider):

    def __init__(self, **kwargs):
        BasicCnfProvider.__init__(self, **kwargs)

        # 水平绝对坐标
        self.x = None

        # 垂直绝对坐标
        self.y = None

        # 水平相对坐标，设置百分比0-1
        self.relx = None

        # 垂直相对坐标，设置百分比0-1
        self.rely = None

        self.weight = None
        self.height = None

        self.relweight = None
        self.relheight = None

    def place(self, component):
        component.place(self.build())
        return component
