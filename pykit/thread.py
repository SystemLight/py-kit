import time
from threading import Thread, Lock
from typing import Optional, Callable


def fiber(start: Optional[Callable] = None, end: Optional[Callable] = None):
    """

    `装饰器`，封装一个函数作为线程执行，允许传入开始和结束的回调函数

    :param start: 开始执行函数的回调
    :param end: 结束执行函数的回调
    :return: 函数封装器

    """

    def decorator(func):
        def wrap(*args):
            def task():
                if start:
                    start(*args)
                func(*args)
                if end:
                    end(*args)

            Thread(target=task).start()

        return wrap

    return decorator


class TaskThread(Thread):

    def __init__(self, name=None, target=None, args=(), kwargs=None):
        super().__init__(name=name, target=target, args=args, kwargs=kwargs, daemon=True)

        self._is_run_flag = False
        self._is_exit = False
        self.before_run = None
        self.after_run = None

    @property
    def is_run_flag(self):
        return self._is_run_flag

    @property
    def is_exit(self):
        return self._is_exit

    def run(self) -> None:
        self._is_run_flag = True
        self._is_exit = False
        self.before_run and self.before_run()
        try:
            if self._target:
                self._target(*self._args, **self._kwargs)
        finally:
            del self._target, self._args, self._kwargs
        self._is_exit = True
        self.after_run and self.after_run()

    def terminate(self):
        """

        发送终端信号

        :return:

        """
        self._is_run_flag = False
        return self._is_exit

    def wait(self):
        """

        等待线程彻底退出

        :return:

        """
        while not self._is_exit:
            time.sleep(0.1)
        return self._is_exit


class SingletonTask:

    def __init__(self, boot_func):
        """

        单例任务

        :param boot_func: 不能为阻塞函数，主要用于启动执行，一般配合线程start使用

        """
        self._boot_func = boot_func
        self._on_call_stop_func = None
        self._is_start = False
        self._mutex = Lock()

    def start(self, *args):
        with self._mutex:
            if not self._is_start:
                self._boot_func(*args)
                self._is_start = True

    def stop(self, *args):
        with self._mutex:
            if self._is_start:
                self._on_call_stop_func and self._on_call_stop_func(*args)
                self._is_start = False

    def on_stop(self, on_call_stop_func: Callable):
        """

        注册停止时执行的函数

        :param on_call_stop_func:
        :return:

        """
        self._on_call_stop_func = on_call_stop_func


class SingletonTaskThread(SingletonTask):

    def __init__(self, target_func: Callable[["SingletonTaskThread", ...], None]):
        self._thread: Optional[TaskThread] = None
        super().__init__(self._wrap_boot_func(target_func))
        self._on_call_stop_func = self._on_call_stop

    @property
    def run_flag(self):
        return self._thread.is_run_flag

    def _wrap_boot_func(self, target_func: Callable):
        def _boot_func(*args):
            if self._thread is None:
                self._thread = TaskThread(target=target_func, args=[self, *args])
            self._thread.start()

        return _boot_func

    def _on_call_stop(self):
        self._thread.terminate()

    def wait(self):
        self._thread.wait()
