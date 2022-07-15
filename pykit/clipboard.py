from ctypes import cdll, windll, memmove, sizeof, c_size_t, c_wchar_p, c_wchar, wstring_at
from ctypes.wintypes import (
    HGLOBAL, LPVOID, DWORD, LPCSTR, INT, HWND,
    HINSTANCE, HMENU, BOOL, UINT, HANDLE
)

msvcrt = cdll.msvcrt
user32 = windll.user32
kernel32 = windll.kernel32

# https://docs.microsoft.com/zh-cn/windows/win32/dataxchg/standard-clipboard-formats
# https://docs.microsoft.com/zh-cn/windows/win32/api/winuser/nf-winuser-openclipboard
CF_UNICODETEXT = 13
GMEM_MOVEABLE = 0x0002

wcslen = msvcrt.wcslen
wcslen.argtypes = [c_wchar_p]
wcslen.restype = UINT

GlobalAlloc = kernel32.GlobalAlloc
GlobalAlloc.argtypes = [UINT, c_size_t]
GlobalAlloc.restype = HGLOBAL

GlobalLock = kernel32.GlobalLock
GlobalLock.argtypes = [HGLOBAL]
GlobalLock.restype = LPVOID

GlobalUnlock = kernel32.GlobalUnlock
GlobalUnlock.argtypes = [HGLOBAL]
GlobalUnlock.restype = BOOL

CreateWindowExA = user32.CreateWindowExA
CreateWindowExA.argtypes = [
    DWORD, LPCSTR, LPCSTR, DWORD, INT, INT,
    INT, INT, HWND, HMENU, HINSTANCE, LPVOID
]
CreateWindowExA.restype = HWND

DestroyWindow = user32.DestroyWindow
DestroyWindow.argtypes = [HWND]
DestroyWindow.restype = BOOL

OpenClipboard = user32.OpenClipboard
OpenClipboard.argtypes = [HWND]
OpenClipboard.restype = BOOL

CloseClipboard = user32.CloseClipboard
CloseClipboard.argtypes = []
CloseClipboard.restype = BOOL

EmptyClipboard = user32.EmptyClipboard
EmptyClipboard.argtypes = []
EmptyClipboard.restype = BOOL

GetClipboardData = user32.GetClipboardData
GetClipboardData.argtypes = [UINT]
GetClipboardData.restype = HANDLE

SetClipboardData = user32.SetClipboardData
SetClipboardData.argtypes = [UINT, HANDLE]
SetClipboardData.restype = HANDLE

if __name__ == '__main__':
    # 获取剪贴板数据
    if user32.IsClipboardFormatAvailable(CF_UNICODETEXT) and OpenClipboard(None):
        h_mem = GetClipboardData(CF_UNICODETEXT)
        mem = GlobalLock(h_mem)
        text = wstring_at(mem)
        GlobalUnlock(h_mem)

        # 清除剪贴版数据
        EmptyClipboard()

        # 写入数据
        text += '：后缀'
        count = wcslen(text) + 1
        handle = GlobalAlloc(GMEM_MOVEABLE, count * sizeof(c_wchar))
        locked_handle = GlobalLock(handle)
        memmove(c_wchar_p(locked_handle), c_wchar_p(text), count * sizeof(c_wchar))
        GlobalUnlock(handle)
        SetClipboardData(CF_UNICODETEXT, handle)

        CloseClipboard()
