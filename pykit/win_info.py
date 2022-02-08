import ctypes


class DeviceCap:
    DRIVERVERSION = 0
    TECHNOLOGY = 2
    HORZSIZE = 4
    VERTSIZE = 6
    HORZRES = 8
    VERTRES = 10
    BITSPIXEL = 12
    PLANES = 14
    NUMBRUSHES = 16
    NUMPENS = 18
    NUMMARKERS = 20
    NUMFONTS = 22
    NUMCOLORS = 24
    PDEVICESIZE = 26
    CURVECAPS = 28
    LINECAPS = 30
    POLYGONALCAPS = 32
    TEXTCAPS = 34
    CLIPCAPS = 36
    RASTERCAPS = 38
    ASPECTX = 40
    ASPECTY = 42
    ASPECTXY = 44
    SHADEBLENDCAPS = 45
    LOGPIXELSX = 88  # 逻辑上每英寸的像素数
    LOGPIXELSY = 90  # 逻辑上每英寸的像素数
    SIZEPALETTE = 104
    NUMRESERVED = 106
    COLORRES = 108
    PHYSICALWIDTH = 110
    PHYSICALHEIGHT = 111
    PHYSICALOFFSETX = 112
    PHYSICALOFFSETY = 113
    SCALINGFACTORX = 114
    SCALINGFACTORY = 115
    VREFRESH = 116
    DESKTOPVERTRES = 117
    DESKTOPHORZRES = 118
    BLTALIGNMENT = 119


def get_device_caps(device_cap: int):
    user32 = ctypes.windll.user32
    gdi32 = ctypes.windll.gdi32
    dc = user32.GetDC(None)
    return gdi32.GetDeviceCaps(dc, device_cap)


def get_dpi():
    return get_device_caps(DeviceCap.LOGPIXELSX)
