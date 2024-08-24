import copy
import json
import textwrap
from typing import List, Dict, Union, Optional, Callable, TypeVar, Iterable, Tuple, Type


def extract_jpg_from_pdf(path):
    pdf = open(path, "rb").read()

    start_mark = b"\xff\xd8"
    start_fix = 0
    end_mark = b"\xff\xd9"
    end_fix = 2

    i = 0
    n_jpg = 0

    while True:
        is_stream = pdf.find(b"stream", i)
        if is_stream < 0:
            break

        is_start = pdf.find(start_mark, is_stream, is_stream + 20)
        if is_start < 0:
            i = is_stream + 20
            continue

        is_end = pdf.find(b"endstream", is_start)
        if is_end < 0:
            raise Exception("Didn't find end of stream !")
        is_end = pdf.find(end_mark, is_end - 20)
        if is_end < 0:
            raise Exception("Didn't find end of JPG!")

        is_start += start_fix
        is_end += end_fix

        print("JPG %d from %d to %d" % (n_jpg, is_start, is_end))
        jpg = pdf[is_start:is_end]

        print("提取图片" + "pic_%d.jpg" % n_jpg)
        jpg_file = open("pic_%d.jpg" % n_jpg, "wb")
        jpg_file.write(jpg)
        jpg_file.close()

        n_jpg += 1
        i = is_end


def scale(number, decimal_str="01"):
    """

    转换十进制成为任意进制数值，进制字母可自定义

    :param number: 十进制数值
    :param decimal_str: 默认数值字符是01，也就是说默认是转换成传统二进制数值
    :return: 进制转换后的数值字符串

    """
    alphabet = list(decimal_str)
    decimal = len(alphabet)
    output = ""
    while number != 0:
        number, digit = divmod(number, decimal)
        output += alphabet[digit]
    if output is "":
        output = alphabet[0]
    return output[::-1]


def str2unicode_str(n=5371):
    """

    该方法在获取a-z，0-9这种字符时得不到编码值，但是python3中的ord函数实现的便是Unicode编码值返回。
    print(ord("a"))

    """
    return (b"\u" + str(n).encode("unicode_escape")).decode("unicode_escape")


def mod(a, b):
    c = a // b
    r = a - c * b
    return r


def rem(a, b):
    c = int(a / b)
    r = a - c * b
    return r


def xabs(n):
    """

    取绝对值

    """
    s = n >> 32
    return (n ^ s) - s


def xover(n):
    """

    超出归零

    """
    s = n - 10 >> 32
    return n & s


def omit(obj: dict, fields: List[str]):
    new_obj = copy.copy(obj)
    for key in fields:
        try:
            new_obj.pop(key)
        except KeyError:
            continue
    return new_obj


def find_key(obj: Union[Dict, List], key: str):
    """

    根据字符串查找对象值，字符串形式如a.b.0，
    查找对象，如::

        {'a':{'b':['val']}}

    val值将被查出

    :param obj: 查找key值的对象
    :param key: 查找key
    :return: 查找到的值

    """
    key_list = key.split('.')
    for k in key_list:
        if isinstance(obj, list):
            val = obj[int(k)]
        else:
            val = obj.get(k)
        if val is None:
            return None
        else:
            obj = val
    return obj


def inin(content: str, pool: List[str]) -> Optional[str]:
    """

    查找指定内容是否存在于列表的字符串中，这种情况content一定要比列表中字符串短

    举例::

        inin('a',['asdf','fsfsdf']) 将返回 'asdf'

    :param content: 内容
    :param pool: 列表
    :return: 匹配内容

    """
    for p in pool:
        if content in p:
            return p
    return None


def rinin(content: str, pool: List[str]) -> Optional[str]:
    """

    查找指定内容是否存在于列表的字符串中，这种情况content一定要比列表中字符串长

    举例::

        inin('asdf',['a','fsfsdf']) 将返回 'a'

    :param content: 内容
    :param pool: 列表
    :return: 匹配内容

    """
    for p in pool:
        if p in content:
            return p
    return None


IT = TypeVar('IT')


def find(iterable: Iterable[IT], func: Callable[[IT], bool]) -> Tuple[int, Optional[IT]]:
    """

    查找可迭代对象的指定项，匹配第一个子项并返回，无匹配项时返回(-1,None)

    :param func: 匹配函数
    :param iterable: 可迭代对象
    :return: 索引，子对象

    """
    for i, v in enumerate(iterable):
        if func(v):
            return i, v
    return -1, None


def retry(freq: int = 3, retry_hook: Optional[Callable[[int], None]] = None) -> Callable:
    """

    装饰器，为函数添加此装饰器当函数抛出异常时会对函数重新调用，重新调用次数取决于freq指定的参数

    :param freq: 重试次数
    :param retry_hook: 钩子函数，当函数重调用时回调的函数
    :return: 原函数返回值

    """

    def decorator(func):
        def wrap(*args, **kwargs):
            now_freq = 1
            while True:
                try:
                    result = func(*args, **kwargs)
                    break
                except Exception as e:
                    if now_freq > freq:
                        raise e
                    now_freq += 1
                    if hasattr(retry_hook, '__call__'):
                        retry_hook(now_freq)

            return result

        return wrap

    return decorator


