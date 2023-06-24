from cefpython3 import cefpython as cef

from tkinter import *
import threading
import sys


# cefpython3 目前只支持python3.7，高版本Python不兼容
def embed_browser_thread(frame, _rect):
    sys.excepthook = cef.ExceptHook
    window_info = cef.WindowInfo(frame.winfo_id())
    window_info.SetAsChild(frame.winfo_id(), _rect)
    cef.Initialize()
    cef.CreateBrowserSync(window_info, url='http://www.baidu.com')
    cef.MessageLoop()


if __name__ == '__main__':
    root = Tk()
    root.geometry("800x600")

    frame1 = Frame(root, bg='blue', height=200)
    frame1.pack(side=TOP, fill=X)

    frame2 = Frame(root, bg='white', height=200)
    frame2.pack(side=TOP, fill=X)

    rect = [0, 0, 800, 200]
    thread = threading.Thread(target=embed_browser_thread, args=(frame1, rect))
    thread.setDaemon(True)
    thread.start()

    root.mainloop()
