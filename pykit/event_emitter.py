import copy
import time
from collections import defaultdict
from typing import Callable, Optional


class EventEmitter:

    def __init__(self):
        self._event_pool = defaultdict(lambda: [])

    def on(self, key: str):
        def decorator(func: Callable):
            self.add_event_listener(key, func)
            return func

        return decorator

    def one(self, key: str):
        def decorator(func: Callable):
            self.add_event_listener(key, func, True)
            return func

        return decorator

    def add_event_listener(self, key: str, callback: Callable, is_one=False):
        if is_one:
            def one_callback(*args):
                callback(*args)
                self._event_pool[key].remove(one_callback)

            self._event_pool[key].append(one_callback)
        else:
            self._event_pool[key].append(callback)

    def remove_event_listener(self, key: str, callback: Callable):
        if not isinstance(key, str):
            raise ValueError('key must be a string')
        self._event_pool[key].remove(callback)

    def remove_key(self, key: str):
        """

        移除指定key值的所有监听器

        :param key:
        :return:

        """
        self._event_pool.pop(key)

    def emit(self, key: str, args=None):
        if args is None:
            args = []
        for func in copy.copy(self._event_pool[key]):  # 防止回调函数中含有删除或者添加方法导致错误
            func(*args)

    def get(self, key: str, timeout=0, sleep=0.5) -> tuple:
        """

        提供一种同步阻塞的方式去监听key的返回值

        :param key: 监听key值
        :param timeout: 超时
        :param sleep: 延迟捕获
        :return:

        """
        result_args: Optional[tuple] = None
        timeout_flag = False
        start_time = time.time()

        def _callback(*args):
            """

            其它线程调取

            :param args:
            :return:

            """
            nonlocal result_args
            result_args = args

        self.add_event_listener(key, _callback)

        while not result_args:
            if 0 < timeout < (time.time() - start_time):
                timeout_flag = True
                break
            time.sleep(sleep)

        self.remove_event_listener(key, _callback)

        if timeout_flag:
            raise TimeoutError

        return result_args