class AdvancedJSONEncoder(json.JSONEncoder):
    """

    定义ApiController JSON解析器

    """
    find_dict = {
        'date': lambda v: v.strftime('%Y-%m-%d'),
        'datetime': lambda v: v.strftime('%Y-%m-%d %H:%M'),
        'Decimal': lambda v: v.to_eng_string()
    }

    def default(self, obj):
        deal_with = self.find_dict.get(type(obj).__name__, None)
        if deal_with:
            return deal_with(obj)
        else:
            return super(AdvancedJSONEncoder, self).default(obj)


def prettier_hex(data: Union[int, bytes, str, None], sep=' ', _width=None):
    if data is None:
        return ''

    if isinstance(data, int):
        hex_result = format(data, 'x')
        if len(hex_result) % 2 > 0:
            hex_result = '0' + hex_result
        result = sep.join(textwrap.wrap(hex_result, width=2))
    elif isinstance(data, bytes):
        result = data.hex(sep)
    elif isinstance(data, str):
        return sep.join(textwrap.wrap(data, width=2))
    else:
        raise ValueError

    if _width:
        result = result.zfill(_width)
    return result


def pp_hex(data: Union[int, bytes, str], sep=' '):
    print(prettier_hex(data, sep))


def array2str(data: list):
    return ''.join(map(lambda v: str(v), data))


def at(data_ist, index, default=None):
    try:
        return data_ist[index]
    except IndexError:
        return default


class ProxyWatcher:

    def __init__(self, proxy_master: "Proxy"):
        self.proxy_master = proxy_master
        self.container = proxy_master.container

    def watch(self, key, invoke):
        ...


class Proxy:

    def __init__(self, container, *args: Type[ProxyWatcher]):
        self.container = container

        watchers = list(args)  # type: List
        for index in range(len(watchers)):
            watcher = watchers[index]
            watchers[index] = watcher(self)

        self.watchers = watchers  # type: List[ProxyWatcher]
        self.watcher_map = {}

    def __getattr__(self, key):
        invoke = None
        if hasattr(self.container, key):
            invoke = getattr(self.container, key)
        self.watch(key, invoke)
        return self.proxy(key, invoke)

    def proxy(self, key: str, invoke):
        proxy_invoke = None
        for watcher in self.watchers:
            proxy_handler_method = f'proxy_{key}'
            proxy_handler_factory_method = f'{proxy_handler_method}_factory'

            if hasattr(watcher, proxy_handler_factory_method):
                proxy_invoke = getattr(watcher, proxy_handler_factory_method)(invoke)
            elif hasattr(watcher, proxy_handler_method):
                proxy_invoke = getattr(watcher, proxy_handler_method)

            if proxy_invoke is not None:
                break

        return proxy_invoke or invoke

    def set_watcher(self, key, handler):
        self.watcher_map[key] = handler

    def watch(self, key, invoke):
        for watcher in self.watchers:
            watcher.watch(key, invoke)

        watcher_handler = self.watcher_map.get(key)
        if watcher_handler:
            watcher_handler(key, invoke)


class ProxyClass:

    def __init__(self, container_class, *args: Type[ProxyWatcher]):
        self.container_class = container_class
        self.watchers = args

    def __call__(self, *args, **kwargs):
        return Proxy(
            self.container_class(*args, **kwargs),
            *self.watchers
        )


class Place:

    def __init__(self, max_num=0):
        self.max_num = max_num
        self.after_place = None
        self.before_place = None
        self.index = 0

    def after(self, place: "Place"):
        self.after_place = place
        place.before(self)
        return place

    def before(self, place: "Place"):
        self.before_place = place
        return place

    def step(self):
        if self.index >= self.max_num:
            if self.before_place:
                self.before_place.step()
            else:
                raise IndexError('超出最大存储范围')
            self.reset()
            return self
        self.index += 1
        return self

    def reset(self):
        self.index = 0
        if self.after_place:
            self.after_place.reset()


class PlaceManager:

    def __init__(self, data):
        self.data = data
        self.root_place = None
        self.place_list = []

        for i in range(len(data)):
            p = Place(len(data[i]))
            if self.root_place:
                self.root_place.after(p)
            self.place_list.append(p)
            self.root_place = p

    def step(self):
        if self.root_place:
            self.root_place.step()

    def get_index(self, is_max=False):
        result = []
        place = self.root_place
        while place:
            result.append(place.max_num if is_max else place.index)
            place = place.before_place
        result.reverse()
        return result

    def get_max_num(self):
        result = 1
        index_list = self.get_index(True)
        for i in range(len(index_list)):
            result *= index_list[i]
        return result
