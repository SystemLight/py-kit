import json
import os
from typing import Dict, Any, NoReturn


def require(path: str, encoding: str = 'utf-8') -> Dict[str, Any]:
    """

    有时你可能只是需要从文件中读取到json数据，这是require函数将根据
    获取到的path，返回dict对象，相当方便，该函数同样类似于json.load

    :param path: json文件路径
    :param encoding: 编码方式
    :return: dict

    """
    fp = open(path, 'r', encoding=encoding)
    data = fp.read()
    fp.close()
    try:
        return json.loads(data)
    except json.decoder.JSONDecodeError:
        return {}


def read(path: str, encoding: str = 'utf-8') -> str:
    """

    读取文件返回字符串

    :param path: 文件路径
    :param encoding: 编码方式
    :return: 读取所有字符串

    """
    with open(path, 'r', encoding=encoding) as fp:
        result = fp.read()
    return result


def read_bytes(path: str) -> bytes:
    """

    读取文件返回bytes

    :param path: 文件路径
    :return: 读取所有字符串

    """
    with open(path, 'rb') as fp:
        result = fp.read()
    return result


def write(path: str, data: str, encoding: str = 'utf-8') -> NoReturn:
    """

    将字符串写入文件当中

    :param path: 文件路径
    :param data: 写入的字符串数据
    :param encoding: 编码方式
    :return:

    """
    with open(path, 'w', encoding=encoding) as fp:
        fp.write(data)


def write_bytes(path: str, data: bytes) -> NoReturn:
    """

    将bytes写入文件当中

    :param path: 文件路径
    :param data: 写入的字符串数据
    :return:

    """
    with open(path, 'wb') as fp:
        fp.write(data)


def insert2fp(file_path, offset, content, per_size=2048):
    """

    允许你在文件指定位置进行内容插入

    :param file_path: 文件路径
    :param offset: 文件偏移位置
    :param content: 插入的内容
    :param per_size: 每片读取大小限制
    :return: None

    """
    copies = offset // per_size

    f_dir, f_name = os.path.split(file_path)
    temp_path = os.path.join(f_dir, f_name + '.temp')

    with open(temp_path, 'w') as w_fp:
        with open(file_path, 'r') as fp:
            fp.seek(0)

            for c in range(1, copies + 1 + int(offset % per_size > 0)):
                if c * per_size >= offset:
                    result = fp.read(offset - fp.tell())
                else:
                    result = fp.read(per_size)
                w_fp.write(result)

            w_fp.write(content)

            for c in fp:
                w_fp.write(c)

    os.remove(file_path)
    os.rename(temp_path, file_path)


def check_join(root_path: str, *args) -> str:
    """

    检查合并后的路径是否在root_path当中，如果超出抛出异常

    :param root_path: 根路径
    :param args: 路径块集合
    :return: 合并后的绝对路径

    """
    root_path = os.path.abspath(root_path)
    result_path = os.path.abspath(os.path.join(root_path, *args))
    if not result_path.startswith(root_path):
        raise ValueError('Illegal path')
    return result_path


def safe_join(*args) -> str:
    """

    合并给定路径成为一个绝对路径，如果某个子路径块超出父路径就会抛出异常

    :param args: 路径块集合
    :return: 合并后的绝对路径

    """
    safe_path = args[0]
    for i in range(1, len(args)):
        safe_path = check_join(safe_path, args[i])
    return safe_path


def int_content2bytes(content: int):
    return str(content).encode('utf-8')


def gbk2utf8(path: str):
    """

    gbk编码转utf8编码

    :param path: 文件路径
    :return:

    """

    with open(path, 'r', encoding='gbk') as fp:
        content = fp.read()
    with open(path, 'w', encoding='utf-8') as fp:
        fp.write(content)
