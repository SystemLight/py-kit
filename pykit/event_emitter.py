import queue
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
                self.remove_event_listener(key, one_callback)

            self._event_pool[key].append(one_callback)
        else:
            self._event_pool[key].append(callback)

    def remove_event_listener(self, key: str, callback: Callable):
        if not isinstance(key, str):
            raise ValueError('key must be a string')

        try:
            self._event_pool[key].remove(callback)
        except ValueError:
            ...

    def remove(self, key: str):
        """

        移除指定key值的所有监听器

        :param key:
        :return:

        """
        return self._event_pool.pop(key)

    def emit(self, key: str, args=None):
        if args is None:
            args = []

        for func in self._event_pool[key][:]:
            func(*args)

    def get(self, key: str, timeout=0, sleep=0.5, on_hook: Callable = None) -> tuple:
        """

        非线程安全，提供一种同步阻塞的方式去监听key的返回值，具备自动销毁机制，没有存储功能
        为了保证线程安全，多线程模式需要为emit方法加锁

        :param key: 监听key值
        :param timeout: 超时
        :param sleep: 延迟捕获
        :param on_hook: 延迟捕获
        :return:

        """
        result_args: Optional[tuple] = None
        timeout_flag = False
        start_time = time.time()

        def _callback(*args):
            """

            其它线程调取，多线程同时emit可能会产生错误结果，非线程安全

            :param args:
            :return:

            """
            nonlocal result_args
            result_args = args

        self.add_event_listener(key, _callback)

        on_hook and on_hook()

        while not result_args:
            if 0 < timeout < (time.time() - start_time):
                timeout_flag = True
                break
            time.sleep(sleep)

        self.remove_event_listener(key, _callback)

        if timeout_flag:
            raise TimeoutError

        return result_args

    def queue(self, key: str, maxsize=0, block=True, timeout=None):
        """

        使用queue方法注意需要通过remove方法移除所有监听器

        :param key:
        :param maxsize:
        :param block:
        :param timeout:
        :return:

        """
        q = queue.Queue(maxsize)

        def _callback(*args):
            """

            其它线程调取

            :param args:
            :return:

            """
            q.put(args, block=block, timeout=timeout)

        self.add_event_listener(key, _callback)

        return q

    def listen(self, key: str):
        """

        跟简便的方式使用queue()方法，通用需要通过remove方法移除所有监听器

        :param key:
        :return:

        """
        q = self.queue(key)

        while True:
            yield q.get()
