from tkinter import *
from tkinter import ttk

__author__ = {
    "project": "Tkinter 小工具开发模板",
    "version": " V1.0.0"
}


class Windows:

    def __init__(self, master, width=690, height=490):
        master.title(__author__["project"] + __author__["version"])
        master.geometry(str(width) + "x" + str(height))
        master.resizable(width=False, height=False)

        self.menu_init(master)
        self.tool_boxes_init(master, width)
        self.left_top_frame_init(master)
        self.left_middle_frame_init(master)
        self.left_bottom_frame_init(master)
        self.right_panel_init(master)
        self.footer_init(master)

    @staticmethod
    def menu_init(windows):
        menu = Menu(windows)

        file_menu = Menu(menu, tearoff=False)
        file_menu_list = (
            "新建...",
            "打开配置...",
            "保存配置...      Ctrl+S",
            "配置另存为...",
            "保存消息...",
            "查看当前消息日志",
            "打开消息日志文件夹",
            "退出(X)"
        )
        for i in range(0, len(file_menu_list)):
            if i == 4 or i == 7:
                file_menu.add_separator()
            file_menu.add_command(label=file_menu_list[i])
        menu.add_cascade(label="文件(F)", menu=file_menu)

        edit_menu = Menu(menu, tearoff=False)
        edit_menu_list = (
            "开始",
            "暂停",
            "停止",
            "Cloud Sync",
            "增加端口",
            "删除端口",
            "清除",
            "清除发送历史",
            "Line Mode"
        )
        for i in range(0, len(edit_menu_list)):
            if i == 3 or i == 4 or i == 6 or i == 8:
                edit_menu.add_separator()
            edit_menu.add_command(label=edit_menu_list[i])
        menu.add_cascade(label="编辑(E)", menu=edit_menu)

        view_menu = Menu(menu, tearoff=False)
        view_menu_list = (
            "水平",
            "垂直",
            "网格",
            "自定义",
            "快速设置",
            "窗口设置",
            "语言"
        )
        for i in range(0, len(view_menu_list)):
            if i == 4 or i == 5 or i == 6:
                view_menu.add_separator()
            view_menu.add_command(label=view_menu_list[i])
        menu.add_cascade(label="视图(V)", menu=view_menu)

        tool_menu = Menu(menu, tearoff=False)
        tool_menu_list = (
            "ToolBox...",
            "ASCII Code...",
            "选项"
        )
        for i in range(0, len(tool_menu_list)):
            if i == 2:
                tool_menu.add_separator()
            tool_menu.add_command(label=tool_menu_list[i])
        menu.add_cascade(label="工具(T)", menu=tool_menu)

        help_menu = Menu(menu, tearoff=False)
        help_menu.add_command(label="帮助文档")
        help_menu.add_command(label="联系作者")
        menu.add_cascade(label="帮助(H)", menu=help_menu)

        windows.config(menu=menu)

    @staticmethod
    def tool_boxes_init(windows, width):
        pass

    @staticmethod
    def left_top_frame_init(windows):
        frame = LabelFrame(windows, width=200, height=210, text="串口设置")
        frame.place(x=10, y=35)
        Label(frame, text="端  口").place(x=5, y=10)
        Label(frame, text="波特率").place(x=5, y=40)
        Label(frame, text="数据位").place(x=5, y=70)
        Label(frame, text="校验位").place(x=5, y=100)
        Label(frame, text="停止位").place(x=5, y=130)
        Label(frame, text="流  控").place(x=5, y=160)

    @staticmethod
    def left_middle_frame_init(windows):
        frame = LabelFrame(windows, width=200, height=120, text="接收设置")
        frame.place(x=10, y=250)
        Radiobutton(frame, text="ASCII").place(x=5, y=5)
        Radiobutton(frame, text="Hex").place(x=100, y=5)
        Checkbutton(frame, text="自动换行").place(x=5, y=30)
        Checkbutton(frame, text="显示发送").place(x=5, y=50)
        Checkbutton(frame, text="显示时间").place(x=5, y=70)

    @staticmethod
    def left_bottom_frame_init(windows):
        frame = LabelFrame(windows, width=200, height=80, text="发送设置")
        frame.place(x=10, y=375)
        Radiobutton(frame, text="ASCII").place(x=5, y=5)
        Radiobutton(frame, text="Hex").place(x=100, y=5)
        Checkbutton(frame, text="自动重发").place(x=5, y=30)
        Spinbox(frame, width=10).place(x=85, y=33)
        Label(frame, text="ms").place(x=170, y=30)

    @staticmethod
    def right_panel_init(windows):
        display_text_area = Text(windows, width=65, height=23)
        display_text_area.place(x=220, y=40)
        send_text_area = Text(windows, width=55, height=5)
        send_text_area.place(x=220, y=352)
        Button(windows, text=" 清   空 ").place(x=620, y=351)
        Button(windows, text=" 发   送 ").place(x=620, y=390)
        ttk.Combobox(windows, width=62).place(x=220, y=430)

    @staticmethod
    def footer_init(windows):
        button_frame = Frame(windows, bg="#DCDCDC", width=700, height=30)
        button_frame.place(x=0, y=460)

        footer_display_1 = Text(button_frame, width=40, height=1)
        footer_display_1.insert(END, "底部显示1")
        footer_display_1.config(state=DISABLED)
        footer_display_1.place(x=5, y=5)

        footer_display_2 = Text(button_frame, width=20, height=1)
        footer_display_2.insert(END, "底部显示2")
        footer_display_2.config(state=DISABLED)
        footer_display_2.place(x=390, y=5)

        footer_display_3 = Text(button_frame, width=20, height=1)
        footer_display_3.insert(END, "底部显示3")
        footer_display_3.config(state=DISABLED)
        footer_display_3.place(x=540, y=5)


if __name__ == '__main__':
    root = Tk()
    app = Windows(root)
    root.mainloop()
