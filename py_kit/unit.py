PT = 1 / 72


def in2cm(source):
    return source * 2.54


def cm2in(source):
    return source / 2.54


def pt2px(source, dpi=96):
    return source * dpi * PT


def px2pt(source, dpi=96):
    return source / (dpi * PT)
