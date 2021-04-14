def gbk2utf8(path: str):
    """

    gbk编码转utf8编码

    :param path: 文件路径
    :return:

    """

    with open(path, "r", encoding="gbk") as fp:
        content = fp.read()
    with open(path, "w", encoding="utf-8") as fp:
        fp.write(content)
