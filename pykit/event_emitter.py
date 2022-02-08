from collections import defaultdict
from typing import Callable


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
        self._event_pool.pop(key)

    def emit(self, key: str, args=None):
        if args is None:
            args = []
        for func in self._event_pool[key]:
            func(*args)
