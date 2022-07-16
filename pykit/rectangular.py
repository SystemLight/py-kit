def rectangular_factor(x0, y0, x1, y1):
    """

    根据左上角和右下角坐标返回的Rectangular对象

    :return: Rectangular

    """
    return Rectangular(x0, y0, x1 - x1, y1 - y0)


class Rectangular:

    def __init__(self, x, y, w, h):
        """

        矩形对象，不考虑矩阵变换矩形

        :param x: 左上角x坐标点
        :param y: 左上角y坐标点
        :param w: 矩形宽度
        :param h: 矩形高度

        """
        self.x0 = x
        self.y0 = y
        self.x1 = x + w
        self.y1 = y + h
        self.w = w
        self.h = h

    def __gt__(self, other):
        if self.w > other.w and self.h > other.h:
            return True
        return False

    def __lt__(self, other):
        if self.w < other.w and self.h < other.h:
            return True
        return False

    def collision(self, r2):
        """

        判断两个矩形是否产生碰撞关系

        r1.x0 < r2.x1
        r1.y0 < r2.y1
        r1.x1 > r2.x0
        r1.y1 > r2.y0

        :param r2: Rectangular
        :return: 布尔

        """
        if self.x0 < r2.x1 and self.y0 < r2.y1 and self.x1 > r2.x0 and self.y1 > r2.y0:
            return True
        return False

    def contain(self, r2):
        """

        判断矩形中是否包含另外一个矩形r2，注意包含也是矩形碰撞所以collision方法会返回True

        r1.x0 < r2.x0
        r1.x1 > r2.x1
        r1.y0 < r2.y0
        r1.y1 > r2.y1

        :param r2: Rectangular
        :return: 布尔

        """
        if self.x0 < r2.x0 and self.x1 > r2.x1 and self.y0 < r2.y0 and self.y1 > r2.y1:
            return True
        return False


if __name__ == '__main__':
    rr1 = Rectangular(460, 353, 100, 100)
    rr2 = Rectangular(300, 300, 200, 200)
    print(rr2.collision(rr1))  # 碰撞
    print(rr2.contain(rr1))  # 不包含

    rr1 = Rectangular(393, 360, 100, 100)
    rr2 = Rectangular(300, 300, 200, 200)
    print(rr1.collision(rr2))  # 碰撞
    print(rr2.contain(rr1))  # rr2包含rr1矩形
    print(rr2 > rr1)  # rr2两边全大于rr1，返回True
    print(rr1.contain(rr2))  # rr1不包含rr2，因为rr2大
