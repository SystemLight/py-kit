PT = 1 / 72  # 1pt 等于 1/72 英寸


def in2cm(source):
    return source * 2.54


def cm2in(source):
    return source / 2.54


def pt2px(source, dpi=96):
    return source * dpi * PT


def px2pt(source, dpi=96):
    return source / (dpi * PT)


def dpi72to300(source: int):
    return source * 300 / 72
